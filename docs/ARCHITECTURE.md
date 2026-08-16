# Architecture.md – App Flow, Structure & Tech Stack

---

## 1. App Flow & Architecture

### High-Level Flow

```
User speaks or types
        ↓
React Frontend (UI + Microphone)
        ↓
HTTP Request (POST /api/chat)
        ↓
Python FastAPI Backend
        ↓
   ┌──────────────────────────┐
   │   Intent Detection       │
   │                          │
   │  Is it a system command? │
   │          │               │
   │     Yes  │  No           │
   │      ↓   │   ↓           │
   │ Command  │  Gemini AI    │
   │ Service  │  Service      │
   └──────────────────────────┘
        ↓
Execute action on Laptop / Generate AI reply
        ↓
Return response + optional audio
        ↓
Frontend shows reply + speaks it
```

### Request Lifecycle (Step by Step)

1. **Capture** — The user types or speaks a message in the frontend.
2. **Send** — `services/api.js` (axios) POSTs `{ "message": "...", "history": [...] }` to `POST http://127.0.0.1:8001/api/chat`.
3. **Receive** — FastAPI route (`routes/chat.py`) validates the body with Pydantic (`models/schemas.py`).
4. **Route** — `command_service.py` decides: is this a known system command?
   - **Yes** → `system_service.py` executes the safe-list action (open app, tell time, …).
   - **No** → `ai_service.py` calls Google Gemini with conversation history.
5. **Respond** — The backend returns `{ "reply", "type": "command" | "ai", "success", "audio_url" }`.
6. **Render** — The frontend appends the reply to the Zustand chat store and (Phase 5+) plays the audio.

### Command vs Conversation Decision

| Input | Detected as | Handled by |
|-------|-------------|------------|
| "open chrome" | Command | command_service → system_service |
| "what time is it" | Command | command_service → system_service |
| "search google for cats" | Command | command_service → webbrowser |
| "explain black holes" | Conversation | ai_service → Gemini |
| "tell me a joke" | Conversation | ai_service → Gemini |

---

## 2. Folder & File Structure

```
aura-assistant/
│
├── frontend/                          # React Application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBubble.jsx         # ✅ Built — one message bubble (Phase 2)
│   │   │   ├── ChatWindow.jsx         # ✅ Built — scrollable message list (Phase 2)
│   │   │   ├── MicrophoneButton.jsx   # Voice input button (Phase 5)
│   │   │   ├── Sidebar.jsx            # ✅ Built (Phase 1)
│   │   │   ├── StatusBar.jsx          # Listening/Thinking/Speaking (Phase 5)
│   │   │   ├── QuickCommands.jsx      # Shortcut buttons (Phase 6)
│   │   │   └── SettingsPanel.jsx      # Settings (Phase 6)
│   │   ├── pages/
│   │   │   └── Home.jsx               # ✅ Built — chat area shell (Phase 1)
│   │   ├── services/
│   │   │   └── api.js                 # ✅ Built — axios calls to backend (Phase 2)
│   │   ├── hooks/
│   │   │   └── useSpeech.js           # Web Speech API wrapper (Phase 5)
│   │   ├── store/
│   │   │   └── chatStore.js           # ✅ Built — Zustand store for messages (Phase 2)
│   │   ├── App.jsx                    # ✅ Built — layout (Phase 1)
│   │   ├── main.jsx                   # ✅ Built
│   │   └── index.css                  # ✅ Built — Tailwind + base styles
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── backend/                           # Python FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # ✅ Built — app, CORS, GET / (Phase 1)
│   │   ├── config.py                  # ✅ Built — .env settings (Phase 1)
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py                # ✅ Built — POST /api/chat (Phase 2)
│   │   │   └── system.py              # System actions API (Phase 3)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py          # Gemini calls (Phase 4)
│   │   │   ├── command_service.py     # Intent detection (Phase 3)
│   │   │   ├── speech_service.py      # edge-tts audio (Phase 5)
│   │   │   └── system_service.py      # OS actions (Phase 3)
│   │   └── models/
│   │       └── schemas.py             # ✅ Built — Pydantic models (Phase 2)
│   ├── requirements.txt
│   ├── .env / .env.example
│   └── run.py                         # ✅ Built — launcher (Phase 1)
│
├── docs/                              # All documentation
├── README.md
└── .gitignore
```

> ✅ = already built. Files without ✅ arrive in the phase shown.

---

## 3. Tech Stack

