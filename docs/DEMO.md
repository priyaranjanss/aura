# AURA – Demo Script (5–7 minutes)

A step-by-step presentation script. Practice twice before the real run; keep
the chat history clear between sections (sidebar → Clear chat).

**Before you start (2 min prep):**
1. Backend running: `python run.py` in `backend/` (port 8001).
2. Frontend running: `npm run dev` in `frontend/` (http://localhost:5173).
3. Groq API key set in `backend/.env` (`AI_API_KEY=...`, `AI_PROVIDER=groq`).
4. Speaker volume on. Chrome/Edge open (for voice + wake word).
5. Close other heavy apps so commands (screenshot, apps) feel snappy.

---

## 1. Introduction (30 sec)

> "This is AURA — a voice-controlled AI assistant that runs on my laptop.
> It combines an AI brain with real computer control: I can chat with it,
> and I can tell it to do things on this machine — open apps, search the
> web, take screenshots — all in plain English."

**Do:** Point at the UI — chat on the left, mic + wake button in the input bar.

---

## 2. AI Conversation (1 min)

**Type (or say):** `what is the capital of France`

**Expected:** Request analysis card first (What/Where filled, rest "Not needed"),
then the answer, then AURA speaks it aloud.

> "Every reply starts with a full request analysis — What, When, Who, How,
> Where, Why, and the rest — marked 'Not needed' when they don't apply."

**Say:** `tell me a joke`

**Expected:** A spoken joke.

> "The AI brain answers any style of question."

---

## 3. Voice: Mic + Wake Word (1.5 min)

**Click the mic**, say: `what time is it`

**Expected:** Status pill shows Listening (green) → Thinking (amber) →
Speaking (indigo) → Idle. AURA speaks the time.

> "That was speech-to-text, then text-to-speech — the full voice loop."

**Click Wake**, say `Hello`, then say: `open notepad`

**Expected:** Wakes on "Hello", opens Notepad. After ~8 seconds it sleeps
again ("Sleeping… say 'Hello' to wake up").

> "Wake word mode keeps listening for 'Hello', then takes my next sentence as
> a command, then sleeps."

---

## 4. Computer Control + Context (2 min)

**Say/type:** `open youtube in brave`

**Expected:** YouTube opens in Brave. (Mention: "Open <site> in <browser> —
any phrasing works, the AI brain figures it out.")

**Say:** `search arijit singh songs`

**Expected:** YouTube search opens **in the same Brave tab** (context is
inherited from the previous step — same app, same browser, same tab).

**Say:** `open notepad and minimize it`

**Expected:** Notepad opens, then minimizes — a **multi-step command** in one
sentence ("Opening notepad. Minimized notepad.").

**Say:** `take a screenshot`

**Expected:** Screenshot captured and shown right in the chat bubble.

**Say:** `close notepad`

**Expected:** Notepad closes gracefully.

> "Commands are executed by safe code — the AI only suggests, Python decides
> what's allowed and does it."

---

## 5. Safety: Confirmation (30 sec)

**Say/type:** `lock the computer`

**Expected:** A confirm dialog appears — **nothing happens until confirmed**.

> "Dangerous actions — lock, shutdown, restart — always ask for confirmation
> first. Everything is validated: apps by safe name, URLs by http/https,
> typed text by safe characters."

**Do:** Click **Cancel** (so the demo keeps going).

---

## 6. Wrap-up (30 sec)

> "That's AURA: conversation, voice, computer control, multi-step commands,
> and safety — all in one local assistant. Thank you!"

**Optionally show:** Settings panel (sidebar → Settings): spoken replies
toggle, voice language (English/Hindi), clear chat.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Couldn't reach the AI service" | Check `AI_API_KEY` in `backend/.env`, then restart the backend (`Ctrl+C` → `python run.py`). Uvicorn does NOT reload `.env`. |
| Mic not working | Chrome/Edge only; allow mic permission; check the address-bar lock icon. |
| No spoken reply | Check Settings → Spoken replies is on; the browser must have had one click (autoplay rule). |
| Wake word not listening | Red error appears if mic blocked/offline. Only the focused tab can listen (browser rule). |
| Port 8001 busy | `WinError 10013` — another process holds the port; close it or change `PORT` in `.env`. |
