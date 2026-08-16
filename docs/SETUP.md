# AURA – Setup & Installation Guide

This guide explains how to install and run the AURA Voice Assistant on your laptop.

---

## Quick Start (TL;DR)

```bash
# Terminal 1 – Backend
cd backend
python -m venv venv
source venv/Scripts/activate        # Git Bash · venv\Scripts\activate (cmd/PowerShell) · source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
cp .env.example .env
python run.py                       # → http://127.0.0.1:8001

# Terminal 2 – Frontend
cd frontend
npm install
npm run dev                         # → http://localhost:5173
```

Everything below explains each step in detail.

---

## 1. Prerequisites

### Required Software
- **Python 3.10+** → [Download](https://www.python.org/downloads/)
- **Node.js 18+** → [Download](https://nodejs.org/)
- **Git** (optional but recommended)
- **Google Chrome** (best browser for microphone access)

### Check Versions
Open terminal/command prompt and run:

```bash
python --version
node --version
npm --version
```

---

## 2. Get an AI API Key (default: Groq)

AURA uses a provider-agnostic **AI service** (`AI_PROVIDER` in `.env`). The
current default is **Groq** (fast, free tier); Gemini, OpenAI, or a local
Ollama server can be swapped in without changing code.

**Groq (default):**
1. Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign in / create a free account
3. Click **Create API Key**, copy it

**Alternative providers:** Gemini → [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) ·
OpenAI → platform.openai.com · Ollama → local server (no key)

> **Note:** The key is only used by the AI service (Phase 4). The app runs
> fine without it during Phase 1–3.

---

## 3. Project Setup

The project is already fully scaffolded, so setup is just two steps:
install backend dependencies and install frontend dependencies.

### Step 1: Backend Setup

```bash
cd backend

# 1. Create and activate a virtual environment
python -m venv venv

# Windows (cmd/PowerShell):
venv\Scripts\activate
# Windows (Git Bash) / Mac / Linux:
source venv/Scripts/activate   # Git Bash
# source venv/bin/activate     # Mac / Linux

# 2. Install backend dependencies
pip install -r requirements.txt
```

Create the environment file. A template already exists at `backend/.env.example`:

```bash
cp .env.example .env
```

Then open `.env` and set your AI API key (can be left empty for now):

```
AI_PROVIDER=gemini      # gemini (default), openai, or ollama
AI_API_KEY=your_actual_api_key_here
AI_MODEL=               # optional model override
HOST=127.0.0.1
PORT=8001
```

> `.env` is gitignored — never commit it. Only `.env.example` is tracked.

> **Tip:** if you run `python run.py` WITHOUT activating the venv, the server
> uses your system Python — install the same requirements there too:
> `python -m pip install -r requirements.txt`.

**Verify:** `pip list` should show `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`.

### Step 2: Frontend Setup

Open a **new terminal** (or deactivate the venv first):

```bash
cd frontend
npm install
```

**Verify:** `npm run build` should complete without errors (a `dist/` folder is produced).

---

## 4. Running the Application

You need **two terminals**: one for the backend, one for the frontend.

### Start Backend (Terminal 1)

```bash
cd backend
# Activate venv if not already active (see Step 1)
python run.py
```

`run.py` reads `HOST` and `PORT` from `.env` and enables auto-reload.

Alternative (same result, no launcher):

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Backend will run at: **http://127.0.0.1:8001**

Verify it is up by opening http://127.0.0.1:8001/ in the browser — you should
see:

```json
{"status": "online", "message": "Hello from AURA"}
```

Interactive API docs (FastAPI auto-generated): **http://127.0.0.1:8001/docs**

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will run at: **http://localhost:5173**

Open that URL in Chrome. You should see the AURA dark-themed interface
(sidebar + chat area + input box).

---

## 5. Development Workflow (Daily Loop)

After initial setup, your normal working loop is:

1. **Terminal 1:** `cd backend && python run.py` — backend with auto-reload
2. **Terminal 2:** `cd frontend && npm run dev` — frontend with hot reload
3. Edit code → save → both servers pick changes up automatically
4. **Important:** uvicorn's auto-reload watches `.py` files **only** — after editing `.env` (e.g. adding/rotating an API key), restart the backend manually: `Ctrl+C` then `python run.py`
5. Test in the browser at http://localhost:5173
6. Run checks before finishing: `npm run build` (frontend) and `python -c "import app.main"` (backend imports clean)
7. Commit after each completed phase (see docs/RULES.md git workflow)

---

## 6. First Run Checklist

- [ ] Backend is running without errors
- [ ] http://127.0.0.1:8001/ shows `"message": "Hello from AURA"`
- [ ] Frontend opens in browser at http://localhost:5173
- [ ] AURA interface (sidebar + empty chat + input box) is visible
- [ ] (Later phases) Microphone permission is allowed
- [ ] (Later phases) AI API key is correctly set in `.env`

---

## 7. Common Issues & Solutions

| Problem                        | Solution                                      |
|--------------------------------|-----------------------------------------------|
| Microphone not working         | Use Chrome + allow permission                 |
| AI API error                   | Check `AI_API_KEY` in `.env`                  |
| CORS error                     | Make sure backend CORS is enabled             |
| Module not found               | Activate virtual environment                  |
| `python run.py` not found      | Make sure you are inside the `backend/` folder |
| `[WinError 10013]` port error  | Port busy — wait, or `netstat -ano \| findstr :8001` then `taskkill /PID <pid> /F` |
| Port already in use            | Change port in `.env` or kill previous process |
| pyautogui not working on Mac   | Give Accessibility permission to Terminal     |

---

## 8. Folder Structure After Setup

```
aura-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app (hello endpoint, CORS)
│   │   ├── config.py        # Loads .env settings
│   │   ├── routes/          # API routes (chat comes in Phase 2)
│   │   ├── services/        # Business logic (Phase 3+)
│   │   └── models/          # Pydantic schemas (Phase 2+)
│   ├── venv/                # Virtual environment (not committed)
│   ├── .env                 # Your secrets (not committed)
│   ├── .env.example         # Template for .env
│   ├── requirements.txt
│   └── run.py               # Convenience launcher
├── frontend/
│   ├── src/
│   │   ├── components/      # Sidebar.jsx, etc.
│   │   ├── pages/           # Home.jsx (chat area)
│   │   └── ...
│   ├── package.json
│   └── ...
├── docs/                    # All documentation (PRD, phases, design, etc.)
└── README.md
```

---

## 9. Recommended Development Order

1. Setup backend + basic FastAPI hello world
2. Setup React frontend + basic UI
3. Connect frontend to backend
4. Add system commands
5. Add AI brain (AI service)
6. Add speech features
7. Polish UI

---

## Version

**v1.1** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Rewritten to match the real repo (venv, requirements.txt, run.py, .env.example) |
| v1.1 | 2026-08-16 | Added Quick Start TL;DR, verify steps, development workflow loop, port-8001 troubleshooting |

---

**You are now ready to start development.**
