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
