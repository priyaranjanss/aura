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

# Remembers the last browser used, so a follow-up in the same browser can
# navigate the CURRENT tab instead of spawning a new one.
_last_browser = ""

# Window-title fragments used to find a running browser (pygetwindow).
_BROWSER_TITLES = {
    "brave": "Brave",
    "chrome": "Chrome",
    "firefox": "Firefox",
    "edge": "Edge",
    "microsoft edge": "Edge",
}

# Only plain app names are allowed when opening arbitrary apps: letters,
# digits, spaces, dots, dashes, underscores. No paths, no shell metacharacters.
_APP_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9 ._-]{0,49}$")

# Only http(s) URLs are allowed when opening a raw link (no javascript:, file:, etc.)
_URL_RE = re.compile(r"^https?://[^\s]+$")

# Only printable ASCII is typed into apps (no control chars, no hotkeys).
_TEXT_RE = re.compile(r"^[\x20-\x7E]+$")


def _is_safe_url(value: str) -> bool:
    return bool(_URL_RE.match(value))

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
    return {
        "success": False,
        "reply": f"Sorry, I couldn't {action} {name}.",
        "analysis": {"what": f"Attempt to {action} '{name}'"},
    }


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
            return {
                "success": True,
                "reply": f"Opened {key}.",
                "analysis": {
                    "what": f"Open the '{key}' application",
                    "how": "Launch via the operating system's app launcher",
                },
            }

        # Generic: open any installed app by name (validated first).
        if not _APP_NAME_RE.match(name):
            return {
                "success": False,
                "reply": f"I can't open '{name}' - that doesn't look like an app name.",
                "analysis": {"what": f"Open '{name}'", "how": "Rejected: invalid app name"},
            }
        if SYSTEM == "Windows":
            os.startfile(name)
        elif SYSTEM == "Darwin":
            subprocess.Popen(["open", "-a", name])
        else:
            return {
                "success": False,
                "reply": f"On Linux I can only open apps from my known list ({', '.join(_APPS)}).",
                "analysis": {"what": f"Open '{name}'", "how": "Linux launcher not available"},
            }
        return {
            "success": True,
            "reply": f"Opened {name}.",
            "analysis": {
                "what": f"Open the '{name}' application",
                "how": "Launch via the operating system's app launcher",
            },
        }
    except OSError:
        return {
            "success": False,
            "reply": f"I couldn't find an app called '{name}' on this computer.",
            "analysis": {"what": f"Open '{name}'", "how": "App not found on this computer"},
        }
    except Exception as e:  # noqa: BLE001 - system actions must never crash the app
        return _fail("open", name, e)


def open_website(key: str) -> dict:
    """Open a website by keyword (safe list) or a plain http(s) URL."""
    try:
        # Known keyword -> mapped URL; otherwise a validated http(s) URL.
        if key.lower() in _WEBSITES:
            url = _WEBSITES[key.lower()]
        elif _is_safe_url(key):
            url = key
        else:
            return {
                "success": False,
                "reply": f"I don't know the website '{key}'.",
                "analysis": {"what": f"Open website '{key}'", "how": "Unknown website"},
            }
        if not webbrowser.open(url):
            raise RuntimeError("webbrowser.open returned False")
        return {
            "success": True,
            "reply": f"Opened {key}.",
            "analysis": {
                "what": f"Open the '{key}' website",
                "how": "Open the URL in the default browser",
                "where": url,
            },
        }
    except Exception as e:  # noqa: BLE001
        return _fail("open", key, e)


def _app_exe_path(exe_name: str):
    """Resolve an installed app's full path via the Windows App Paths registry."""
    try:
        import winreg  # Windows only
    except ImportError:
        return None
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{exe_name}",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "")
            return value
    except OSError:
        return None


def _navigate_current_tab(url: str, browser: str) -> bool:
    """Navigate the CURRENT tab of a running browser via Ctrl+L + URL + Enter."""
    title = _BROWSER_TITLES.get(browser.lower())
    if not title:
        return False
    try:
        import time

        import pyautogui  # lazy import

        windows = pyautogui.getWindowsWithTitle(title)
        if not windows:
            return False
        windows[0].activate()
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.3)
        pyautogui.typewrite(url, interval=0.01)
        pyautogui.press("enter")
        return True
    except Exception:  # noqa: BLE001 - best effort; fall back to a new tab
        return False


