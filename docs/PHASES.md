# phases.md – Project Development Phases

Break the entire AURA project into clear, manageable phases.
Complete one phase fully before moving to the next.

---

## Phase Overview

| Phase | Name                        | Goal                                      | Estimated Time |
|-------|-----------------------------|-------------------------------------------|----------------|
| 1     | Foundation & Login/UI Shell | Basic structure + simple UI               | 1–2 days      |
| 2     | Dashboard & Core Chat       | Working chat interface + backend connection | 1–2 days    |
| 3     | System Commands             | Computer control features                 | 2 days        |
| 4     | AI Integration              | AI intelligence (Gemini default)          | 1–2 days      |
| 5     | Voice Features              | Speech-to-Text + Text-to-Speech           | 2 days        |
| 6     | Advanced UI & Polish        | Final design, settings, extra features    | 1–2 days      |

---

## Progress Tracker

| Phase | Name                        | Status              | Completed |
|-------|-----------------------------|---------------------|-----------|
| 1     | Foundation & Basic Shell    | ✅ Done             | 2026-08-16 |
| 2     | Dashboard & Core Chat       | ✅ Done             | 2026-08-16 |
| 3     | System Commands             | ✅ Done             | 2026-08-16 |
| 4     | AI Integration              | ✅ Done             | 2026-08-16 |
| 5     | Voice Features              | ✅ Done             | 2026-08-16 |
| 6     | Advanced UI & Polish        | ✅ Done             | 2026-08-16 |

> Keep this table updated. Details of completed work live in `docs/memory.md`.
> For the current status of every feature, see [FEATURES.md](FEATURES.md) —
> the single source of truth (phases here list *tasks*, not features).

---

## Phase 1: Foundation & Basic Shell ✅

**Goal:** Create project structure and a basic working interface.

**Tasks:**
- [x] Create full folder structure
- [x] Setup React + Vite + Tailwind
- [x] Setup FastAPI backend with virtual environment
- [x] Create basic layout (Sidebar + Main area)
- [x] Show "AURA" title and empty chat area
- [x] Add a simple text input box
- [x] Make backend return "Hello from AURA"

**Deliverable:** You can open the website and see a clean empty assistant interface.

**Acceptance Criteria**
- [x] `GET http://127.0.0.1:8001/` returns `{"status": "online", "message": "Hello from AURA"}`
- [x] Frontend opens at http://localhost:5173 showing sidebar + chat area + input box
- [x] `npm run build` completes without errors
- [x] Backend starts via `python run.py` on port 8001

---

## Phase 2: Dashboard & Core Chat ✅

**Goal:** Make real conversation work between frontend and backend.

**Tasks:**
- [x] Create ChatWindow and ChatBubble components
- [x] Connect frontend to `/api/chat` endpoint
- [x] Show user messages and assistant replies
- [x] Add loading state ("Thinking...")
- [x] Store messages in Zustand store
- [x] Basic error handling

**Deliverable:** You can type messages and get replies from the backend.

**Acceptance Criteria**
- [x] Typing a message and pressing Enter shows it as a user bubble
- [x] Backend reply appears as an assistant bubble
- [x] "Thinking..." indicator shows while waiting
- [x] Chat history survives component re-renders (Zustand)
- [x] Backend errors show a friendly message instead of crashing

---

## Phase 3: System Commands ✅

**Goal:** Make the assistant control the computer.

**Tasks:**
- [x] Create `command_service.py` and `system_service.py`
- [x] Implement: open applications
- [x] Implement: open websites
- [x] Implement: search Google / YouTube
- [x] Implement: tell time & date
- [x] Add intent detection (simple keyword based)
- [x] Test all commands thoroughly

**Deliverable:** Saying or typing "open chrome" actually opens Chrome.

**Acceptance Criteria**
- [x] "open chrome" opens Chrome
- [x] "open youtube" opens YouTube in the browser
- [x] "search google for cats" opens a Google search
- [x] "what time is it" returns the current time
- [x] Unknown commands fall through to conversation (Phase 4)
- [x] Every command failure returns a friendly message

