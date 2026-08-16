# AURA – Development Memory

Progress notes logged at the end of each phase (per docs/PHASES.md).

---

## Phase 1 – Foundation & Basic Shell ✅ (completed)

**Goal:** Project structure + basic working interface.

**Completed:**
- Created full folder structure per `docs/ARCHITECTURE.md` (frontend + backend)
- Backend: FastAPI app (`app/main.py`, `app/config.py`, package skeleton for
  `routes/`, `services/`, `models/`), `requirements.txt`, `.env`/`.env.example`,
  `run.py` convenience launcher, venv at `backend/venv`
  - `GET /` returns `{"status": "online", "message": "Hello from AURA"}`
  - CORS enabled for `http://localhost:5173`
- Frontend: Vite + React 18 + Tailwind CSS v3 (manual scaffold matching SETUP.md)
  - Design system colors from `docs/DESIGN.md` wired into `tailwind.config.js`
  - Layout: Sidebar (AURA branding + nav) + main chat area with AURA title,
    Idle status pill, empty chat state, and a text input box
- Root `.gitignore` (venv, `.env`, `node_modules`, `dist`, `__pycache__`)

**Verified:**
- Backend starts and `GET /` returns "Hello from AURA" (200 OK)
- Backend default port changed to **8001** (`.env`, `.env.example`, `config.py`, docs)
- Frontend builds with `npm run build` (no errors) and dev server serves on :5173

**Notes / next phase (Phase 2 – Dashboard & Core Chat):**
- Wire the input box to `POST /api/chat`
- Add `ChatWindow` / `ChatBubble` components, Zustand store, loading state
- Add `services/api.js` (axios) and `models/schemas.py`

---

## Phase 2 – Dashboard & Core Chat ✅ (completed)

**Goal:** Real conversation between frontend and backend.

**Completed:**
- Backend: `POST /api/chat` (models/schemas.py + routes/chat.py)
  - Pydantic validation (empty message -> 422), consistent JSON response
  - Placeholder reply logic (greeting + echo) — intent detection (Phase 3) and
    the AI service (Phase 4) plug into the same route later
- Frontend: axios service (`services/api.js`), Zustand store (`store/chatStore.js`)
  - `ChatBubble` (user right/indigo, assistant left/dark, error styling)
  - `ChatWindow` (empty welcome state, auto-scroll, "Thinking..." bubble)
  - `Home` rewired: send on Enter, send disabled while thinking, live status
    pill (Idle / Thinking...)
- Verified: curl POST /api/chat (greeting + echo + 422), `npm run build` passes,
  no emojis in frontend

**Notes / next phase (Phase 3 – System Commands):**
- Add `command_service.py` + `system_service.py` with keyword intent detection
- Route detected commands inside `routes/chat.py`, fall back to current reply
- Test: "open chrome", "open youtube", "what time is it"

---

## Phase 3 – System Commands ✅ (completed)

**Goal:** Make the assistant control the computer.

**Completed:**
- `services/command_service.py` — keyword/regex intent detection:
  - time/date, "open X" (apps + websites), "search google/youtube/wikipedia for X",
    "play music", "play X on youtube"
  - Returns `None` for non-commands so conversation (AI service, Phase 4) takes over
- `services/system_service.py` — safe-list OS actions (all try-except wrapped):
  - Apps: notepad, calculator, paint, cmd, explorer, chrome, firefox, edge (per-OS)
  - Websites: google, youtube, gmail, wikipedia, github, stack overflow, maps, news
  - Google / YouTube / Wikipedia search via webbrowser
  - Time + date
- `routes/chat.py` routes commands first; greetings/echo remain as conversation fallback

**Verified (live, opened real windows/tabs):**
- "what time is it" → "The time is 03:42 PM."
- "what is today's date" → "Today is Sunday, 16 August 2026."
- "search google for cats" → Google search tab
- "open youtube" → youtube.com
- "open notepad" / "open chrome" → apps opened
- "open spotify" → friendly "no shortcut" message (success=false)
- "hello" / non-commands → conversation fallback

