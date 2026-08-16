"""Chat API routes.

Phase 4 (AI-first): EVERY message is analyzed by the AI brain first. The AI
decides the intent (any phrasing) and suggests a command; Python validates the
command against the safe action set and executes it. Keyword matching remains
as an offline fallback when the AI service is unavailable.

Phase 5: every reply also gets TTS audio (edge-tts) via `audio_url` so the
frontend can speak it aloud.
"""

from fastapi import APIRouter, HTTPException

from app import config
from app.models.schemas import ChatRequest, ChatResponse, build_analysis
from app.services import ai_service, command_service, speech_service

router = APIRouter(prefix="/api", tags=["chat"])


@router.delete("/audio/{filename}")
def delete_audio(filename: str):
    """Delete a generated audio file once the frontend has played it.

    The filename is strictly validated (32-hex + .mp3) so this can only ever
    remove generated TTS files.
    """
    if not speech_service.delete_audio(filename):
        raise HTTPException(status_code=404, detail="Audio file not found")
    return {"deleted": True}


def _with_audio(**fields) -> ChatResponse:
    """Build a ChatResponse and attach TTS audio for the reply (best effort)."""
    reply = fields["reply"]
    fields["audio_url"] = speech_service.generate_speech(reply)
    return ChatResponse(**fields)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """Handle a user message: AI analyzes it, then safe code executes."""
    history = [m.model_dump() for m in payload.history]

    # 1. AI brain: analyze the request (intent + question analysis + reply).
    ai_result = None
    try:
        ai_result = ai_service.generate_reply(payload.message, history)
    except Exception as e:  # noqa: BLE001 - the app must never crash on AI failure
        print(f"[ai] generate_reply failed: {e}")

    # 2. If the AI suggested commands (one or more steps), validate and run
    #    each one in order ("open notepad and minimize it" -> two steps).
    if ai_result and ai_result.get("steps"):
        results = command_service.execute_ai_steps(ai_result["steps"])
        if results:
            reply = " ".join(r["reply"] for r in results)
            success = all(r["success"] for r in results)
            analysis = build_analysis(
                ai_result.get("analysis") or results[0].get("analysis", {})
            )
            return _with_audio(
                reply=reply,
                type="command",
                success=success,
                analysis=analysis,
            )

    # 3. Offline fallback: keyword-based detection (works without the AI).
    result = command_service.handle(payload.message)
    if result is not None:
        return _with_audio(
            reply=result["reply"],
            type="command",
            success=result["success"],
            analysis=build_analysis(result.get("analysis", {})),
        )

    # 4. Conversation: show the AI's answer (or a friendly error if AI is down).
    if ai_result is not None:
        analysis = build_analysis(
            ai_result.get("analysis")
            or {"what": "Answer the user's question", "how": f"AI provider ({config.AI_PROVIDER})"}
        )
        return _with_audio(
            reply=ai_result["reply"],
            type="ai",
            success=True,
            analysis=analysis,
        )

    return _with_audio(
        reply=(
            "Sorry, I couldn't reach the AI service. "
            "Check that AI_PROVIDER and AI_API_KEY are set correctly in backend/.env."
        ),
        type="error",
        success=False,
        analysis=build_analysis(
            {"what": "Answer the user's question", "how": "AI service unavailable"}
        ),
    )
