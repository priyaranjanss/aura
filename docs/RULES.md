# rules.md – Development Rules & Guidelines

This document defines clear rules for building AURA so the project stays clean, safe, and maintainable.

---

## 1. What to Use

### Recommended Libraries & Tools

**Frontend**
- React + Vite
- Tailwind CSS
- Axios for API calls
- Web Speech API (built into Chrome)

**Backend**
- FastAPI
- Google Generative AI (`google-generativeai`)
- `edge-tts` for Text-to-Speech
- `pyautogui` for system automation
- `python-dotenv` for secrets
- `pydantic` for request/response models

**General**
- Git for version control
- Virtual environment (`venv`) for Python
- `.env` file for API keys
- Chrome browser for testing voice features

### Coding Practices to Follow
- Write clean and readable code
- Use meaningful variable and function names
- Keep functions small and focused
- Add comments for complex logic
- Use try-except blocks around system commands
- Return consistent JSON responses from backend
- Keep frontend components small

---

## 2. What to Avoid

### Libraries & Approaches to Avoid
- Do **not** use Streamlit (we are using React)
- Do **not** put system control code in the frontend
- Do **not** hardcode Gemini API key in code
- Do **not** use outdated speech libraries when edge-tts is available
- Avoid very heavy frameworks unless necessary
- Do not depend on paid APIs if free alternatives exist

### Bad Practices to Avoid
- Do not run dangerous commands (shutdown/restart) without confirmation
- Do not commit `.env` file to Git
- Do not leave print debugging statements in final code
- Do not make the backend publicly accessible on the internet
- Avoid deeply nested if-else (prefer clean intent detection)
- Do not ignore errors silently
- Do **not** use emojis in frontend code or user-facing UI text — use SVG icons and text labels instead. Emojis are allowed only in terminal/chat communication (e.g. assistant replies) for readability

---

## 3. Error Handling Rules

- Every system command must be wrapped in try-except
- Return friendly error messages to the user
- If Gemini fails, show a fallback reply
- If microphone fails, allow text input
- Log errors in backend console for debugging
- Never crash the whole application because of one failed command

**Example pattern:**
```python
try:
    # execute command
    return {"success": True, "reply": "Done"}
except Exception as e:
    print(f"[command] error: {e}")  # log for debugging
    return {"success": False, "reply": "Sorry, I couldn't do that."}
```

---

## 4. Boundary for AI (Important)

### What AI (Gemini) Should Handle
- General questions
- Conversations
- Jokes, facts, explanations
- Summarization
- Creative responses
- Intent understanding (advanced)

### What AI Should NOT Directly Control
- AI should **never** directly execute system commands
- All system actions must go through the Command Service
- Dangerous actions must have explicit confirmation from user
- AI should not be given unrestricted shell access

### Safety Boundary
```
User Message
     ↓
Intent Detection (Code)
     ↓
┌──────────────┬─────────────────┐
│ System       │  Gemini AI      │
│ Command      │  (Conversation) │
│ (Safe list)  │                 │
└──────────────┴─────────────────┘
```

Only pre-approved commands are allowed to run on the system.

---

## 5. Security Rules

- Backend must run only on `127.0.0.1` (localhost)
- Never expose the backend to the public internet
- Keep Gemini API key secret
- Confirm before shutdown / restart / lock
- Do not allow arbitrary code execution from user input

---

## 6. Code Quality Rules

- One feature = one clear module/service
- Frontend and Backend must stay separated
- Write a short comment at the top of every major file
- Keep the project structure consistent with Architecture.md
- Update documentation when you add major features

### Naming Conventions

| Layer | Convention | Example |
|-------|------------|---------|
| Python files | snake_case | `command_service.py` |
| Python functions/vars | snake_case | `def open_app(name):` |
| JSX components | PascalCase | `ChatBubble.jsx` |
| JS functions/vars | camelCase | `handleSubmit` |
| CSS/Tailwind | Design tokens | `bg-aura-surface` |
| Endpoints | kebab/snake paths | `/api/chat`, `/api/status` |

---

## 7. Code Style Examples

### Backend (Python)

```python
"""Opens an installed application by name."""
import subprocess

APPS = {"chrome": "chrome", "notepad": "notepad", "code": "code"}

def open_app(name: str) -> dict:
    """Open a pre-approved app. Returns a consistent JSON result."""
    try:
        subprocess.Popen([APPS[name]])  # name is validated against APPS
        return {"success": True, "reply": f"Opening {name}."}
    except KeyError:
        return {"success": False, "reply": f"I don't know the app '{name}'."}
    except Exception as e:
        print(f"[system] open_app failed: {e}")
        return {"success": False, "reply": "Sorry, I couldn't open that app."}
```

### Frontend (React)

```jsx
// One small, focused component
export default function ChatBubble({ role, text }) {
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[75%] rounded-2xl px-4 py-3 ${
        isUser ? 'bg-aura-primary text-white' : 'bg-aura-surface text-white'
      }`}>
        {text}
      </div>
    </div>
  );
}
```

---

## 8. Git Workflow

```bash
# Work on a feature branch
git checkout -b feature/phase-2-chat

# Commit in small, focused steps
git add .
git commit -m "feat(chat): connect input box to POST /api/chat"

# Commit once per completed phase (see docs/PHASES.md)
# Never commit .env, venv/, node_modules/ (already in .gitignore)
```

- One commit = one logical change
- Commit after each phase milestone
- Write meaningful messages (what + why)

---

## 9. Review Checklist (Before You Finish a Feature)

- [ ] Code follows naming conventions (§6)
- [ ] System commands wrapped in try-except (§3)
- [ ] No hardcoded secrets (§5)
- [ ] No leftover `print()`/`console.log` debug lines (§2)
- [ ] No emojis in frontend/UI (§2 — emojis allowed in terminal messages only)
- [ ] Consistent JSON responses (§1)
- [ ] Backend imports cleanly: `python -c "import app.main"`
- [ ] Frontend builds: `npm run build`
- [ ] Docs updated if behavior/API changed (§6)

---

## Version

**v1.1** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added naming conventions, code style examples (Python + React), git workflow, review checklist. |
| v1.1 | 2026-08-16 | Added no-emoji-in-frontend rule and review checklist item. |

---

**Follow these rules strictly. They will help you build a professional and safe project.**