def _open_url_with_browser(url: str, browser: str) -> str:
    """Open a URL with a browser.

    Returns "tab" (navigated the current tab), "new" (launched the browser
    with the URL), or "" (failed). Same-browser follow-ups reuse the current
    tab; a first open (or a different browser) launches a fresh tab.
    """
    browser = browser.lower()
    global _last_browser

    if _last_browser == browser and _navigate_current_tab(url, browser):
        _last_browser = browser
        return "tab"

    try:
        if SYSTEM == "Windows":
            exe = _app_exe_path(f"{browser}.exe")
            if exe:
                subprocess.Popen([exe, url])
                _last_browser = browser
                return "new"
        names = {
            "chrome": "google-chrome",
            "firefox": "firefox",
            "edge": "edge",
            "microsoft edge": "edge",
            "brave": "brave",
        }
        registered = names.get(browser)
        if registered:
            try:
                webbrowser.get(registered).open(url)
                _last_browser = browser
                return "new"
            except webbrowser.Error:
                pass
    except Exception:
        pass
    return ""


def open_website_in_browser(key: str, browser: str) -> dict:
    """Open a safe-list website in a specific browser ('open youtube in brave')."""
    key = key.lower()
    browser = browser.lower()
    if key not in _WEBSITES:
        return {
            "success": False,
            "reply": f"I don't know the website '{key}'.",
            "analysis": {"what": f"Open '{key}' in {browser}", "how": "Unknown website"},
        }
    url = _WEBSITES[key]
    try:
        mode = _open_url_with_browser(url, browser)
        if mode:
            same_tab = " (same tab)" if mode == "tab" else ""
            return {
                "success": True,
                "reply": f"Opened {key} in {browser}.{same_tab}",
                "analysis": {
                    "what": f"Open the '{key}' website in {browser}",
                    "how": "Open the URL in the browser",
                    "where": url,
                },
            }
        webbrowser.open(url)  # fallback: default browser
        return {
            "success": True,
            "reply": f"Opened {key} in the default browser.",
            "analysis": {
                "what": f"Open the '{key}' website",
                "how": "Open the URL in the default browser",
                "where": url,
            },
        }
    except Exception as e:  # noqa: BLE001
        return _fail("open", f"{key} in {browser}", e)


def type_text(text: str, app: str = "") -> dict:
    """Type plain text into a window (pyautogui) — safe characters only.

    The app is usually inherited from context ("write hello" after opening
    Notepad). If the app's window can't be focused, we refuse rather than type
    into the wrong place.
    """
    if not _TEXT_RE.match(text) or len(text) > 300:
        return {
            "success": False,
            "reply": "I can only type plain text up to 300 characters (no special hotkeys).",
            "analysis": {"what": f"Type text into {app or 'the focused window'}", "how": "Rejected: unsafe text"},
        }
    try:
        import time

        import pyautogui  # lazy import

        if app and SYSTEM == "Windows":
            try:
                windows = pyautogui.getWindowsWithTitle(app)
                if not windows:
                    return {
                        "success": False,
                        "reply": f"I couldn't find the {app} window to type into.",
                        "analysis": {
                            "what": f"Type text into {app}",
                            "how": "App window not found",
                        },
                    }
                windows[0].activate()
            except Exception:  # noqa: BLE001 - best effort focus
                pass
        time.sleep(0.6)
        pyautogui.typewrite(text, interval=0.02)
        target = app or "the focused window"
        return {
            "success": True,
            "reply": f"Typed \"{text}\" into {target}.",
            "analysis": {
                "what": f"Type text into {target}",
                "how": "Send keystrokes to the focused window (pyautogui)",
            },
        }
    except ImportError:
        return {
            "success": False,
            "reply": "Typing isn't available yet - the pyautogui package is missing.",
            "analysis": {"what": "Type text", "how": "pyautogui not installed"},
        }
    except Exception as e:  # noqa: BLE001
        return _fail("type into", app or "focused window", e)


def close_app(name: str) -> dict:
    """Close a running application by name (graceful quit, no force-kill)."""
    if not _APP_NAME_RE.match(name):
        return {
            "success": False,
            "reply": f"I can't close '{name}' - that doesn't look like an app name.",
            "analysis": {"what": f"Close '{name}'", "how": "Rejected: invalid app name"},
        }
    try:
        if SYSTEM == "Windows":
            result = subprocess.run(
                ["taskkill", "/IM", f"{name}.exe"], capture_output=True, timeout=20
            )
        elif SYSTEM == "Darwin":
            result = subprocess.run(
                ["osascript", "-e", f'quit app "{name}"'],
                capture_output=True,
                timeout=20,
            )
        else:
            result = subprocess.run(
                ["pkill", "-x", name], capture_output=True, timeout=20
            )
        if result.returncode != 0:
            return {
                "success": False,
                "reply": f"I couldn't close {name} - it may not be running.",
                "analysis": {
                    "what": f"Close the '{name}' application",
                    "how": "App not running or couldn't be closed",
                },
            }
        return {
            "success": True,
            "reply": f"Closed {name}.",
            "analysis": {
                "what": f"Close the '{name}' application",
                "how": "Request a graceful quit via the OS",
            },
        }
    except Exception as e:  # noqa: BLE001
        return _fail("close", name, e)


