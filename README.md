# AURA – Advanced Universal Response Assistant

**AURA** is a modern fullstack AI Voice Assistant that runs on your laptop and can control your computer using voice or text commands.

It features a beautiful React frontend and a powerful Python FastAPI backend. You can open applications, search the web, play music, control volume, take screenshots, ask intelligent questions, and much more — all by speaking or typing.

---

## Key Highlights

- Real computer control (open apps, websites, system actions)
- Google Gemini powered intelligent conversations
- High-quality Text-to-Speech replies
- Modern dark-themed React UI
- Voice + Text input support
- Real-time status indicators
- Chat history
- Multilingual support (English + Hindi)

---

## Project Structure

```
aura-assistant/
├── frontend/          # React + Vite + Tailwind CSS
├── backend/           # Python FastAPI
├── README.md          # This file
├── SETUP.md           # Installation guide
├── FEATURES.md        # Complete feature list
├── ARCHITECTURE.md    # System design
└── API.md             # Backend API documentation
```

---

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | React 18, Vite, Tailwind CSS, JavaScript, Zustand |
| Backend     | Python 3.10+, FastAPI, Uvicorn      |
| AI          | Google Gemini API                   |
| Speech      | Web Speech API + edge-tts           |
| System Control | os, subprocess, pyautogui, webbrowser |

---

## Quick Start

1. Read **SETUP.md** for detailed installation steps.
2. Add your Gemini API key in `backend/.env`
3. Start the backend
4. Start the frontend
5. Open http://localhost:5173

---

## Documentation Files

- [SETUP.md](SETUP.md) – Complete installation & running guide
- [FEATURES.md](FEATURES.md) – All features explained
- [ARCHITECTURE.md](ARCHITECTURE.md) – How the system works
- [API.md](API.md) – Backend API reference
- [DEVELOPMENT.md](DEVELOPMENT.md) – Development guidelines & roadmap

---

## Requirements

- Windows / macOS / Linux laptop
- Python 3.10 or higher
- Node.js 18 or higher
- Google Gemini API key (free)
- Chrome browser (recommended for microphone)

---

## License

This project is created for educational and personal use.

---

**Made for Computer Science Engineering students and developers who want a real-world fullstack + AI + system control project.**
