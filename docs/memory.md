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
    Gemini (Phase 4) plug into the same route later
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
  - Returns `None` for non-commands so conversation (Gemini, Phase 4) takes over
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
- Hook Gemini into the conversation fallback in `routes/chat.py` via `ai_service.py`
- Send history for context; handle missing/invalid API key gracefully

**Improvement (same day): generic app opening**
- `system_service.open_app` now opens ANY installed app by name (validated:
  letters/digits/spaces only; paths & shell metachars rejected). Known apps
  still use the per-OS map; others go to the OS launcher (`os.startfile` on
  Windows, `open -a` on macOS). Verified: "open snippingtool" opens it;
  "open ../../evil" and "open calc & del *" are rejected.
- The real "brain" (Gemini intent detection) lands in Phase 4 — Gemini decides
  the action, code still executes it (per RULES.md safety boundary).

---

## Fixes (2026-08-16)

- **CORS:** changed to `allow_origins=["*"]` (credentials off) so any local
  dev port works (5173, 5174, ...). Preflight was returning 400 for ports not
  in the old allow-list, which made the browser show "couldn't reach backend".
- Duplicate Vite servers on 5173 + 5174 caused the frontend to load from an
  unexpected port — keep only one `npm run dev` running.

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
