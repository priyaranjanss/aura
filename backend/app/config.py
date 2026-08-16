"""AURA backend configuration.

Loads settings from the .env file located next to this project's backend
folder so secrets (like the Gemini API key) stay out of the codebase.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# backend/ directory (parent of app/)
BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8001"))
