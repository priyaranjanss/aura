"""Pydantic request/response models for the AURA chat API."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single message in the conversation history."""

    role: Literal["user", "assistant"] = "user"
    content: str


class ChatRequest(BaseModel):
    """Body of POST /api/chat."""

    message: str = Field(..., min_length=1, description="User message")
    history: List[ChatMessage] = Field(
        default_factory=list,
        description="Optional conversation history for context",
    )


class ChatResponse(BaseModel):
    """Response returned by POST /api/chat."""

    reply: str = Field(..., description="Assistant's text reply")
    type: Literal["command", "ai", "error"] = Field(
        "ai", description="Reply type: system command, AI answer, or error"
    )
    success: bool = True
    audio_url: Optional[str] = Field(
        default=None, description="URL to TTS audio (Phase 5; null until then)"
    )
