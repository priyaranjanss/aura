"""AURA backend entrypoint (FastAPI).

Phase 1: serves a health/hello endpoint and enables CORS for the React
frontend running on http://localhost:5173.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AURA Backend",
    description="Advanced Universal Response Assistant - local backend",
    version="0.1.0",
)

# Allow the Vite dev server to talk to the backend during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Basic health check - Phase 1 requirement."""
    return {"status": "online", "message": "Hello from AURA"}
