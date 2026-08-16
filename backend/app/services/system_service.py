"""System actions executed on the user's laptop.

Only pre-approved, safe-list actions live here. Every function returns a
consistent JSON dict: {"success": bool, "reply": str}. All OS interactions
are wrapped in try-except so one failure never crashes the backend.
"""

import datetime
import os
import platform
import re
import subprocess
import webbrowser
from urllib.parse import quote

SYSTEM = platform.system()  # "Windows" | "Darwin" | "Linux"

# Only plain app names are allowed when opening arbitrary apps: letters,
# digits, spaces, dots, dashes, underscores. No paths, no shell metacharacters.
_APP_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9 ._-]{0,49}$")

# Safe list of applications: keyword -> launch name per OS.
_APPS = {
    "notepad": {"Windows": "notepad", "Darwin": "TextEdit", "Linux": "gedit"},
    "calculator": {"Windows": "calc", "Darwin": "Calculator", "Linux": "gnome-calculator"},
    "paint": {"Windows": "mspaint", "Darwin": "Preview", "Linux": "gimp"},
    "cmd": {"Windows": "cmd", "Darwin": "Terminal", "Linux": "xterm"},
    "explorer": {"Windows": "explorer", "Darwin": "Finder", "Linux": "nautilus"},
    "chrome": {"Windows": "chrome", "Darwin": "Google Chrome", "Linux": "google-chrome"},
    "firefox": {"Windows": "firefox", "Darwin": "Firefox", "Linux": "firefox"},
    "edge": {"Windows": "msedge", "Darwin": "Microsoft Edge", "Linux": "microsoft-edge"},
}

# Safe list of websites: keyword -> URL.
_WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "wikipedia": "https://www.wikipedia.org",
    "github": "https://github.com",
    "stack overflow": "https://stackoverflow.com",
    "maps": "https://maps.google.com",
    "news": "https://news.google.com",
}


def _fail(action: str, name: str, error: Exception) -> dict:
    """Log the error and return a friendly failure result."""
    print(f"[system] {action}({name}) failed: {error}")
    return {"success": False, "reply": f"Sorry, I couldn't {action} {name}."}


def open_app(name: str) -> dict:
    """Launch an application.

    Known safe-list apps use the per-OS map; any other name is passed to the
    OS launcher after validation (Windows App Paths / macOS 'open -a'), so
    installed apps like Spotify work without being enumerated here.
    """
    key = name.lower()
    try:
        if key in _APPS:
            if SYSTEM == "Windows":
                os.startfile(_APPS[key]["Windows"])
            elif SYSTEM == "Darwin":
                subprocess.Popen(["open", "-a", _APPS[key]["Darwin"]])
            else:
                subprocess.Popen([_APPS[key]["Linux"]])
            return {"success": True, "reply": f"Opening {key}."}

        # Generic: open any installed app by name (validated first).
        if not _APP_NAME_RE.match(name):
            return {
                "success": False,
                "reply": f"I can't open '{name}' - that doesn't look like an app name.",
            }
        if SYSTEM == "Windows":
            os.startfile(name)
        elif SYSTEM == "Darwin":
            subprocess.Popen(["open", "-a", name])
        else:
            return {
                "success": False,
                "reply": f"On Linux I can only open apps from my known list ({', '.join(_APPS)}).",
            }
        return {"success": True, "reply": f"Opening {name}."}
    except OSError:
        return {
            "success": False,
            "reply": f"I couldn't find an app called '{name}' on this computer.",
        }
    except Exception as e:  # noqa: BLE001 - system actions must never crash the app
        return _fail("open", name, e)


def open_website(key: str) -> dict:
    """Open a pre-approved website by keyword."""
    try:
        if not webbrowser.open(_WEBSITES[key]):
            raise RuntimeError("webbrowser.open returned False")
        return {"success": True, "reply": f"Opening {key}."}
    except KeyError:
        return {"success": False, "reply": f"I don't know the website '{key}'."}
    except Exception as e:  # noqa: BLE001
        return _fail("open", key, e)


def open_target(name: str) -> dict:
    """Open a website or app by keyword ('open youtube', 'open chrome').

    Websites and known apps are matched by keyword; anything else is treated
    as an installed app name and passed to the validated generic opener.
    """
    key = name.lower()
    if key in _WEBSITES:
        return open_website(key)
    return open_app(name)


def search_google(query: str) -> dict:
    """Search Google for a query."""
    try:
        url = f"https://www.google.com/search?q={quote(query)}"
        if not webbrowser.open(url):
            raise RuntimeError("webbrowser.open returned False")
        return {"success": True, "reply": f"Searching Google for '{query}'."}
    except Exception as e:  # noqa: BLE001
        return _fail("search Google for", query, e)


def search_youtube(query: str, action: str = "search") -> dict:
    """Search YouTube for a query; used for 'search youtube' and 'play'."""
    try:
        url = f"https://www.youtube.com/results?search_query={quote(query)}"
        if not webbrowser.open(url):
            raise RuntimeError("webbrowser.open returned False")
        reply = (
            f"Playing '{query}' on YouTube."
            if action == "play"
            else f"Searching YouTube for '{query}'."
        )
        return {"success": True, "reply": reply}
    except Exception as e:  # noqa: BLE001
        return _fail("play", query, e)


def search_wikipedia(query: str) -> dict:
    """Search Wikipedia for a query."""
    try:
        url = f"https://en.wikipedia.org/wiki/Special:Search?search={quote(query)}"
        if not webbrowser.open(url):
            raise RuntimeError("webbrowser.open returned False")
        return {"success": True, "reply": f"Searching Wikipedia for '{query}'."}
    except Exception as e:  # noqa: BLE001
        return _fail("search Wikipedia for", query, e)


def tell_time() -> dict:
    """Return the current time."""
    now = datetime.datetime.now()
    return {"success": True, "reply": f"The time is {now:%I:%M %p}."}


def tell_date() -> dict:
    """Return today's date."""
    now = datetime.datetime.now()
    return {"success": True, "reply": f"Today is {now:%A, %d %B %Y}."}
