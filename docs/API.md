# AURA – Backend API Documentation

Base URL: `http://127.0.0.1:8001`

All endpoints return JSON.

---

## 1. Health Check

**GET** `/`

Returns basic status of the backend.

**Response**
```json
{
  "status": "online",
  "message": "Hello from AURA"
}
```

**Usage:** Open http://127.0.0.1:8001/ in a browser, or:
```
curl http://127.0.0.1:8001/
```

---

## 2. Chat Endpoint (Main)

**POST** `/api/chat`

Send a user message (from voice or text). Every message is first analyzed by the **AI brain** (any phrasing): it returns a suggested intent, the question analysis, and a reply. Code validates the intent against the safe action allowlist and executes it (commands) or shows the AI's answer (conversation). Keyword detection is an offline fallback if the AI is unreachable.

> **Status:** Live since Phase 2 (placeholder reply logic; intent detection in Phase 3, AI service in Phase 4).

**Request Body**
```json
{
  "message": "open chrome",
  "history": [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "Hi! How can I help you?"}
  ]
}
```

**Response**
```json
{
  "reply": "Opening Google Chrome for you.",
  "type": "command",
  "success": true,
  "audio_url": null,
  "analysis": [
    {"question": "What", "answer": "Open the 'chrome' application"},
    {"question": "When", "answer": "Not needed"},
    {"question": "Who", "answer": "Not needed"},
    {"question": "How", "answer": "Launch via the operating system's app launcher"},
    {"question": "Where", "answer": "Not needed"},
    {"question": "Why", "answer": "Not needed"},
    {"question": "Which", "answer": "Not needed"},
    {"question": "Whose", "answer": "Not needed"},
    {"question": "Whom", "answer": "Not needed"},
    {"question": "How much", "answer": "Not needed"}
  ]
}
```

**Response Fields**

| Field | Type | Meaning |
|-------|------|---------|
| `reply` | string | The assistant's text reply (shown and/or spoken) |
| `type` | string | `"command"` (system action) or `"ai"` (AI reply) |
| `success` | boolean | Whether the action/reply succeeded |
| `audio_url` | string \| null | URL to TTS audio (edge-tts mp3 served from `/static/audio/`); `null` when speech is skipped (e.g. reply too long or TTS offline) |
| `analysis` | array | Request analysis shown before the reply: `{question, answer}` pairs for What/When/Who/How/Where/Why/Which/Whose/Whom/How much — each answered or `"Not needed"` |

**Example (curl)**
```
curl -X POST http://127.0.0.1:8001/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"what time is it\", \"history\": []}"
```

---

## 3. Available Commands Reference

These are examples of messages the backend understands (live since Phase 3):

| User Message                  | Action                          |
|-------------------------------|---------------------------------|
| open chrome                   | Opens Google Chrome             |
| open notepad and minimize it  | Opens Notepad, then minimizes it (multi-step) |
| minimize notepad              | Minimizes Notepad (also "minimise X") |
| close brave                   | Closes Brave (also "quit/exit X") |
| write hello                   | Types "hello" into the active app (context-aware) |
| open notepad                  | Opens Notepad                   |
| open vs code                  | Opens Visual Studio Code        |
| open youtube                  | Opens YouTube                   |
| open youtube in brave         | Opens YouTube in Brave/Chrome/Firefox/Edge |
| search google for cats        | Searches Google                 |
| play music on youtube         | Opens YouTube music search      |
| what time is it               | Returns current time            |
| increase volume               | Increases system volume         |
| decrease volume               | Decreases system volume         |
| mute                          | Mutes volume                    |
| take screenshot               | Captures and saves screenshot   |
| lock computer                 | Locks the session               |

> **Note:** volume, screenshot and lock land in Phase 6; the rest are live since Phase 3.
>
> "open <anything>" also works for any installed app by name (name is validated:
> letters/digits/spaces only — paths and shell metacharacters are rejected).

---

## 4. System Status (Optional)

**GET** `/api/status`

Returns current backend status and loaded services.

**Planned response**
```json
{
  "status": "online",
  "services": ["command", "ai", "speech"],
  "ai_configured": true,
  "version": "0.1.0"
}
```

> **Status:** Planned — not implemented yet.

---

## 5. Delete Audio (after playback)

**DELETE** `/api/audio/{filename}`

Deletes a generated TTS file once the frontend has played it, so the audio
folder stays clean. The frontend calls this automatically when playback ends
(or fails).

| Case | Result |
|------|--------|
| Valid generated file (32-hex + `.mp3`) | `200` → `{"deleted": true}` |
| Unknown / already-deleted file | `404` |
| Anything else (path traversal, arbitrary names) | `404` (strictly validated) |

Orphaned files (e.g. a tab closed mid-playback) are swept automatically when
a new file is generated (files older than 1 hour).

---

## 6. WebSocket (Future / Advanced)

**WS** `/ws/status`

Used for real-time status updates (Listening, Thinking, Speaking).

> **Status:** Optional, planned for Phase 5.

---

## 7. Error Response Format

```json
{
  "reply": "Sorry, I couldn't process that request.",
  "type": "error",
  "success": false,
  "detail": "Optional error message"
}
```

### Error Scenarios

| Scenario | HTTP Status | Response |
|----------|-------------|----------|
| Missing/invalid `message` field | 422 | FastAPI validation error |
| Command failed at runtime | 200 | `success: false` + friendly `reply` |
| AI API key missing / provider error | 200 | `type: "error"`, `success: false` + friendly reply |
| Server exception | 500 | `success: false` + generic message |

---

## 8. CORS

The backend enables CORS for **any origin** (`allow_origins=["*"]`) during
development. This is safe because the server binds to `127.0.0.1` only, so
only pages running on this machine can reach it. No credentials are used
(`allow_credentials=False`).

---

## Notes for Developers

- Always send the `message` field.
- `history` is optional but recommended for better AI context — the AI uses it for follow-ups (e.g. after "open youtube in brave", "search X" becomes a YouTube search in Brave).
- Keep messages reasonably short for best performance.
- Dangerous actions (shutdown/restart) should be confirmed on the frontend before calling the API.
- Backend must stay on `127.0.0.1` — never expose it publicly.

---

## Version

**v1.1** — Last updated: 2026-08-16

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-08-16 | Initial API reference |
| v1.1 | 2026-08-16 | Base URL updated to port 8001; added response field table, curl examples, error scenario table, planned-status notes. |
| v1.2 | 2026-08-16 | `/api/chat` implemented (Phase 2); removed "planned" status. |
| v1.3 | 2026-08-16 | CORS now allows any local origin (dev-permissive; server bound to 127.0.0.1). |
| v1.4 | 2026-08-16 | Commands live (Phase 3): open apps/websites, search Google/YouTube/Wikipedia, time & date. |
| v1.5 | 2026-08-16 | Added `analysis` field to responses (What/When/Who/How/Where/... with "Not needed" defaults). |
| v1.6 | 2026-08-16 | Added "open <website> in <browser>" command (App Paths on Windows, fallback to default browser). |
| v1.7 | 2026-08-16 | Added "close/quit/exit <app>" (graceful quit via taskkill/osascript/pkill). |

---
