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
| 4     | AI Integration              | Gemini intelligence                       | 1–2 days      |
| 5     | Voice Features              | Speech-to-Text + Text-to-Speech           | 2 days        |
| 6     | Advanced UI & Polish        | Final design, settings, extra features    | 1–2 days      |

---

## Phase 1: Foundation & Basic Shell

**Goal:** Create project structure and a basic working interface.

**Tasks:**
- Create full folder structure
- Setup React + Vite + Tailwind
- Setup FastAPI backend with virtual environment
- Create basic layout (Sidebar + Main area)
- Show “AURA” title and empty chat area
- Add a simple text input box
- Make backend return “Hello from AURA”

**Deliverable:**  
You can open the website and see a clean empty assistant interface.

---

## Phase 2: Dashboard & Core Chat

**Goal:** Make real conversation work between frontend and backend.

**Tasks:**
- Create ChatWindow and ChatBubble components
- Connect frontend to `/api/chat` endpoint
- Show user messages and assistant replies
- Add loading state (“Thinking...”)
- Store messages in Zustand store
- Basic error handling

**Deliverable:**  
You can type messages and get replies from the backend.

---

## Phase 3: System Commands

**Goal:** Make the assistant control the computer.

**Tasks:**
- Create `command_service.py` and `system_service.py`
- Implement:
  - Open applications
  - Open websites
  - Search Google / YouTube
  - Tell time & date
- Add intent detection (simple keyword based)
- Test all commands thoroughly

**Deliverable:**  
Saying or typing “open chrome” actually opens Chrome.

---

## Phase 4: AI Integration (Gemini)

**Goal:** Add intelligent conversation ability.

**Tasks:**
- Integrate Google Gemini API
- Create `ai_service.py`
- Send conversation history for context
- Route non-command messages to Gemini
- Handle API errors gracefully

**Deliverable:**  
You can ask any question and get smart answers.

---

## Phase 5: Voice Features

**Goal:** Full voice interaction.

**Tasks:**
- Add Microphone button
- Use Web Speech API for Speech-to-Text
- Integrate `edge-tts` for Text-to-Speech
- Show live status (Listening / Thinking / Speaking)
- Play audio reply automatically

**Deliverable:**  
You can fully talk to AURA and it talks back.

---

## Phase 6: Advanced UI & Final Polish

**Goal:** Make the project presentation-ready.

**Tasks:**
- Improve design (colors, spacing, animations)
- Add Quick Command buttons
- Add Settings panel
- Add Clear Chat button
- Volume control + Screenshot
- Confirmation for dangerous actions
- Final testing of all features
- Prepare demo script

**Deliverable:**  
Complete, polished, demo-ready AURA assistant.

---

## Tips for Success

- Finish one phase completely before starting the next
- Test after every major feature
- Commit code to Git after each phase
- Keep the UI working at every stage
- Write small notes about what you completed each day

---

**Following these phases will help you finish the project systematically without getting overwhelmed.**