**Notes / next phase (Phase 4 – AI Integration):**
- Hook the AI service into the conversation fallback in `routes/chat.py` via `ai_service.py`
- Send history for context; handle missing/invalid API key gracefully

**Improvement (same day): generic app opening**
- `system_service.open_app` now opens ANY installed app by name (validated:
  letters/digits/spaces only; paths & shell metachars rejected). Known apps
  still use the per-OS map; others go to the OS launcher (`os.startfile` on
  Windows, `open -a` on macOS). Verified: "open snippingtool" opens it;
  "open ../../evil" and "open calc & del *" are rejected.
- The real "brain" (AI intent detection) lands in Phase 4 — the AI decides
  the action, code still executes it (per RULES.md safety boundary).

---

## Phase 4 – AI Integration ✅ (completed)

**Goal:** Intelligent conversation via the AI service.

**Completed:**
- Provider switched to **groq** (`AI_PROVIDER=groq` in `.env`); added
  `GroqProvider` to `ai_service.py` (OpenAI-compatible endpoint
  https://api.groq.com/openai/v1/chat/completions, default model
  `llama-3.3-70b-versatile`). `requests` added to requirements.
- `ai_service.generate_reply()` now returns structured `{reply, analysis}`:
  shared SYSTEM_PROMPT asks the model to answer What/When/Who/How/Where/Why/
  Which/Whose/Whom/How much ("Not needed" when N/A) then the final reply as
  strict JSON; `_parse_structured()` handles clean/fenced/embedded JSON with a
  plain-text fallback.
- `routes/chat.py`: non-command messages go to the AI service; failures return
  a friendly `type: "error"` reply (verified live: empty key -> friendly
  message, commands unaffected). AI's own analysis is used when valid.
- Frontend: replies with `success: false` render with error styling.

**Verified:** provider selection, JSON parsing (clean/fenced/messy/fallback),
no-key error path, commands still work, `npm run build` passes.

**Notes / next phase (Phase 5 – Voice Features):**
- Microphone button + Web Speech API (STT) in the frontend
- edge-tts (TTS) via `speech_service.py`; play audio reply automatically
- Live status pill: Listening (green) / Thinking (amber) / Speaking (indigo)

**Gotcha (hit twice):** uvicorn's `--reload` watches `.py` files only — `.env`
changes (API key) are NOT picked up. Always restart the backend manually after
editing `.env` (`Ctrl+C` → `python run.py`).

**Added (same day):** "open <website> in <browser>" — e.g. "open youtube in
brave". Uses Windows App Paths (`winreg`) to find the browser exe, falls back
to registered webbrowser names, then the default browser. Verified live.

**Added (same day):** close_app — "close brave" / "quit chrome" / "exit edge".
Graceful quit (Windows `taskkill /IM`, macOS osascript, Linux pkill), validated
name, friendly "not running" message. Verified: open+close notepad cycle;
AI recognized "please quit notepad".

**Context across turns (same day):** the system prompt now instructs the AI to
use conversation history for follow-ups, for ANY app/site — not just browsers.
After opening an app, "write X" → `type_text`, "close" → `close_app` (target
inherited). New `type_text` action (pyautogui): safe printable-ASCII text only,
max 300 chars, focuses the app window before typing. Verified end-to-end:
open notepad → "write hello" typed into Notepad → "close" closed it.
Search actions accept an optional validated `browser`; open youtube in brave →
"search arijit singh" opened YouTube search in Brave.

**Environment gotcha:** the dev server may run on the SYSTEM Python, not the
venv (`python run.py` without activating the venv). Dependencies must exist in
whichever Python runs the server — installed pyautogui into the system Python
too.

**Multi-step commands (same day):** the AI now returns a `steps` array (one
object per action) instead of a single command, so compound requests work:
"open notepad and minimize it" → [open_app notepad, minimize_app notepad],
executed in order with a 0.8s pause. New `minimize_app` action: Windows via
ctypes EnumWindows (process-name prefix match, plus ApplicationFrameHost
by-title match for UWP apps like Calculator; pygetwindow 0.0.9 is flaky on
64-bit Python 3.13+ with an intermittent WinFunctionType TypeError, so it is
only a last-resort fallback), macOS via AppleScript. Keyword fallback also got
"minimize/minimise X". Verified: open notepad and minimize it → "Opening
notepad. Minimizing notepad." (live), minimize notepad + minimize calculator
5/5 stable.