### Frontend
| Technology       | Purpose                              |
|------------------|--------------------------------------|
| React 18         | UI library                           |
| Vite             | Fast build tool                      |
| Tailwind CSS     | Styling                              |
| JavaScript (ES6) | Main language                        |
| Zustand          | State management                     |
| Axios            | API calls                            |
| Web Speech API   | Speech-to-Text in browser            |

### Backend
| Technology              | Purpose                              |
|-------------------------|--------------------------------------|
| Python 3.10+            | Main language                        |
| FastAPI                 | Web framework                        |
| Uvicorn                 | ASGI server                          |
| Google Gemini API       | AI brain                             |
| edge-tts                | High quality Text-to-Speech          |
| pyautogui               | Mouse/keyboard & system control      |
| webbrowser / os / subprocess | Open apps & websites            |
| python-dotenv           | Environment variables                |
| Pydantic                | Data validation                      |

### Tools & Others
- Git & GitHub
- Chrome browser (recommended)
- VS Code (recommended editor)

---

## 4. Communication

- **Frontend ↔ Backend** → REST API (JSON)
- **Real-time status** → WebSocket `/ws/status` (optional, advanced)
- **All system actions happen only through the Python backend** (security)

### Example Payloads

**Request** — `POST /api/chat`
```json
{
  "message": "open chrome",
  "history": [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "Hi! How can I help you?"}
  ]
}
```

**Response**
```json
{
  "reply": "Opening Google Chrome for you.",
  "type": "command",
  "success": true,
  "audio_url": null
}
```

---

## 5. Module Responsibilities

### Frontend
| Module | Responsibility |
|--------|----------------|
| `App.jsx` | Root layout (sidebar + main area) |
| `pages/Home.jsx` | Chat area: header, messages, input |
| `components/ChatWindow.jsx` | Scrollable list of bubbles |
| `components/ChatBubble.jsx` | Renders one user/assistant message |
| `components/MicrophoneButton.jsx` | Captures speech via Web Speech API |
| `components/StatusBar.jsx` | Live Listening/Thinking/Speaking state |
| `services/api.js` | All axios calls to the backend |
| `store/chatStore.js` | Zustand: messages, status, actions |

### Backend
| Module | Responsibility |
|--------|----------------|
| `main.py` | App factory, CORS, router mounting |
| `config.py` | Loads `.env` (HOST, PORT, GEMINI_API_KEY) |
| `routes/chat.py` | `POST /api/chat` — validates + orchestrates |
| `services/command_service.py` | Keyword-based intent detection |
| `services/system_service.py` | Executes safe-list OS actions |
| `services/ai_service.py` | Calls Gemini with history |
| `services/speech_service.py` | Generates TTS audio via edge-tts |
| `models/schemas.py` | Pydantic request/response models |

### System Control Layer
- Directly interacts with the Operating System
- Uses Python libraries to open apps, control volume, take screenshots, etc.
- Every action is wrapped in try-except (never crashes the app)

---

## 6. Error Handling Flow

```
Route receives request
        ↓
Validate (Pydantic) ── fails ──► 422 error JSON
        ↓
Intent detection ── error ──► friendly reply, success=false
        ↓
System command ── exception ──► "Sorry, I couldn't do that." + logged error
        ↓
Gemini call ── exception ──► fallback reply, success=false
        ↓
Return consistent JSON
```

---

## 7. Configuration

| Variable | Default | Used by |
|----------|---------|---------|
| `GEMINI_API_KEY` | empty | ai_service (Phase 4) |
| `HOST` | `127.0.0.1` | uvicorn bind address |
| `PORT` | `8001` | uvicorn port |

Loaded from `backend/.env` by `config.py` (gitignored; template in `.env.example`).

---

## 8. Extension Points

- **Add a command** → add a keyword → action entry in `command_service.py` + the action in `system_service.py`.
- **Add an API route** → create `routes/<name>.py`, include the router in `main.py`, add a Pydantic model in `schemas.py`.
- **Add a frontend feature** → new component under `components/`, state in `store/chatStore.js`, styles with Tailwind tokens from `docs/DESIGN.md`.
- **Change ports** → edit `backend/.env` (`PORT`) and `frontend/vite.config.js` (`server.port`).

---

## Version

**v1.0** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added request lifecycle walkthrough, module responsibility tables, error flow, configuration table, extension points; marked built files with ✅. |
| v1.1 | 2026-08-16 | Marked Phase 2 files as built (chat route, schemas, api.js, chatStore, ChatBubble, ChatWindow). |

---

**This architecture keeps the system simple, powerful, and easy to extend.**
