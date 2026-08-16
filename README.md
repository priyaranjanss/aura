# AURA – Advanced Universal Response Assistant

**AURA** is a modern fullstack AI Voice Assistant that runs on your laptop and can control your computer using voice or text commands.

It features a beautiful React frontend and a powerful Python FastAPI backend. You can open applications, search the web, play music, control volume, take screenshots, ask intelligent questions, and much more — all by speaking or typing.

---

## Key Highlights

- Real computer control (open apps, websites, system actions)
- AI-powered conversations (Gemini by default, provider-swappable)
- High-quality Text-to-Speech replies
- Modern dark-themed React UI
- Voice + Text input support
- Real-time status indicators
- Chat history
- Multilingual support (English + Hindi)

---

## Project Status

The project is developed in 6 phases (see [docs/PHASES.md](docs/PHASES.md)). Progress is logged in [docs/memory.md](docs/memory.md).

| Phase | Name                        | Status                                   |
|-------|-----------------------------|------------------------------------------|
| 1     | Foundation & Login/UI Shell | ✅ Done — structure, UI shell, hello API |
| 2     | Dashboard & Core Chat       | ⬜ Not started                           |
| 3     | System Commands             | ⬜ Not started                           |
| 4     | AI Integration              | ⬜ Not started                           |
| 5     | Voice Features              | ⬜ Not started                           |
| 6     | Advanced UI & Polish        | ⬜ Not started                           |

---

## Project Structure

```
aura-assistant/
├── frontend/          # React + Vite + Tailwind CSS (port 5173)
├── backend/           # Python FastAPI (port 8001)
├── docs/              # All project documentation
├── README.md          # This file
└── .gitignore
```

---

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | React 18, Vite, Tailwind CSS, JavaScript, Zustand |
| Backend     | Python 3.10+, FastAPI, Uvicorn      |
| AI          | Pluggable AI service (Groq active)   |
| Speech      | Web Speech API + edge-tts           |
| System Control | os, subprocess, pyautogui, webbrowser |

---

## Quick Start

```bash
# Terminal 1 – backend (from project root)
cd backend
python -m venv venv
source venv/Scripts/activate        # Windows Git Bash · venv\Scripts\activate on cmd/PowerShell · source venv/bin/activate on Mac/Linux
pip install -r requirements.txt
cp .env.example .env                # optionally add your AI API key
python run.py                       # → http://127.0.0.1:8001

# Terminal 2 – frontend
cd frontend
npm install
npm run dev                         # → http://localhost:5173
```

Full step-by-step instructions: [docs/SETUP.md](docs/SETUP.md)

---

## Documentation Files

| File | Description |
|------|-------------|
| [SETUP.md](docs/SETUP.md) | Complete installation & running guide |
| [PRD.md](docs/PRD.md) | Project requirements, users, success criteria |
| [FEATURES.md](docs/FEATURES.md) | All features with phase mapping |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & data flow |
| [API.md](docs/API.md) | Backend API reference (base: `http://127.0.0.1:8001`) |
| [RULES.md](docs/RULES.md) | Development rules & safety guidelines |
| [PHASES.md](docs/PHASES.md) | Phase plan with acceptance criteria |
| [DESIGN.md](docs/DESIGN.md) | UI design system (colors, typography) |
| [DEVELOPMENT.md](docs/DEVELOPMENT.md) | Dev workflow, guidelines & roadmap |
| [memory.md](docs/memory.md) | Development progress log |

---

## Requirements

- Windows / macOS / Linux laptop
- Python 3.10 or higher
- Node.js 18 or higher
- AI API key (Groq free tier works) — needed for Phase 4 AI
- Chrome browser (recommended for microphone)

---

## License

This project is created for educational and personal use.

---

## Version

**v1.0** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added project status, ports, docs overview, quick start commands, version footer. |

---

**Made for Computer Science Engineering students and developers who want a real-world fullstack + AI + system control project.**
