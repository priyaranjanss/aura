# AURA – Development Guide & Roadmap

This file contains practical development guidelines, coding standards, and the recommended roadmap to complete the project.

---

## 1. Development Roadmap

### Phase 1 – Foundation (Day 1) ✅
- [x] Create project folders
- [x] Setup FastAPI backend with hello world
- [x] Setup React + Vite + Tailwind
- [x] Connect frontend to backend (simple test message)
- [x] Create basic chat UI

### Phase 2 – Core System Control (Day 2)
- [ ] Implement open application commands
- [ ] Implement open website commands
- [ ] Implement time & date
- [ ] Add intent detection logic
- [ ] Test all basic commands

### Phase 3 – AI Integration (Day 3)
- [ ] Integrate AI service (default provider: Gemini)
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

> Phase numbering here differs slightly from `docs/PHASES.md` (which splits chat
> and system commands). **Follow PHASES.md** for what each phase must deliver;
> this roadmap maps the same work onto a day-by-day plan.

---

## 2. Development Workflow (Daily Loop)

1. **Pick a phase** from docs/PHASES.md and read its tasks + acceptance criteria.
2. **Create a branch:** `git checkout -b feature/phase-<n>-<name>`
3. **Run both servers** (see docs/SETUP.md §5):
   - `cd backend && python run.py`
   - `cd frontend && npm run dev`
4. **Implement** one small piece, then test it in the browser immediately.
5. **Run checks** before committing:
   - Backend imports: `cd backend && python -c "import app.main"`
   - Frontend build: `cd frontend && npm run build`
6. **Commit** small, focused changes with clear messages.
7. **Finish a phase** → update docs/PHASES.md tracker + docs/memory.md, then commit.

---

## 3. Coding Guidelines

### Backend (Python)
- Use type hints
- Keep services separated (ai_service, command_service, system_service)
- Never hardcode API keys
- Return consistent JSON responses
- Add try-except blocks around system commands

```python
def tell_time() -> dict:
    """Return the current time as a consistent JSON result."""
    from datetime import datetime
    now = datetime.now().strftime("%I:%M %p")
    return {"success": True, "reply": f"The time is {now}."}
```

### Frontend (React)
- Use functional components + hooks
- Use Zustand for state management
- Keep components small and focused
- Store chat messages in a Zustand store
- Handle loading and error states properly
- Use Tailwind for styling (tokens from docs/DESIGN.md)

```jsx
// Store: src/store/chatStore.js (Phase 2)
import { create } from 'zustand';

export const useChatStore = create((set) => ({
  messages: [],
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  clearMessages: () => set({ messages: [] }),
}));
```

---

## 4. Recommended File Creation Order

**Backend**
1. `main.py` ✅
2. `config.py` ✅
3. `schemas.py` (Phase 2)
4. `system_service.py` (Phase 3)
5. `command_service.py` (Phase 3)
6. `ai_service.py` (Phase 4)
7. `routes/chat.py` (Phase 2)

**Frontend**
1. Basic `App.jsx` layout ✅
2. `ChatWindow.jsx` + `ChatBubble.jsx` (Phase 2)
3. `MicrophoneButton.jsx` (Phase 5)
4. `api.js` service (Phase 2)
5. Status and Sidebar components (Sidebar ✅, Status in Phase 5)

---

## 5. Testing Checklist

- [ ] Backend starts without error (`python run.py`)
- [ ] Frontend starts without error (`npm run dev`)
- [ ] `npm run build` passes
- [ ] Can send text message and receive reply (Phase 2+)
- [ ] "open chrome" actually opens Chrome (Phase 3+)
- [ ] AI service answers general questions (Phase 4+)
- [ ] Microphone permission works (Phase 5+)
- [ ] Voice is converted to text correctly (Phase 5+)
- [ ] Assistant speaks the reply (Phase 5+)
- [ ] Volume commands work (Phase 6+)
- [ ] Screenshot is saved (Phase 6+)
- [ ] UI looks good on different screen sizes (Phase 6+)

---

## 6. Git Recommendations

```bash
git init
git add .
git commit -m "Initial project structure"
```

Create a `.gitignore` file (already done at repo root):

```
backend/venv/
backend/.env
frontend/node_modules/
frontend/dist/
__pycache__/
*.pyc
.DS_Store
```

**Commit message style:** `type(scope): short summary` — e.g.
`feat(chat): wire input to POST /api/chat`, `fix(backend): fallback when AI key missing`.

---

## 7. Demo Tips (For College Presentation)

1. Start both backend and frontend before the demo
2. Prepare a list of commands to show
3. Show both voice and text input
4. Demonstrate system control live (open Chrome, tell time, etc.)
5. Show the AI answering a smart question
6. Keep a backup text-only mode ready in case microphone fails

---

## 8. Possible Extensions After Completion

- Add wake word using open-source libraries
- Support local LLM (Ollama) as fallback
- Create a system tray icon
- Add user-defined custom commands
- Export chat history
- Add authentication if needed

---

## 9. Definition of Done (per task)

- Code follows docs/RULES.md (naming, error handling, no debug prints)
- No emojis in frontend/UI (emojis allowed in terminal messages only)
- Backend imports cleanly; frontend builds
- Feature tested in the browser against its acceptance criteria
- Docs updated if API/UI changed
- Committed with a clear message

---

## Version

**v1.1** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added daily workflow loop, code examples (Python + Zustand), definition of done, commit message style. |
| v1.1 | 2026-08-16 | Added no-emoji-in-frontend item to Definition of Done. |

---

**Follow this roadmap step by step and you will have a complete, professional fullstack AI Voice Assistant project.**
