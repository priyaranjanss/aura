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
- Frontend builds with `npm run build` (no errors) and dev server serves on :5173

**Notes / next phase (Phase 2 – Dashboard & Core Chat):**
- Wire the input box to `POST /api/chat`
- Add `ChatWindow` / `ChatBubble` components, Zustand store, loading state
- Add `services/api.js` (axios) and `models/schemas.py`
