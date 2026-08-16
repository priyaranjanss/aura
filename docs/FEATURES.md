# AURA – Complete Feature List

**This is the single source of truth for AURA features.** Other docs
(README, PRD, API, PHASES) point here instead of duplicating feature lists.
Every feature, its status, and the phase it landed in lives in this file.

**Status legend:** ✅ Done · 🚧 In progress · ⬜ Planned (phase) · 🔮 Future

---

## 1. Voice Interaction Features

| Feature | Status |
|---------|--------|
| Speak commands using the laptop microphone | ✅ Phase 5 |
| Text input as alternative to voice | ✅ Phase 2 |
| High-quality natural Text-to-Speech replies | ✅ Phase 5 (edge-tts) |
| Real-time status feedback (Listening → Thinking → Speaking) | ✅ Phase 5 |
| Support for continuous conversation | ✅ Phase 4 |
| Wake word ("Hello" / "Hey AURA" / etc.) + auto-sleep | ✅ Phase 5 (Wake toggle, continuous listening) |
| Mic permission / offline errors surface visibly (not silent) | ✅ Phase 5 |

---

## 2. Computer Control Features

### Application Control
| Feature | Status |
|---------|--------|
| Open Chrome / Edge / Firefox | ✅ Phase 3 |
| Open VS Code | ⬜ Future (add to safe list) |
| Open Notepad / TextEdit | ✅ Phase 3 |
| Open Calculator | ✅ Phase 3 |
| Open File Explorer / Finder | ✅ Phase 3 |
| Open Spotify | ⬜ Future (add to safe list) |
| Open any installed application by name | ✅ Phase 4 (validated generic opener) |
| Open Windows system tools (Device Manager, Task Manager, Settings, Disk Management, Services…) | ✅ Phase 4 (devmgmt.msc etc.) |
| Close applications ("close brave", "quit chrome") | ✅ Phase 4 |
| Minimize applications ("minimize notepad") | ✅ Phase 4 (ctypes + UWP support) |
| Type/write into apps ("write hello" after opening Notepad) | ✅ Phase 4 (pyautogui, safe text) |
| Multi-step commands ("open notepad and minimize it") | ✅ Phase 4 (steps array) |

### Web & Search
| Feature | Status |
|---------|--------|
| Open Google, YouTube, Gmail, Wikipedia, GitHub, etc. | ✅ Phase 3 |
| Search Google by voice/text | ✅ Phase 3 |
| Search YouTube | ✅ Phase 3 |
| Search Wikipedia and get summary | ⬜ Phase 6 (summary) · ✅ Phase 3 (open search) |
| Search Windows itself ("search hello in windows") | ✅ Phase 4 (Win key + type) |

### Media & System
| Feature | Status |
|---------|--------|
| Play music on YouTube | ✅ Phase 3 |
| Increase / Decrease / Mute / Unmute volume | ✅ Phase 6 |
| Take screenshot and save it | ✅ Phase 6 (shown in chat) |
| Tell current time | ✅ Phase 3 |
| Tell current date | ✅ Phase 3 |
| Lock the computer | ✅ Phase 6 (asks confirmation first) |
| Shutdown computer (with confirmation) | ✅ Phase 6 |
| Restart computer (with confirmation) | ✅ Phase 6 |

---

## 3. AI Intelligence Features

| Feature | Status |
|---------|--------|
| Powered by a pluggable AI service (Groq active; Gemini/OpenAI/Ollama swappable) | ✅ Phase 4 |
| Natural language understanding | ✅ Phase 4 |
| Context-aware conversations (remembers previous messages) | ✅ Phase 4 |
| Answer general knowledge questions | ✅ Phase 4 |
| Tell jokes, fun facts, motivational quotes | ✅ Phase 4 |
| Explain topics in simple language | ✅ Phase 4 |
| Multilingual TTS (English + Hindi voice) | ✅ Phase 6 (Settings -> Voice language) |
| Smart intent detection (system action vs conversation) | ✅ Phase 4 (AI brain, any phrasing) + keyword fallback |
| Command confirmations use completed wording ("Opened notepad.", not "Opening…") | ✅ Phase 6 |
| Request analysis before every reply (What/When/Who/How/Where/Why/Which/Whose/Whom/How much, "Not needed" when not applicable) | ✅ Phase 3 |