---

## Phase 4: AI Integration (AI Service) ✅

**Goal:** Add intelligent conversation ability.

**Tasks:**
- [x] Integrate the AI service (default provider: Groq; Gemini/OpenAI/Ollama swappable)
- [x] Create `ai_service.py` (provider-agnostic)
- [x] Send conversation history for context
- [x] Route non-command messages to the AI service
- [x] AI replies include the same request analysis format (What/When/Who/How/... first, "Not needed" when not applicable)
- [x] Handle API errors gracefully

**Deliverable:** You can ask any question and get smart answers.

**Acceptance Criteria**
- [x] General questions get intelligent answers
- [x] Conversation context is remembered (history sent)
- [x] Missing/invalid API key shows a friendly fallback
- [x] Command routing still wins over AI for system intents

---

## Phase 5: Voice Features ✅

**Goal:** Full voice interaction.

**Tasks:**
- [x] Add Microphone button
- [x] Use Web Speech API for Speech-to-Text
- [x] Integrate `edge-tts` for Text-to-Speech
- [x] Show live status (Listening / Thinking / Speaking)
- [x] Play audio reply automatically

**Deliverable:** You can fully talk to AURA and it talks back.

**Acceptance Criteria**
- [x] Clicking the mic captures speech → text
- [x] Text appears in the chat and gets answered
- [x] The reply is spoken aloud (edge-tts audio)
- [x] Status pill shows Listening (green), Thinking (amber), Speaking (indigo)
- [x] Text input still works if the microphone is blocked

---

## Phase 6: Advanced UI & Final Polish ✅

**Goal:** Make the project presentation-ready.

**Tasks:**
- [x] Improve design (colors, spacing, animations)
- [x] Add Quick Command buttons
- [x] Add Settings panel
- [x] Add Clear Chat button
- [x] Volume control + Screenshot
- [x] Confirmation for dangerous actions
- [x] Final testing of all features
- [x] Prepare demo script (see `docs/DEMO.md`)

**Deliverable:** Complete, polished, demo-ready AURA assistant.

**Acceptance Criteria**
- [x] Full 5–7 minute demo runs without failure (script in docs/DEMO.md)
- [x] Volume up/down/mute work
- [x] Screenshot saves to disk
- [x] Shutdown/restart/lock ask for confirmation first
- [x] UI matches docs/DESIGN.md tokens
- [x] README + docs final and accurate

---

## Dependencies Between Phases

- Phase 2 needs Phase 1 (structure + backend).
- Phase 3 builds on Phase 2's chat routing (command replies appear in chat).
- Phase 4 needs Phase 3's intent detection (fallback for non-commands).
- Phase 5 needs Phase 4 (spoken answers) and Phase 2 (chat UI).
- Phase 6 builds on everything.

> Phase 6 complete: see the progress tracker below and docs/DEMO.md for the
> presentation script.

---

## Definition of Done (per phase)

1. All phase tasks checked off
2. Acceptance criteria pass
3. Backend + frontend both run without errors
4. `npm run build` passes
5. Phase logged in `docs/memory.md`
6. Progress table in this file updated
7. Changes committed to Git

---

## Tips for Success

- Finish one phase completely before starting the next
- Test after every major feature
- Commit code to Git after each phase
- Keep the UI working at every stage
- Write small notes about what you completed each day

---

## Version

**v1.0** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Expanded: added progress tracker, acceptance criteria per phase, dependency map, definition of done. |
| v1.1 | 2026-08-16 | Marked Phase 2 complete (chat wired frontend ↔ backend). |
| v1.2 | 2026-08-16 | Marked Phase 3 complete (system commands: apps, websites, search, time/date). |
| v1.3 | 2026-08-16 | Marked Phase 4 complete (AI integration with Groq provider). |
| v1.4 | 2026-08-16 | Marked Phase 5 complete (voice: STT via Web Speech API, TTS via edge-tts). |

---

**Following these phases will help you finish the project systematically without getting overwhelmed.**
