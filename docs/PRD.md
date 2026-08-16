# PRD.md – Project Requirements Document

**Project Name:** AURA – Advanced Universal Response Assistant  
**Version:** 1.0  
**Type:** Fullstack AI Voice Assistant (Desktop Control)

---

## 1. What to Build

AURA is a fullstack AI-powered Voice Assistant that runs locally on a user’s laptop.  

It allows the user to:

- Control the computer using voice or text commands
- Open applications and websites
- Search the web and play music
- Ask intelligent questions and get spoken answers
- Manage system settings (volume, screenshot, lock, etc.)

The application has two main parts:

1. **Frontend** → Modern React web interface (chat + microphone)
2. **Backend** → Python FastAPI server that controls the computer and talks to Google Gemini AI

The entire system runs on the user’s own laptop (no cloud deployment needed for core features).

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

---

## 3. Features

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

- Wake word (“Hey Aura”)
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

---

## 5. Constraints

- Must work with only a laptop (no extra hardware)
- Backend must run locally (for system control)
- Free tier of Google Gemini should be sufficient
- Code should be clean and well-documented for evaluation

---

**Document Owner:** Project Developer  
**Last Updated:** 2026
