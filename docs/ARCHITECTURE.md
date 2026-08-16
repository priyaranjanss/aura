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

### Detailed Components

**Frontend Responsibilities**
- Display chat interface
- Capture voice using Web Speech API
- Send messages to backend
- Show live status
- Play Text-to-Speech audio
- Manage chat history in UI

**Backend Responsibilities**
- Receive user message
- Detect intent (command vs conversation)
- Execute system commands on the laptop
- Call Google Gemini for intelligent replies
- Generate speech using edge-tts
- Return clean JSON response

**System Control Layer**
- Directly interacts with Operating System
- Uses Python libraries to open apps, control volume, take screenshots, etc.

---

## 2. Folder & File Structure

```
aura-assistant/
│
├── frontend/                          # React Application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBubble.jsx
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── MicrophoneButton.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── StatusBar.jsx
│   │   │   ├── QuickCommands.jsx
│   │   │   └── SettingsPanel.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── hooks/
│   │   │   └── useSpeech.js
│   │   ├── store/
│   │   │   └── chatStore.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── backend/                           # Python FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── system.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py
│   │   │   ├── command_service.py
│   │   │   ├── speech_service.py
│   │   │   └── system_service.py
│   │   └── models/
│   │       └── schemas.py
│   ├── requirements.txt
│   ├── .env
│   └── run.py
│
├── docs/                              # All documentation
│   ├── PRD.md
│   ├── Architecture.md
│   ├── rules.md
│   ├── phases.md
│   ├── design.md
│   ├── SETUP.md
│   ├── FEATURES.md
│   └── API.md
│
├── README.md
└── .gitignore
```

---

## 3. Tech Stack

### Frontend
| Technology       | Purpose                              |
|------------------|--------------------------------------|
| React 18         | UI library                           |
| Vite             | Fast build tool                      |
| Tailwind CSS     | Styling                              |
| JavaScript (ES6) | Main language                        |
| Zustand          | State management                       |
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

- Frontend ↔ Backend → REST API (JSON)
- Real-time status → WebSocket (optional advanced)
- All system actions happen only through the Python backend (security)

---

**This architecture keeps the system simple, powerful, and easy to extend.**
