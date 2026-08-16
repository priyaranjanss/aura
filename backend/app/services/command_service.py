"""Intent detection: decides whether a message is a system command.

Phase 3: simple keyword/regex matching against the safe list of commands.
Messages that are not commands return None so the chat route falls back to
conversation (AI service in Phase 4).
"""

import re

from app.services import system_service

# Actions the AI may suggest; anything else is refused (never executed).
_AI_ACTIONS = {
    "open_app",
    "close_app",
    "minimize_app",
    "type_text",
    "open_website",
    "open_website_in_browser",
    "search_google",
    "search_youtube",
    "search_wikipedia",
    "tell_time",
    "tell_date",
}

_BROWSERS = {"brave", "chrome", "firefox", "edge", "microsoft edge", "default", "default browser"}


def execute_ai_command(command: dict):
    """Validate an AI-suggested command and execute it (safe list only).

    Returns the command result dict, or None if the command is not in the
    allowed action set / has invalid parameters.
    """
    if not isinstance(command, dict):
        return None

    action = str(command.get("action", "")).strip().lower()
    if action not in _AI_ACTIONS:
        return None

    target = str(command.get("target", "")).strip()
    browser = str(command.get("browser", "")).strip().lower()
    # "Not needed" / empty -> default browser for search actions.
    if browser not in _BROWSERS:
        browser = ""

    if action == "open_app":
        return system_service.open_app(target)
    if action == "close_app":
        return system_service.close_app(target)
    if action == "minimize_app":
        target = target or str(command.get("app", "")).strip()
        return system_service.minimize_app(target)
    if action == "type_text":
        app = str(command.get("app", "")).strip()
        return system_service.type_text(target, app=app)
    if action == "open_website":
        return system_service.open_website(target)
    if action == "open_website_in_browser":
        if browser not in _BROWSERS:
            return None
        return system_service.open_website_in_browser(target, browser)
    if action == "search_google":
        return system_service.search_google(target, browser=browser)
    if action == "search_youtube":
        return system_service.search_youtube(target, browser=browser)
    if action == "search_wikipedia":
        return system_service.search_wikipedia(target, browser=browser)
    if action == "tell_time":
        return system_service.tell_time()
    if action == "tell_date":
        return system_service.tell_date()
    return None


def execute_ai_steps(steps: list):
    """Execute a list of AI-suggested commands in order (each validated).

    Compound requests like "open notepad and minimize it" become multiple
    steps. Each step is validated against the safe list; invalid steps are
    skipped. A short pause between steps lets the previous one finish
    (e.g. the window must exist before it can be minimized).
    """
    if not isinstance(steps, list):
        return []
    results = []
    for i, step in enumerate(steps):
        result = execute_ai_command(step)
        if result is not None:
            results.append(result)
            if i < len(steps) - 1:
                import time

                time.sleep(0.8)
    return results


def handle(message: str):
    """Return a command result dict, or None if the message isn't a command."""
    msg = message.strip().lower()

    # --- Type/write text ("write hello", "type hello world") ---
    m = re.match(r"^(?:please\s+)?(?:type|write)\s+(.+)$", msg)
    if m:
        return system_service.type_text(m.group(1).strip())

    # --- Close something ("close brave", "quit chrome", "exit edge") ---
    m = re.match(r"^(?:please\s+)?(?:close|quit|exit)\s+(.+)$", msg)
    if m:
        target = m.group(1).strip()
        if target.startswith("the "):
            target = target[4:].strip()
        return system_service.close_app(target)

    # --- Minimize something ("minimize notepad", "minimise brave") ---
    m = re.match(r"^(?:please\s+)?(?:minimize|minimise)\s+(.+)$", msg)
    if m:
        target = m.group(1).strip()
        if target.startswith("the "):
            target = target[4:].strip()
        return system_service.minimize_app(target)

    # --- Time & date ---------------------------------------------------
    if re.search(r"(what|current|tell)[^.]{0,15}time", msg) or msg in {"time", "the time"}:
        return system_service.tell_time()
    if re.search(r"(what|current|today)[^.]{0,15}date", msg) or msg in {"date", "today's date"}:
        return system_service.tell_date()

    # --- Open a website in a specific browser ("open youtube in brave") ---
    m = re.match(
        r"^(?:please\s+)?open\s+(.+?)\s+in\s+(brave|chrome|firefox|edge|microsoft edge|default browser)$",
        msg,
    )
    if m:
        return system_service.open_website_in_browser(
            m.group(1).strip(), m.group(2).strip()
        )

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

    # Not a command -> let the conversation handler (AI service, Phase 4) reply.
    return None
