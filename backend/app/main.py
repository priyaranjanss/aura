"""AURA backend entrypoint (FastAPI).

Phase 1: serves a health/hello endpoint and enables CORS for the React
frontend running on http://localhost:5173.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.chat import router as chat_router

app = FastAPI(
    title="AURA Backend",
    description="Advanced Universal Response Assistant - local backend",
    version="0.1.0",
)

# Allow the Vite dev server to talk to the backend during development.
# Any origin is accepted because the backend binds to 127.0.0.1 only, so
# only pages on this machine can reach it (dev convenience, no credentials).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)

# Serve generated TTS audio (backend/static).
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def root():
    """Basic health check - Phase 1 requirement."""
    return {"status": "online", "message": "Hello from AURA"}
