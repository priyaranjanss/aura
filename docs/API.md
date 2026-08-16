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
  "message": "AURA Backend is running"
}
```

---

## 2. Chat Endpoint (Main)

**POST** `/api/chat`

Send a user message (from voice or text). The backend will either execute a system command or reply using Gemini.

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
  "type": "command",          // or "ai"
  "success": true,
  "audio_url": null           // optional future field
}
```

---

## 3. Available Commands Reference

These are examples of messages the backend understands:

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

---

## 4. System Status (Optional)

**GET** `/api/status`

Returns current backend status and loaded services.

---

## 5. WebSocket (Future / Advanced)

**WS** `/ws/status`

Used for real-time status updates (Listening, Thinking, Speaking).

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

---

## 7. CORS

The backend enables CORS for `http://localhost:5173` so the React frontend can communicate freely during development.

---

## Notes for Developers

- Always send the `message` field.
- `history` is optional but recommended for better AI context.
- Keep messages reasonably short for best performance.
- Dangerous actions (shutdown/restart) should be confirmed on the frontend before calling the API.
