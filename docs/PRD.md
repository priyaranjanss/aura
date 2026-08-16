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
2. **Backend** → Python FastAPI server that controls the computer and talks to Google Gemini AI

The entire system runs on the user's own laptop (no cloud deployment needed for core features).

### Glossary

| Term | Meaning |
|------|---------|
| AURA | The assistant product as a whole (frontend + backend) |
| Command | A message that maps to a system action (e.g. "open chrome") |
| Conversation | A message that should be answered by Gemini AI |
| Intent Detection | The backend logic that decides command vs conversation |
| TTS / STT | Text-to-Speech / Speech-to-Text |

---

## 2. Targeted Users

| User Type                    | Description                                      | Why they need AURA                          |
|-----------------------------|--------------------------------------------------|---------------------------------------------|
| Students (CSE / IT)         | College students doing final year projects       | Perfect fullstack + AI + system control project |
| Developers & Programmers    | People who want hands-free computer control      | Increase productivity while coding          |
| Productivity Seekers        | Anyone who wants to control PC by voice          | Reduce mouse/keyboard usage                 |
| AI Enthusiasts              | People learning AI, voice interfaces, LLMs       | Practical hands-on experience with Gemini + Speech |
| Demo / Presentation Users   | Students presenting projects                     | Impressive live demo of AI controlling PC   |

**Primary Focus:** Computer Science Engineering students who need a complete, impressive, and realistic project.

### User Stories

- As a **student**, I can open apps and websites by voice so my demo looks impressive.
- As a **developer**, I can ask general questions and get Gemini answers while keeping my hands on the keyboard.
- As a **productivity seeker**, I can control volume, take screenshots, and lock my PC with one command.
- As an **AI enthusiast**, I can see the full pipeline: voice → intent → AI/system → spoken reply.
- As a **demo presenter**, I can fall back to typed input if the microphone fails.

---

## 3. Features

### Feature Matrix (Priority → Phase)

| # | Feature                       | Priority | Phase |
|---|-------------------------------|----------|-------|
| 1 | Text input chat               | Core     | 2     |
| 2 | Chat history in UI            | Core     | 2     |
| 3 | Open applications             | Core     | 3     |
| 4 | Open websites                 | Core     | 3     |
| 5 | Search Google / YouTube / Wikipedia | Core | 3     |
| 6 | Tell time & date              | Core     | 3     |
| 7 | Intelligent conversation (Gemini) | Core  | 4     |
| 8 | Voice input (Web Speech API)  | Core     | 5     |
| 9 | Text-to-Speech (edge-tts)     | Core     | 5     |
| 10 | Real-time status (Listening/Thinking/Speaking) | Core | 5 |
| 11 | Volume control                | Should   | 6     |
| 12 | Screenshot                    | Should   | 6     |
| 13 | Quick command buttons         | Should   | 6     |
| 14 | Settings panel                | Should   | 6     |
| 15 | Multilingual (English + Hindi) | Should  | 6     |
| 16 | Confirmation for dangerous actions | Should | 6 |
| 17 | Error handling with friendly replies | Should | 2–6 |
| 18 | Conversation memory           | Should   | 4     |
| 19 | Wake word ("Hey Aura")        | Nice-to-have | Future |
| 20 | Offline mode (local LLM)      | Nice-to-have | Future |
| 21 | Custom user-defined commands  | Nice-to-have | Future |
| 22 | Face recognition unlock       | Nice-to-have | Future |
| 23 | Mobile companion app          | Nice-to-have | Future |

### Core Features (Must Have)

- Voice input using laptop microphone
- Text input as alternative
- Text-to-Speech (assistant speaks replies)
- Open applications (Chrome, VS Code, Notepad, Calculator, etc.)
- Open websites (Google, YouTube, Gmail, Wikipedia…)
- Search Google / YouTube / Wikipedia
- Play music on YouTube
- Tell current time and date
- Volume control (up / down / mute)
- Take screenshot
- Intelligent conversation using Google Gemini
- Chat history in the UI
- Real-time status (Listening / Thinking / Speaking)
- Modern dark-themed React UI

### Advanced Features (Should Have)

- Quick command buttons
- Settings panel
- Multilingual support (English + Hindi)
- Confirmation before dangerous actions (shutdown / restart)
- Lock computer
- Error handling with friendly voice replies
- Conversation memory (context awareness)

### Future Features (Nice to Have)

- Wake word ("Hey Aura")
- Offline mode with local LLM
- Custom user-defined commands
- Face recognition unlock
- Mobile companion app

---

## 4. Success Criteria

The project will be considered successful when:

1. User can control the computer completely by voice
2. Gemini AI gives intelligent and useful answers
3. UI looks modern and professional
4. System works reliably on a normal laptop
5. Student can demonstrate all major features live in 5–7 minutes

### Measurable Targets

| Criterion | Target |
|-----------|--------|
| Backend response time (command) | < 500 ms on a normal laptop |
| Backend response time (Gemini) | < 5 s on free tier |
| UI load time | < 2 s on localhost |
| Demo coverage | All Core features shown in 5–7 minutes |
| Crash resistance | One failed command never crashes the app |

---

## 5. Constraints

- Must work with only a laptop (no extra hardware)
- Backend must run locally (for system control)
- Free tier of Google Gemini should be sufficient
- Code should be clean and well-documented for evaluation
- Backend binds to `127.0.0.1` only (never exposed publicly)

---

## 6. Scope & Boundaries

### In Scope

- Local desktop control via a browser-based UI
- Text and voice input; spoken replies
- Pre-approved, safe-list system commands only
- Gemini for conversations and non-command intents

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
| M4 | 4 | Gemini-powered answers with context |
| M5 | 5 | Full voice interaction (speak + hear replies) |
| M6 | 6 | Polished, demo-ready application |

---

## 8. Assumptions & Risks

### Assumptions

- User has Python 3.10+, Node 18+, and Chrome
- Gemini free tier is sufficient for demos
- System commands run on the user's own laptop

### Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Gemini API key missing / quota exceeded | Graceful fallback reply + clear `.env` instructions |
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
