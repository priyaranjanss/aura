"""Chat API routes.

Phase 2: validates requests and returns a placeholder reply so the
frontend <-> backend round trip works. Intent detection (Phase 3) and
Gemini (Phase 4) will replace the placeholder logic later.
"""

from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api", tags=["chat"])

# Simple greetings that get a friendly hello back.
_GREETINGS = {"hello", "hi", "hey", "hey aura", "hello aura", "namaste"}


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """Handle a user message and return the assistant's reply."""
    message = payload.message.strip().lower()

    if message in _GREETINGS:
        reply = (
            "Hello! I'm AURA, your voice assistant. "
            "Ask me anything, or try a command like 'open chrome'."
        )
    else:
        reply = (
            f"You said: \"{payload.message}\" - I'm still learning in Phase 2. "
            "Ask me something or try a command like 'open chrome'."
        )

    return ChatResponse(reply=reply, type="ai", success=True, audio_url=None)
