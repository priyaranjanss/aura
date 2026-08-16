"""Chat API routes.

Phase 4 (AI-first): EVERY message is analyzed by the AI brain first. The AI
decides the intent (any phrasing) and suggests a command; Python validates the
command against the safe action set and executes it. Keyword matching remains
as an offline fallback when the AI service is unavailable.
"""

from fastapi import APIRouter

from app import config
from app.models.schemas import ChatRequest, ChatResponse, build_analysis
from app.services import ai_service, command_service

router = APIRouter(prefix="/api", tags=["chat"])


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

    # 2. If the AI suggested a command, validate it and execute it.
    if ai_result and ai_result.get("command"):
        result = command_service.execute_ai_command(ai_result["command"])
        if result is not None:
            analysis = build_analysis(
                ai_result.get("analysis") or result.get("analysis", {})
            )
            return ChatResponse(
                reply=result["reply"],
                type="command",
                success=result["success"],
                audio_url=None,
                analysis=analysis,
            )

    # 3. Offline fallback: keyword-based detection (works without the AI).
    result = command_service.handle(payload.message)
    if result is not None:
        return ChatResponse(
            reply=result["reply"],
            type="command",
            success=result["success"],
            audio_url=None,
            analysis=build_analysis(result.get("analysis", {})),
        )

    # 4. Conversation: show the AI's answer (or a friendly error if AI is down).
    if ai_result is not None:
        analysis = build_analysis(
            ai_result.get("analysis")
            or {"what": "Answer the user's question", "how": f"AI provider ({config.AI_PROVIDER})"}
        )
        return ChatResponse(
            reply=ai_result["reply"],
            type="ai",
            success=True,
            audio_url=None,
            analysis=analysis,
        )

    return ChatResponse(
        reply=(
            "Sorry, I couldn't reach the AI service. "
            "Check that AI_PROVIDER and AI_API_KEY are set correctly in backend/.env."
        ),
        type="error",
        success=False,
        audio_url=None,
        analysis=build_analysis(
            {"what": "Answer the user's question", "how": "AI service unavailable"}
        ),
    )