def _minimize_windows_process(exe_name: str, display_name: str = "") -> bool:
    """Minimize every visible top-level window of an app (Windows).

    Two matching strategies, so both classic and UWP (Store) apps work:
    - Process image name prefix match ("notepad" -> notepad.exe,
      "calc" -> CalculatorApp.exe).
    - ApplicationFrameHost windows by title (UWP apps like Calculator host
      their visible window in ApplicationFrameHost.exe, whose title is the
      app name).
    Returns True if at least one window was minimized.
    """
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        SW_MINIMIZE = 6
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        wanted = exe_name.lower()
        wanted_title = display_name.strip().lower()

        targets = []
        found = []

        WNDENUMPROC = ctypes.WINFUNCTYPE(
            wintypes.BOOL, wintypes.HWND, wintypes.LPARAM
        )
        user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
        user32.GetWindowThreadProcessId.argtypes = [
            wintypes.HWND, ctypes.POINTER(wintypes.DWORD)
        ]
        kernel32.OpenProcess.argtypes = [
            wintypes.DWORD, wintypes.BOOL, wintypes.DWORD
        ]
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.QueryFullProcessImageNameW.argtypes = [
            wintypes.HANDLE, wintypes.DWORD,
            wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD),
        ]

        @WNDENUMPROC
        def callback(hwnd, _lparam):
            found.append(hwnd)
            return True

        user32.EnumWindows(callback, 0)

        for hwnd in found:
            if not user32.IsWindowVisible(hwnd):
                continue
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            handle = kernel32.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value
            )
            if not handle:
                continue
            try:
                size = wintypes.DWORD(512)
                buf = ctypes.create_unicode_buffer(512)
                if kernel32.QueryFullProcessImageNameW(
                    handle, 0, buf, ctypes.byref(size)
                ):
                    exe = buf.value.rsplit("\\", 1)[-1].lower()
                    if exe == f"{wanted}.exe" or exe.startswith(wanted):
                        targets.append(hwnd)
                        continue
                    # UWP apps: the visible window lives in the frame host.
                    if wanted_title and exe == "applicationframehost.exe":
                        title = ctypes.create_unicode_buffer(512)
                        user32.GetWindowTextW(hwnd, title, 512)
                        if wanted_title in title.value.lower():
                            targets.append(hwnd)
            finally:
                kernel32.CloseHandle(handle)

        for hwnd in targets:
            user32.ShowWindow(hwnd, SW_MINIMIZE)
        return bool(targets)
    except Exception:  # noqa: BLE001 - best effort
        return False


def minimize_app(name: str) -> dict:
    """Minimize (not close) a running application's window."""
    if not _APP_NAME_RE.match(name):
        return {
            "success": False,
            "reply": f"I can't minimize '{name}' - that doesn't look like an app name.",
            "analysis": {"what": f"Minimize '{name}'", "how": "Rejected: invalid app name"},
        }
    try:
        if SYSTEM == "Windows":
            # 1) Reliable path: minimize by process name (own ctypes
            #    implementation). pygetwindow 0.0.9 is flaky on 64-bit
            #    Python 3.13+ (intermittent WinFunctionType TypeError), so it
            #    is only a last-resort fallback below. Also try the known-app
            #    launcher name ("minimize calculator" -> calc.exe).
            candidates = {name.lower()}
            key = name.lower()
            if key in _APPS:
                candidates.add(_APPS[key]["Windows"].lower())
            for candidate in candidates:
                if _minimize_windows_process(candidate, display_name=name):
                    return {
                        "success": True,
                        "reply": f"Minimized {name}.",
                        "analysis": {
                            "what": f"Minimize the '{name}' application",
                            "how": "Minimize the app's window via the OS",
                        },
                    }
            # 2) Best-effort fallback: title matching via pygetwindow
            #    (bundled with pyautogui). Fully wrapped because it can raise
            #    intermittently on newer Pythons.
            try:
                import pyautogui

                windows = pyautogui.getWindowsWithTitle(name)
                for window in windows:
                    try:
                        window.minimize()
                    except Exception:  # noqa: BLE001
                        pass
                if windows:
                    return {
                        "success": True,
                        "reply": f"Minimized {name}.",
                        "analysis": {
                            "what": f"Minimize the '{name}' application",
                            "how": "Minimize the app's window via the OS",
                        },
                    }
            except Exception:  # noqa: BLE001 - pygetwindow can crash; ignore
                pass
            return {
                "success": False,
                "reply": f"I couldn't find the {name} window to minimize.",
                "analysis": {
                    "what": f"Minimize the '{name}' application",
                    "how": "App window not found",
                },
            }
        if SYSTEM == "Darwin":
            result = subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'tell application "System Events" to tell process "{name}" '
                    "to set miniaturized of every window to true",
                ],
                capture_output=True,
                timeout=20,
            )
            if result.returncode != 0:
                return {
                    "success": False,
                    "reply": f"I couldn't find the {name} window to minimize.",
                    "analysis": {"what": f"Minimize '{name}'", "how": "App window not found"},
                }
            return {
                "success": True,
                "reply": f"Minimized {name}.",
                "analysis": {"what": f"Minimize the '{name}' application", "how": "Minimize via AppleScript"},
            }
        return {
            "success": False,
            "reply": "Minimizing apps isn't supported on Linux yet.",
            "analysis": {"what": f"Minimize '{name}'", "how": "Not supported on Linux"},
        }
    except Exception as e:  # noqa: BLE001
        return _fail("minimize", name, e)


