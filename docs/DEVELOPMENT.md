# AURA – Development Guide & Roadmap

This file contains practical development guidelines, coding standards, and the recommended roadmap to complete the project.

---

## 1. Development Roadmap

### Phase 1 – Foundation (Day 1)
- [ ] Create project folders
- [ ] Setup FastAPI backend with hello world
- [ ] Setup React + Vite + Tailwind
- [ ] Connect frontend to backend (simple test message)
- [ ] Create basic chat UI

### Phase 2 – Core System Control (Day 2)
- [ ] Implement open application commands
- [ ] Implement open website commands
- [ ] Implement time & date
- [ ] Add intent detection logic
- [ ] Test all basic commands

### Phase 3 – AI Integration (Day 3)
- [ ] Integrate Google Gemini
- [ ] Send conversation history
- [ ] Handle AI vs Command routing
- [ ] Improve reply quality

### Phase 4 – Voice Features (Day 4)
- [ ] Add microphone button in React
- [ ] Use Web Speech API for Speech-to-Text
- [ ] Integrate edge-tts for Text-to-Speech
- [ ] Show live status (Listening / Thinking / Speaking)

### Phase 5 – Advanced Commands & UI (Day 5)
- [ ] Volume control
- [ ] Screenshot
- [ ] Quick command buttons
- [ ] Chat history persistence
- [ ] Settings panel
- [ ] Better dark theme and animations

### Phase 6 – Polish & Final (Day 6+)
- [ ] Error handling
- [ ] Confirmation for dangerous actions
- [ ] Multilingual support
- [ ] README and documentation finalization
- [ ] Demo video preparation

---

## 2. Coding Guidelines

### Backend (Python)
- Use type hints
- Keep services separated (ai_service, command_service, system_service)
- Never hardcode API keys
- Return consistent JSON responses
- Add try-except blocks around system commands

### Frontend (React)
- Use functional components + hooks
- Use Zustand for state management
- Keep components small and focused
- Store chat messages in a Zustand store
- Handle loading and error states properly
- Use Tailwind for styling

---

## 3. Recommended File Creation Order

**Backend**
1. `main.py`
2. `config.py`
3. `schemas.py`
4. `system_service.py`
5. `command_service.py`
6. `ai_service.py`
7. `routes/chat.py`

**Frontend**
1. Basic `App.jsx` layout
2. `ChatWindow.jsx` + `ChatBubble.jsx`
3. `MicrophoneButton.jsx`
4. `api.js` service
5. Status and Sidebar components

---

## 4. Testing Checklist

- [ ] Backend starts without error
- [ ] Frontend starts without error
- [ ] Can send text message and receive reply
- [ ] “open chrome” actually opens Chrome
- [ ] Gemini answers general questions
- [ ] Microphone permission works
- [ ] Voice is converted to text correctly
- [ ] Assistant speaks the reply
- [ ] Volume commands work
- [ ] Screenshot is saved
- [ ] UI looks good on different screen sizes

---

## 5. Git Recommendations

```bash
git init
git add .
git commit -m "Initial project structure"
```

Create a `.gitignore` file:

```
backend/venv/
backend/.env
frontend/node_modules/
frontend/dist/
__pycache__/
*.pyc
.DS_Store
```

---

## 6. Demo Tips (For College Presentation)

1. Start both backend and frontend before the demo
2. Prepare a list of commands to show
3. Show both voice and text input
4. Demonstrate system control live (open Chrome, tell time, etc.)
5. Show Gemini answering a smart question
6. Keep a backup text-only mode ready in case microphone fails

---

## 7. Possible Extensions After Completion

- Add wake word using open-source libraries
- Support local LLM (Ollama) as fallback
- Create a system tray icon
- Add user-defined custom commands
- Export chat history
- Add authentication if needed

---

**Follow this roadmap step by step and you will have a complete, professional fullstack AI Voice Assistant project.**
