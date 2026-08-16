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

Send a user message (from voice or text). The backend will either execute a system command or reply using Gemini.

> **Status:** Live since Phase 2 (placeholder reply logic; intent detection in Phase 3, Gemini in Phase 4).

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
  "audio_url": null
}
```

**Response Fields**

| Field | Type | Meaning |
|-------|------|---------|
| `reply` | string | The assistant's text reply (shown and/or spoken) |
| `type` | string | `"command"` (system action) or `"ai"` (Gemini reply) |
| `success` | boolean | Whether the action/reply succeeded |
| `audio_url` | string \| null | URL to TTS audio (Phase 5; `null` until then) |

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
| open notepad                  | Opens Notepad                   |
| open vs code                  | Opens Visual Studio Code        |
| open youtube                  | Opens YouTube                   |
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
  "gemini_configured": true,
  "version": "0.1.0"
}
```

> **Status:** Planned — not implemented yet.

---

## 5. WebSocket (Future / Advanced)

**WS** `/ws/status`

Used for real-time status updates (Listening, Thinking, Speaking).

> **Status:** Optional, planned for Phase 5.

---

## 6. Error Response Format

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
| Gemini API key missing | 200 | `success: false` + fallback reply |
| Server exception | 500 | `success: false` + generic message |

---

## 7. CORS

The backend enables CORS for **any origin** (`allow_origins=["*"]`) during
development. This is safe because the server binds to `127.0.0.1` only, so
only pages running on this machine can reach it. No credentials are used
(`allow_credentials=False`).

---

## Notes for Developers

- Always send the `message` field.
- `history` is optional but recommended for better AI context.
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

---
