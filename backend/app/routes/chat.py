"""Chat API routes.

Phase 3: messages are checked against the command service first; known
commands execute a system action, everything else falls back to a
conversation reply (Gemini in Phase 4).
"""

from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse
from app.services import command_service

router = APIRouter(prefix="/api", tags=["chat"])

# Simple greetings that get a friendly hello back.
_GREETINGS = {"hello", "hi", "hey", "hey aura", "hello aura", "namaste"}


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """Handle a user message: execute a command or reply conversationally."""
    # 1. Try a system command first.
    result = command_service.handle(payload.message)
    if result is not None:
        return ChatResponse(
            reply=result["reply"],
            type="command",
            success=result["success"],
            audio_url=None,
        )

    # 2. Not a command -> conversation placeholder (Gemini arrives in Phase 4).
    message = payload.message.strip().lower()
    if message in _GREETINGS:
        reply = (
            "Hello! I'm AURA, your voice assistant. "
            "Ask me anything, or try a command like 'open chrome'."
        )
    else:
        reply = (
            f"You said: \"{payload.message}\" - I'm still learning. "
            "Ask me something, or try a command like 'open chrome' or 'what time is it'."
        )

    return ChatResponse(reply=reply, type="ai", success=True, audio_url=None)
