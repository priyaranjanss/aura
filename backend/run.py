"""Convenience launcher for the AURA backend.

Usage (from the backend/ folder, with the venv active):
    python run.py
"""

import uvicorn

from app import config

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
    )
