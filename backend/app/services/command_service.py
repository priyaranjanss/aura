"""Intent detection: decides whether a message is a system command.

Phase 3: simple keyword/regex matching against the safe list of commands.
Messages that are not commands return None so the chat route falls back to
conversation (Gemini in Phase 4).
"""

import re

from app.services import system_service


def handle(message: str):
    """Return a command result dict, or None if the message isn't a command."""
    msg = message.strip().lower()

    # --- Time & date ---------------------------------------------------
    if re.search(r"(what|current|tell)[^.]{0,15}time", msg) or msg in {"time", "the time"}:
        return system_service.tell_time()
    if re.search(r"(what|current|today)[^.]{0,15}date", msg) or msg in {"date", "today's date"}:
        return system_service.tell_date()

    # --- Open something ("open chrome", "open youtube", "open the calculator") ---
    m = re.match(r"^(?:please\s+)?open\s+(.+)$", msg)
    if m:
        target = m.group(1).strip()
        if target.startswith("the "):
            target = target[4:].strip()
        return system_service.open_target(target)

    # --- Search Google ("search google for cats", "google search cats", "google cats") ---
    m = re.search(r"search\s+google\s+for\s+(.+)$", msg)
    if m:
        return system_service.search_google(m.group(1).strip())
    m = re.match(r"^google\s+(?:search\s+)?(.+)$", msg)
    if m:
        return system_service.search_google(m.group(1).strip())

    # --- Search YouTube ("search youtube for X") ------------------------
    m = re.search(r"search\s+youtube\s+for\s+(.+)$", msg)
    if m:
        return system_service.search_youtube(m.group(1).strip())

    # --- Search Wikipedia ("search wikipedia for X", "wikipedia X") -----
    m = re.search(r"search\s+wikipedia\s+for\s+(.+)$", msg)
    if m:
        return system_service.search_wikipedia(m.group(1).strip())

    # --- Music on YouTube ("play music", "play despacito", "play X on youtube") ---
    if re.match(r"^play\s+(music|song)(\s+on\s+youtube)?$", msg):
        return system_service.search_youtube("music", action="play")
    m = re.match(r"^play\s+(.+?)\s+on\s+youtube$", msg)
    if m:
        return system_service.search_youtube(m.group(1).strip(), action="play")
    if msg.startswith("play "):
        return system_service.search_youtube(msg[5:].strip(), action="play")

    # Not a command -> let the conversation handler (Gemini, Phase 4) reply.
    return None
