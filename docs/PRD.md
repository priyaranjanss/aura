# PRD.md – Project Requirements Document

**Project Name:** AURA – Advanced Universal Response Assistant  
**Version:** 1.0  
**Type:** Fullstack AI Voice Assistant (Desktop Control)

---

## 1. What to Build

AURA is a fullstack AI-powered Voice Assistant that runs locally on a user's laptop.

It allows the user to:

- Control the computer using voice or text commands
- Open applications and websites
- Search the web and play music
- Ask intelligent questions and get spoken answers
- Manage system settings (volume, screenshot, lock, etc.)

The application has two main parts:

1. **Frontend** → Modern React web interface (chat + microphone)
2. **Backend** → Python FastAPI server that controls the computer and talks to a pluggable AI service (Groq by default)

The entire system runs on the user's own laptop (no cloud deployment needed for core features).

### Glossary

| Term | Meaning |
|------|---------|
| AURA | The assistant product as a whole (frontend + backend) |
| Command | A message that maps to a system action (e.g. "open chrome") |
| Conversation | A message that should be answered by the AI service |
| Intent Detection | The backend logic that decides command vs conversation |
| TTS / STT | Text-to-Speech / Speech-to-Text |

---

## 2. Targeted Users

| User Type                    | Description                                      | Why they need AURA                          |
|-----------------------------|--------------------------------------------------|---------------------------------------------|
| Students (CSE / IT)         | College students doing final year projects       | Perfect fullstack + AI + system control project |
| Developers & Programmers    | People who want hands-free computer control      | Increase productivity while coding          |
| Productivity Seekers        | Anyone who wants to control PC by voice          | Reduce mouse/keyboard usage                 |
| AI Enthusiasts              | People learning AI, voice interfaces, LLMs       | Practical hands-on experience with AI + Speech    |
| Demo / Presentation Users   | Students presenting projects                     | Impressive live demo of AI controlling PC   |

**Primary Focus:** Computer Science Engineering students who need a complete, impressive, and realistic project.

### User Stories

- As a **student**, I can open apps and websites by voice so my demo looks impressive.
- As a **developer**, I can ask general questions and get AI answers while keeping my hands on the keyboard.
- As a **productivity seeker**, I can control volume, take screenshots, and lock my PC with one command.
- As an **AI enthusiast**, I can see the full pipeline: voice → intent → AI/system → spoken reply.
- As a **demo presenter**, I can fall back to typed input if the microphone fails.

---

## 3. Features

**The complete, up-to-date feature list with status and phase mapping lives in
[docs/FEATURES.md](FEATURES.md) — the single source of truth.** This section
only records the *priority tiers* the requirements were planned around, so
requirements and feature status stay in separate places.

### Priority Tiers

- **Core (must have):** text chat, chat history, computer control (open
  apps/websites, search, time & date), AI conversation, voice input,
  text-to-speech, real-time status, dark UI.
- **Should have:** volume control, screenshot, quick command buttons,
  settings panel, multilingual TTS, confirmation for dangerous actions,
  friendly error handling, conversation memory.
- **Nice to have (future):** offline mode (local LLM), custom user-defined
  commands, face recognition unlock, mobile companion app, voice cloning,
  plugin system, multi-user support.

> Every feature name above is detailed with its status in FEATURES.md; do not
> duplicate feature tables here.

---

## 4. Success Criteria

The project will be considered successful when:

1. User can control the computer completely by voice
2. The AI service gives intelligent and useful answers
3. UI looks modern and professional
4. System works reliably on a normal laptop
5. Student can demonstrate all major features live in 5–7 minutes

### Measurable Targets

| Criterion | Target |
|-----------|--------|
| Backend response time (command) | < 500 ms on a normal laptop |
| Backend response time (AI)     | < 5 s on free tier |
| UI load time | < 2 s on localhost |
| Demo coverage | All Core features shown in 5–7 minutes |
| Crash resistance | One failed command never crashes the app |

---

## 5. Constraints

- Must work with only a laptop (no extra hardware)
- Backend must run locally (for system control)
- Free tier of the default AI provider (Groq) should be sufficient
- Code should be clean and well-documented for evaluation
- Backend binds to `127.0.0.1` only (never exposed publicly)

---

## 6. Scope & Boundaries

### In Scope

- Local desktop control via a browser-based UI
- Text and voice input; spoken replies
- Pre-approved, safe-list system commands only
- AI service for conversations and non-command intents

### Out of Scope (v1)

- Multi-user / accounts and authentication
- Cloud deployment of the backend
- Arbitrary shell access from user input
- Running without a browser

---

## 7. Milestones

| Milestone | Phase | Deliverable |
|-----------|-------|-------------|
| M1 | 1 | Structure + UI shell + "Hello from AURA" API |
| M2 | 2 | Working text chat between UI and backend |
| M3 | 3 | System commands (apps, websites, time/date) |
| M4 | 4 | AI-powered answers with context |
| M5 | 5 | Full voice interaction (speak + hear replies) |
| M6 | 6 | Polished, demo-ready application |

---

## 8. Assumptions & Risks

### Assumptions

- User has Python 3.10+, Node 18+, and Chrome
- Default provider free tier (Groq) is sufficient for demos
- System commands run on the user's own laptop

### Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| AI API key missing / quota exceeded     | Graceful fallback reply + clear `.env` instructions |
| Microphone blocked by browser | Text input always available |
| System command fails (app not installed) | try-except + friendly error message |
| Port 8001/5173 busy | Documented fix in SETUP.md; port configurable via `.env` |

---

## Version

**v1.0** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added glossary, user stories, feature matrix with phase mapping, measurable targets, scope, milestones, risks. |

---

**Document Owner:** Project Developer  
**Last Updated:** 2026
