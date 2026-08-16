"""Text-to-Speech via edge-tts (Microsoft Edge neural voices, free).

Generates an mp3 for a reply and returns its static URL (e.g.
/static/audio/<id>.mp3) or None if generation fails / text is too long.

Files are deleted after playback (the frontend calls DELETE /api/audio/<id>)
and old orphans are swept whenever a new file is generated, so the audio
folder stays clean.
"""

import asyncio
import re
import time
import uuid
from pathlib import Path

import edge_tts

# backend/static/audio — served by FastAPI's /static mount.
AUDIO_DIR = Path(__file__).resolve().parent.parent.parent / "static" / "audio"

# Generated files are <32 hex chars>.mp3 — only those can be deleted (no path
# traversal, no arbitrary files).
_AUDIO_NAME_RE = re.compile(r"^[0-9a-f]{32}\.mp3$")

# Files older than this are swept when a new file is generated (orphans left
# by tabs closed mid-playback, etc.).
MAX_AUDIO_AGE_SECONDS = 3600

# edge-tts voice names per language (English + Hindi for multilingual support).
VOICES = {
    "en": "en-US-AriaNeural",
    "hi": "hi-IN-SwaraNeural",
}

# Replies longer than this are not spoken (keeps demos snappy).
MAX_TTS_CHARS = 400


async def _generate(text: str, voice: str, out_path: Path) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out_path))


async def _generate_speech_async(text: str, lang: str = "en"):
    text = text.strip()
    if not text or len(text) > MAX_TTS_CHARS:
        return None
    try:
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        _sweep_old_audio()
        out_path = AUDIO_DIR / f"{uuid.uuid4().hex}.mp3"
        await _generate(text, VOICES.get(lang, VOICES["en"]), out_path)
        return f"/static/audio/{out_path.name}"
    except Exception as e:  # noqa: BLE001 - TTS must never break a reply
        print(f"[speech] tts failed: {e}")
        return None


def delete_audio(filename: str) -> bool:
    """Delete a generated audio file by name (strictly validated)."""
    if not _AUDIO_NAME_RE.match(filename):
        return False
    path = AUDIO_DIR / filename
    try:
        if path.is_file():
            path.unlink()
            return True
    except OSError as e:  # noqa: BLE001 - best effort
        print(f"[speech] delete failed: {e}")
    return False


def _sweep_old_audio() -> None:
    """Remove audio files older than MAX_AUDIO_AGE_SECONDS (best effort)."""
    try:
        now = time.time()
        for path in AUDIO_DIR.glob("*.mp3"):
            try:
                if now - path.stat().st_mtime > MAX_AUDIO_AGE_SECONDS:
                    path.unlink()
            except OSError:
                pass
    except OSError:
        pass


def generate_speech(text: str, lang: str = "en"):
    """Generate speech for a reply; returns a static URL or None.

    Sync wrapper around the async edge-tts call (runs its own event loop).
    """
    try:
        return asyncio.run(_generate_speech_async(text, lang))
    except Exception as e:  # noqa: BLE001
        print(f"[speech] tts failed: {e}")
        return None
