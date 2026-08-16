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
    "volume_up",
    "volume_down",
    "mute_volume",
    "take_screenshot",
    "lock_computer",
    "shutdown_computer",
    "restart_computer",
}

# Dangerous actions: the user must confirm them in the UI before they run.
DANGEROUS_ACTIONS = {"lock_computer", "shutdown_computer", "restart_computer"}

# Keyword hints that map to dangerous actions (used by the offline fallback).
_DANGEROUS_HINTS = [
    (re.compile(r"\b(lock|lock the computer|lock screen|lock my computer)\b"), "lock_computer"),
    (re.compile(r"\b(shutdown|shut down|turn off|power off|switch off)\b"), "shutdown_computer"),
    (re.compile(r"\b(restart|reboot|reset the computer)\b"), "restart_computer"),
]


def dangerous_action_in_steps(steps: list):
    """Return the first dangerous action name in a list of steps, or None."""
    if not isinstance(steps, list):
        return None
    for step in steps:
        if isinstance(step, dict):
            action = str(step.get("action", "")).strip().lower()
            if action in DANGEROUS_ACTIONS:
                return action
    return None


def dangerous_action_in_message(message: str):
    """Return the dangerous action hinted by a message, or None."""
    msg = message.lower()
    for pattern, action in _DANGEROUS_HINTS:
        if pattern.search(msg):
            return action
    return None

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
    if action == "volume_up":
        return system_service.volume_up()
    if action == "volume_down":
        return system_service.volume_down()
    if action == "mute_volume":
        return system_service.mute_volume()
    if action == "take_screenshot":
        return system_service.take_screenshot()
    if action == "lock_computer":
        return system_service.lock_computer()
    if action == "shutdown_computer":
        return system_service.shutdown_computer()
    if action == "restart_computer":
        return system_service.restart_computer()
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

    # --- Volume ("volume up", "increase volume", "mute") ----------------
    if re.search(r"(volume|sound)\s+(up|increase|raise|louder)|(increase|raise|turn\s+up)\s+(the\s+)?(volume|sound)", msg):
        return system_service.volume_up()
    if re.search(r"(volume|sound)\s+(down|decrease|lower|quieter)|(decrease|lower|turn\s+down)\s+(the\s+)?(volume|sound)", msg):
        return system_service.volume_down()
    if re.search(r"\b(mute|unmute)\b", msg):
        return system_service.mute_volume()

    # --- Screenshot ("take screenshot", "capture the screen") ----------
    if re.search(r"(take|capture|save|grab)\s+(a\s+)?(screenshot|screen\s+shot|screen\s+capture)", msg) or msg in {"screenshot", "screen shot"}:
        return system_service.take_screenshot()

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
