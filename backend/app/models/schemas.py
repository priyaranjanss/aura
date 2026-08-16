"""Pydantic request/response models for the AURA chat API."""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

# Every reply leads with an analysis covering all question dimensions.
# Fields that don't apply are answered with "Not needed".
ANALYSIS_QUESTIONS = [
    "What",
    "When",
    "Who",
    "How",
    "Where",
    "Why",
    "Which",
    "Whose",
    "Whom",
    "How much",
]


def build_analysis(answers: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    """Build the full question analysis, defaulting unneeded fields."""
    answers = answers or {}
    return [
        {"question": question, "answer": str(answers.get(question.lower(), "Not needed"))}
        for question in ANALYSIS_QUESTIONS
    ]


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
    confirm: bool = Field(
        default=False,
        description="True when the user confirmed a dangerous action (lock/shutdown/restart)",
    )
    lang: str = Field(
        default="en", description="TTS language: 'en' or 'hi'"
    )


class ChatResponse(BaseModel):
    """Response returned by POST /api/chat."""

    reply: str = Field(..., description="Assistant's text reply")
    type: Literal["command", "ai", "error", "confirm"] = Field(
        "ai", description="Reply type: system command, AI answer, error, or confirmation prompt"
    )
    success: bool = True
    audio_url: Optional[str] = Field(
        default=None, description="URL to TTS audio (Phase 5; null until then)"
    )
    requires_confirmation: bool = Field(
        default=False,
        description="True when the user must confirm a dangerous action before it runs",
    )
    image_url: Optional[str] = Field(
        default=None, description="URL to an image the command produced (e.g. a screenshot)"
    )
    analysis: List[Dict[str, str]] = Field(
        default_factory=build_analysis,
        description=(
            "Request analysis shown before the reply: What/When/Who/How/Where/... "
            "each answered or 'Not needed'"
        ),
    )