def open_target(name: str) -> dict:
    """Open a website or app by keyword ('open youtube', 'open chrome').

    Websites and known apps are matched by keyword; anything else is treated
    as an installed app name and passed to the validated generic opener.
    """
    key = name.lower()
    if key in _WEBSITES:
        return open_website(key)
    return open_app(name)


def search_google(query: str, browser: str = "") -> dict:
    """Search Google for a query (optionally in a specific browser)."""
    try:
        url = f"https://www.google.com/search?q={quote(query)}"
        mode = _open_url_with_browser(url, browser) if browser else ""
        if not mode and not webbrowser.open(url):
            raise RuntimeError("webbrowser.open returned False")
        reply = f"Searched Google for '{query}'."
        if browser:
            reply = f"Searched Google for '{query}' in {browser}."
        if mode == "tab":
            reply += " (same tab)"
        return {
            "success": True,
            "reply": reply,
            "analysis": {
                "what": f"Search Google for '{query}'",
                "how": "Open the Google search URL in the browser",
            },
        }
    except Exception as e:  # noqa: BLE001
        return _fail("search Google for", query, e)


def search_youtube(query: str, action: str = "search", browser: str = "") -> dict:
    """Search YouTube for a query; used for 'search youtube' and 'play'."""
    try:
        url = f"https://www.youtube.com/results?search_query={quote(query)}"
        mode = _open_url_with_browser(url, browser) if browser else ""
        if not mode and not webbrowser.open(url):
            raise RuntimeError("webbrowser.open returned False")
        playing = action == "play"
        if playing:
            reply = f"Played '{query}' on YouTube."
        else:
            reply = f"Searched YouTube for '{query}'."
        if browser:
            reply = f"{reply} (in {browser})"
        if mode == "tab":
            reply += " (same tab)"
        return {
            "success": True,
            "reply": reply,
            "analysis": {
                "what": f"{'Play' if playing else 'Search YouTube for'} '{query}'",
                "how": "Open the YouTube search results in the browser",
            },
        }
    except Exception as e:  # noqa: BLE001
        return _fail("play", query, e)


def search_wikipedia(query: str) -> dict:
    """Search Wikipedia for a query."""
    try:
        url = f"https://en.wikipedia.org/wiki/Special:Search?search={quote(query)}"
        if not webbrowser.open(url):
            raise RuntimeError("webbrowser.open returned False")
        return {
            "success": True,
            "reply": f"Searched Wikipedia for '{query}'.",
            "analysis": {
                "what": f"Search Wikipedia for '{query}'",
                "how": "Open the Wikipedia search URL in the default browser",
            },
        }
    except Exception as e:  # noqa: BLE001
        return _fail("search Wikipedia for", query, e)


def tell_time() -> dict:
    """Return the current time."""
    now = datetime.datetime.now()
    return {
        "success": True,
        "reply": f"The time is {now:%I:%M %p}.",
        "analysis": {"what": "Tell the current time", "how": "Read the system clock"},
    }


def tell_date() -> dict:
    """Return today's date."""
    now = datetime.datetime.now()
    return {
        "success": True,
        "reply": f"Today is {now:%A, %d %B %Y}.",
        "analysis": {"what": "Tell today's date", "how": "Read the system clock"},
    }
