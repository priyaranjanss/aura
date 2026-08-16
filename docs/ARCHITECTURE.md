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
        ↓   ┌──────────────────────────────┐
   │  AI Brain analyzes request   │
   │  (any phrasing) → intent +   │
   │  question analysis + reply   │
   └──────────────┬───────────────┘
                  ↓
   Code validates the intent
   (safe action allowlist)
                  ↓
   ┌──────────────────────────────┐
   │ Valid command? Yes → execute │
   │ No  → conversation answer    │
   │ (keyword fallback if AI down)│
   └──────────────────────────────┘
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
4. **Analyze (AI first)** — `ai_service.py` sends the message to the AI brain, which returns a
   structured intent (`action`/`target`/`browser`), the question analysis, and a reply.
5. **Validate & execute** — `command_service.execute_ai_command()` checks the intent against the
   safe action allowlist and calls `system_service.py` (open app/website, search, time/date).
   If the AI is unavailable, keyword matching (`command_service.handle()`) runs as an offline fallback.
6. **Respond** — The backend returns `{ "reply", "type": "command" | "ai" | "error", "success", "audio_url", "analysis" }`.
6. **Render** — The frontend appends the reply to the Zustand chat store and (Phase 5+) plays the audio.

### Command vs Conversation Decision

The **AI brain** decides (any phrasing works: "open chrome", "launch chrome",
"can you show me the time"). Code validates and executes. Keyword matching is
an offline fallback when the AI is down.

| Input | Detected as | Handled by |
|-------|-------------|------------|
| "open chrome" / "launch chrome" | Command | AI intent → execute_ai_command → system_service |
| "what time is it" / "whats the time now" | Command | AI intent → execute_ai_command → system_service |
| "search google for cats" / "search the web for cats" | Command | AI intent → execute_ai_command → webbrowser |
| "explain black holes" | Conversation | AI answer |
| "tell me a joke" | Conversation | AI answer |

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
│   │   │   ├── MicrophoneButton.jsx   # ✅ Built — voice input button (Phase 5)
│   │   │   ├── Sidebar.jsx            # ✅ Built (Phase 1)
│   │   │   ├── StatusBar.jsx          # Listening/Thinking/Speaking (Phase 5)
│   │   │   ├── QuickCommands.jsx      # Shortcut buttons (Phase 6)
│   │   │   └── SettingsPanel.jsx      # Settings (Phase 6)
│   │   ├── pages/
│   │   │   └── Home.jsx               # ✅ Built — chat area shell (Phase 1)
│   │   ├── services/
│   │   │   └── api.js                 # ✅ Built — axios calls to backend (Phase 2)
│   │   ├── hooks/
│   │   │   └── useSpeech.js           # ✅ Built — Web Speech API wrapper (Phase 5)
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
│   │   │   ├── ai_service.py          # ✅ Built — AI calls, provider-agnostic (Phase 4)
│   │   │   ├── command_service.py     # ✅ Built — intent detection (Phase 3)
│   │   │   ├── speech_service.py      # ✅ Built — edge-tts audio (Phase 5)
│   │   │   └── system_service.py      # ✅ Built — OS actions (Phase 3)
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
| Pluggable AI service (Gemini default) | AI brain        |
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
  "audio_url": null,
  "analysis": [
    {"question": "What", "answer": "Open the 'chrome' application"},
    {"question": "When", "answer": "Not needed"},
    {"question": "Who", "answer": "Not needed"},
    {"question": "How", "answer": "Launch via the operating system's app launcher"},
    {"question": "Where", "answer": "Not needed"},
    {"question": "Why", "answer": "Not needed"},
    {"question": "Which", "answer": "Not needed"},
    {"question": "Whose", "answer": "Not needed"},
    {"question": "Whom", "answer": "Not needed"},
    {"question": "How much", "answer": "Not needed"}
  ]
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
| `services/ai_service.py` | Calls the configured AI provider with history |
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
AI call ── exception ──► fallback reply, success=false
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
- **Change the AI provider** → edit `backend/.env`: `AI_PROVIDER=gemini|openai|ollama`, plus `AI_API_KEY` / `AI_MODEL`. Providers live in `services/ai_service.py`.
- **Change ports** → edit `backend/.env` (`PORT`) and `frontend/vite.config.js` (`server.port`).

---

## Version

**v1.0** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added request lifecycle walkthrough, module responsibility tables, error flow, configuration table, extension points; marked built files with ✅. |
| v1.1 | 2026-08-16 | Marked Phase 2 files as built (chat route, schemas, api.js, chatStore, ChatBubble, ChatWindow). |
| v1.2 | 2026-08-16 | Marked Phase 3 services as built (command_service, system_service). |
| v1.3 | 2026-08-16 | Marked ai_service as built (Groq provider, structured replies). |
| v1.4 | 2026-08-16 | Marked Phase 5 files as built (speech_service, MicrophoneButton, useSpeech). |

---

**This architecture keeps the system simple, powerful, and easy to extend.**
