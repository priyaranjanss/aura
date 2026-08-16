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

---

**Follow these rules strictly. They will help you build a professional and safe project.**
