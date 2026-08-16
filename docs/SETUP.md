# AURA – Setup & Installation Guide

This guide explains how to install and run the AURA Voice Assistant on your laptop.

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

## 2. Get Google Gemini API Key

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the key

> **Note:** The key is only used from Phase 4 (Gemini AI) onward. The app runs
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

Then open `.env` and set your Gemini API key (can be left empty for now):

```
GEMINI_API_KEY=your_actual_api_key_here
HOST=127.0.0.1
PORT=8001
```

> `.env` is gitignored — never commit it. Only `.env.example` is tracked.

### Step 2: Frontend Setup

Open a **new terminal** (or deactivate the venv first):

```bash
cd frontend
npm install
```

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

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will run at: **http://localhost:5173**

Open that URL in Chrome. You should see the AURA dark-themed interface
(sidebar + chat area + input box).

---

## 5. First Run Checklist

- [ ] Backend is running without errors
- [ ] http://127.0.0.1:8001/ shows `"message": "Hello from AURA"`
- [ ] Frontend opens in browser at http://localhost:5173
- [ ] AURA interface (sidebar + empty chat + input box) is visible
- [ ] (Later phases) Microphone permission is allowed
- [ ] (Later phases) Gemini API key is correctly set in `.env`

---

## 6. Common Issues & Solutions

| Problem                        | Solution                                      |
|--------------------------------|-----------------------------------------------|
| Microphone not working         | Use Chrome + allow permission                 |
| Gemini API error               | Check API key in `.env`                       |
| CORS error                     | Make sure backend CORS is enabled             |
| Module not found               | Activate virtual environment                  |
| `python run.py` not found      | Make sure you are inside the `backend/` folder |
| Port already in use            | Change port in `.env` or kill previous process |
| pyautogui not working on Mac   | Give Accessibility permission to Terminal     |

---

## 7. Folder Structure After Setup

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

## 8. Recommended Development Order

1. Setup backend + basic FastAPI hello world
2. Setup React frontend + basic UI
3. Connect frontend to backend
4. Add system commands
5. Add Gemini AI
6. Add speech features
7. Polish UI

---

**You are now ready to start development.**
