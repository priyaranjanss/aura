"""AURA backend configuration.

Loads settings from the .env file located next to this project's backend
folder so secrets (like the AI API key) stay out of the codebase.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# backend/ directory (parent of app/)
BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")

# --- Server ---
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8001"))

# --- AI provider (provider-agnostic "AI brain") ---
# AI_PROVIDER selects the backend: "gemini" (default), "openai", "ollama".
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()
# AI_API_KEY is the generic key; GEMINI_API_KEY is kept as a legacy alias.
AI_API_KEY = os.getenv("AI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
# Empty -> provider's default model.
AI_MODEL = os.getenv("AI_MODEL", "")