## Phase 5 – Voice Features ✅ (completed)

**Goal:** Full voice interaction (speak to AURA, it speaks back).

**Completed:**
- Frontend STT: `hooks/useSpeech.js` (Web Speech API), `MicrophoneButton.jsx`
  (pulsing green while listening). Mic wired in `Home.jsx`; transcript is shown
  in the input and sent; text input still works if the mic is blocked.
- Backend TTS: `services/speech_service.py` (edge-tts, free neural voices),
  audio saved to `backend/static/audio/` and served via `/static` mount;
  `audio_url` attached to every chat reply (`_with_audio` helper), capped at
  400 chars, graceful None on failure. `edge-tts` installed in venv AND system
  python (server runs on system python).
- Status pill: Listening (green) / Thinking (amber) / Speaking (indigo) / Idle.
  Store auto-plays `audio_url` and sets Speaking while it plays.
- Verified: TTS generates mp3 (39KB), too-long text -> None, chat reply
  includes audio_url, GET /static/audio/*.mp3 -> 200 audio/mpeg, frontend builds.

**Wake word + sleep (same day, Phase 5 bonus):** a **Wake** toggle in the input
bar enables continuous listening (Web Speech API, `continuous: true`,
interimResults). While "Sleeping", AURA waits for a wake phrase — "Hello"
(or "Hello AURA", "Hey", "Hi", "Hey AURA", "Okay AURA"); on wake it
listens for the next utterance (final result only, wake phrase stripped) as
the command, then sleeps again after ~8s of idle (waits for
thinking/speaking to finish). Mic is held open the whole time wake mode is
on. Browser dropping the mic is handled with an auto-restart.

**Notes / next phase (Phase 6 – Advanced UI & Polish):**
- Quick command buttons, Settings panel, Clear Chat button
- Volume control + screenshot (pyautogui), confirmation for dangerous actions
- Multilingual, animations, demo script

---

**Same-tab browsing (same day):** launching a browser with a URL always opens a
new tab. Follow-ups in the SAME browser now navigate the current tab instead:
`_open_url_with_browser` tracks the last browser used and, on a same-browser
follow-up, sends Ctrl+L + URL + Enter (pyautogui) to the running browser
window. First open / different browser still opens a new tab. Verified:
"open youtube in brave" → "search for arijit singh" → "(same tab)". Caveat:
`_last_browser` is in-memory (resets on server restart); the active tab in the
browser window is the one that gets navigated.

## AI-first intent detection (same day)

- EVERY message now goes to the AI brain first (any phrasing). The AI returns
  `{analysis, command, reply}` where command = `{action, target, browser}`.
- `command_service.execute_ai_command()` validates the action against the
  allowlist (open_app, open_website, open_website_in_browser, search_*,
  tell_time/date) and sanitizes targets before executing.
- Keyword matching (`command_service.handle()`) remains as an offline fallback.
- Verified live: "launch chrome", "open youtube in brave", "whats the time now",
  "search the web for cute cats" all work; malicious AI intents (unknown action,
  path traversal, javascript: scheme, bad browser) are rejected.

---

## Feature: request analysis on every reply (2026-08-16)

- Every chat response now leads with an `analysis` block: What / When / Who /
  How / Where / Why / Which / Whose / Whom / How much — each answered or
  "Not needed" (`schemas.build_analysis`, `ChatResponse.analysis`).
- Commands fill `what`/`how`/`where` from `system_service`; conversation
  fallback fills what/how; Phase 4 AI will follow the same format.
- Frontend renders it as a compact "Request analysis" card above each
  assistant reply (`ChatBubble.jsx`). Verified via curl + `npm run build`.

---

## Generalization: provider-agnostic AI service (2026-08-16)

- AI is no longer Gemini-specific. New `backend/app/services/ai_service.py`
  defines an `AIProvider` interface with implementations for **gemini**
  (default), **openai**, and **ollama** (local). Providers are imported lazily,
  so the backend runs even if a provider package is not installed.
- Config generalized: `AI_PROVIDER`, `AI_API_KEY`, `AI_MODEL` in `.env`;
  `GEMINI_API_KEY` kept as a legacy alias (`config.py`).
- `ai_service.generate_reply()` is the single entry point the chat route will
  call in Phase 4. Verified: providers register, unknown provider raises a
  clear error, main imports fine without extra packages.
- Docs updated (README, SETUP, PRD, ARCHITECTURE, FEATURES, API, RULES,
  PHASES, DEVELOPMENT) — Gemini now described as the default provider.

---

## Fixes (2026-08-16)

- **CORS:** changed to `allow_origins=["*"]` (credentials off) so any local
  dev port works (5173, 5174, ...). Preflight was returning 400 for ports not
  in the old allow-list, which made the browser show "couldn't reach backend".
- Duplicate Vite servers on 5173 + 5174 caused the frontend to load from an
  unexpected port — keep only one `npm run dev` running.

---

## Wake mode fix (2026-08-16)

- **Wake listening no longer fails silently.** Previously, `recognition.start()`
  could throw synchronously (mic permission denied) and Chrome's speech
  recognition could fail with a `network` error (it streams audio to Google's
  servers, so it needs internet) — both were swallowed, so the UI showed
  "Sleeping…" but never listened, with zero feedback.
- Now any real failure (`not-allowed`, `service-not-allowed`, `network`,
  `audio-capture`, or a sync throw) stops wake mode and shows a red error
  message telling the user to check mic permission and internet.
- While wake mode is on, the status pill returns to "Sleeping… say 'Hello'"
  after each reply finishes (it was showing "Idle").

---

## Project Conventions (2026-08-16)

- **No emojis in frontend code or UI text** — use SVG icons / text labels.
  Emojis are allowed only in terminal/chat communication (e.g. assistant replies) for readability.
- Replaced the empty-state sparkle emoji in `pages/Home.jsx` with an inline SVG icon.

---

## Documentation Update (2026-08-16)

All markdown docs expanded with more detail (workflow, acceptance criteria,
examples) and given version footers: README, PRD, ARCHITECTURE, SETUP, RULES,
PHASES, DESIGN, FEATURES, API, DEVELOPMENT, and this file.

---

## Version

**v1.1** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Added Phase 1 completion log + docs update note. |
| v1.1 | 2026-08-16 | Added project convention: no emojis in frontend/UI. |
| v1.2 | 2026-08-16 | Added Phase 2 completion log. |
| v1.3 | 2026-08-16 | Logged CORS fix and duplicate-frontend-port issue. |
| v1.4 | 2026-08-16 | Added Phase 3 completion log. |
| v1.5 | 2026-08-16 | Logged generic app opening (no enumeration needed) + safety validation. |
| v1.6 | 2026-08-16 | Logged provider-agnostic AI service (gemini/openai/ollama). |
| v1.7 | 2026-08-16 | Logged request-analysis feature (all question dimensions answered first). |
| v1.8 | 2026-08-16 | Logged Phase 4 (AI integration with Groq provider + structured replies). |
| v1.9 | 2026-08-16 | Logged Phase 5 (voice: STT + edge-tts TTS + status pill). |
| v1.10 | 2026-08-16 | Logged wake word ("Hey AURA") + auto-sleep toggle. |
| v1.11 | 2026-08-16 | Wake word changed to "Hello" (+ variants) per user request. |
| v1.12 | 2026-08-16 | TTS audio deleted after playback: DELETE /api/audio/{filename} (validated) + 1h orphan sweep. Also fixed relative audio_url not playing in dev (absolutized against backend base; strong ref kept). |
| v1.13 | 2026-08-16 | Command replies use "done" format ("Opened notepad.") instead of "doing" ("Opening notepad."). |