---

## 4. User Interface Features

### Main Interface
| Feature | Status |
|---------|--------|
| Clean modern dark theme | ✅ Phase 1 |
| Chat-style message bubbles (User + Assistant) | ✅ Phase 2 |
| Large animated microphone button | ✅ Phase 5 |
| Text input box with send button | ✅ Phase 2 |
| Live status indicator with colors | ✅ Phase 5 (Listening/Thinking/Speaking/Idle) |
| Scrollable chat history | ✅ Phase 2 |

### Extra UI Elements
| Feature | Status |
|---------|--------|
| Sidebar | ✅ Phase 1 (shell) |
| Quick command buttons (What time is it, Open Notepad, Take a screenshot, etc.) | ✅ Phase 6 |
| Settings panel (spoken replies, voice language, clear chat) | ✅ Phase 6 |
| Clear chat button | ✅ Phase 6 (sidebar + settings) |
| Confirmation dialog for dangerous actions (lock/shutdown/restart) | ✅ Phase 6 |
| Message entrance animations | ✅ Phase 6 |
| Theme toggle (Dark / Light) – optional | 🔮 Future |
| Responsive design (works on different screen sizes) | ⬜ Phase 6 (partial — desktop-first) |

---

## 5. Technical Features

| Feature | Status |
|---------|--------|
| Fullstack architecture (React + FastAPI) | ✅ Phase 1 |
| State management with Zustand | ✅ Phase 2 |
| Real-time communication | ⬜ Phase 5 (WebSocket optional) |
| Environment-based configuration | ✅ Phase 1 (`.env` + config.py) |
| Error handling with friendly messages | ✅ Phase 2 (basic) |
| Modular code structure (easy to extend) | ✅ Phase 1 |
| Local execution (full control over the laptop) | ✅ Phase 1 |
| Secure API key handling via `.env` | ✅ Phase 1 |
| TTS audio files deleted after playback (auto-cleanup) | ✅ Phase 5 (DELETE /api/audio + 1h orphan sweep) |

---

## 6. Future / Advanced Features (Can be added later)

- Wake word "Hello" without keeping the tab focused (needs a desktop app)
- Face recognition for security
- Offline mode using local LLM (Ollama)
- Custom command creation by user
- Voice cloning
- Mobile companion app
- Plugin system
- Multi-user support
- Activity logging and analytics

---

## Feature Priority for Development

**Phase 1 (MVP foundation) — ✅ Done**
- Project structure, UI shell, hello API

**Phase 2**
- Text chat
- Chat history
- Backend connection

**Phase 3**
- Basic system commands (open apps & websites)
- Time & date

**Phase 4**
- AI replies
- Context awareness

**Phase 5**
- Voice input
- Text-to-Speech
- Status indicators

**Phase 6**
- Volume control + Screenshot
- Settings panel, quick commands, polish
- Confirmation for dangerous actions

---

## Version

**v1.0** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added status column per feature mapped to phases, priority section aligned with PHASES.md. |
| v1.1 | 2026-08-16 | Marked Phase 2 chat features as done (bubbles, history, Zustand, basic errors). |
| v1.2 | 2026-08-16 | Marked Phase 3 system commands as done (apps, websites, search, time/date). |
| v1.3 | 2026-08-16 | Added request-analysis feature (all question dimensions answered before the reply). |
| v1.4 | 2026-08-16 | Marked Phase 4 AI features as done (Groq provider, context, structured analysis). |
| v1.5 | 2026-08-16 | Marked Phase 5 voice features as done (mic STT, edge-tts TTS, status pill). |
| v1.6 | 2026-08-16 | Added missing features (audio auto-delete, done-format replies, mic error surfacing); declared single source of truth. |

---
