"""AI service — provider-agnostic "AI brain".

The chat route calls generate_reply(); the provider is selected from config
(AI_PROVIDER) so Groq, Gemini, OpenAI, Ollama, etc. can be swapped without
touching the rest of the app. Providers are imported lazily so the backend
runs even if a provider package is not installed.

Every reply is structured: the model first analyzes the request across the
question dimensions (What/When/Who/How/Where/Why/Which/Whose/Whom/How much,
answering "Not needed" when a dimension does not apply), then gives the final
answer. The output is parsed into {"reply", "analysis"} with a safe fallback.

Safety boundary (docs/RULES.md): providers only return TEXT. They never
execute anything on the machine.
"""

import json
import re
from abc import ABC, abstractmethod

from app import config

# System prompt shared by all providers. The AI analyzes EVERY request
# (question dimensions + intent) and returns strict JSON. It only suggests
# actions — Python code validates and executes them (docs/RULES.md).
SYSTEM_PROMPT = (
    "You are AURA, a helpful, friendly voice assistant that runs on the user's laptop. "
    "For every user request, first analyze it across these dimensions: "
    "What, When, Who, How, Where, Why, Which, Whose, Whom, How much. "
    'Answer each dimension in one short phrase, or "Not needed" if it does not apply. '
    "Then detect the intent. The user may phrase commands in any style "
    "(\"open youtube in brave\", \"launch chrome\", \"what's the time\", "
    "\"search the web for cats\", \"play some music\"). "
    "Use the conversation history for follow-up context, for ANY app or site: "
    "a short follow-up inherits the last opened app/site. Examples: after opening "
    "Notepad, \"write hello\" means type into Notepad and \"close\" means close "
    "Notepad; after opening YouTube, \"search arijit singh\" means a YouTube search, "
    "and if it was opened in a browser, use that same browser. Always fill the "
    "inherited target/app/browser explicitly in the command. "
    "You can only request these actions (Python code executes them, you never touch the system): "
    "- open_app (target = installed app name, e.g. chrome, notepad) "
    "- close_app (target = installed app name, e.g. brave, notepad) "
    "- minimize_app (target = running app name, e.g. notepad, brave) "
    "- type_text (target = the text to type, app = the app to type into, usually inherited) "
    "- open_website (target = a known website: google, youtube, gmail, wikipedia, github, "
    "stack overflow, maps, news — or a plain http(s) URL) "
    "- open_website_in_browser (target = website as above, browser = brave, chrome, firefox, edge, default) "
    "- search_google / search_youtube / search_wikipedia (target = the search query) "
    "- tell_time / tell_date "
    "If the request is not one of these actions, set steps to an empty array and answer normally. "
    "Compound requests get MULTIPLE steps, one action per step. For example \"open notepad "
    "and minimize it\" becomes two steps: first {action: open_app, target: notepad}, then "
    "{action: minimize_app, target: notepad}. Repeat the app/site name explicitly in every "
    "step — never use words like \"it\", \"that\", or \"there\" as a target. "
    'Respond with ONLY valid JSON in exactly this shape: '
    '{"analysis": {"what": "...", "when": "...", "who": "...", "how": "...", '
    '"where": "...", "why": "...", "which": "...", "whose": "...", "whom": "...", '
    '"how much": "..."}, '
    '"steps": [{"action": "...", "target": "...", "app": "...", "browser": "..."}] '
    '(empty array when no command), '
    '"reply": "..."}. The reply is a short confirmation for commands '
    '(e.g. "Opened YouTube in Brave.") and a full answer for conversations. '
    "Do not include any text outside the JSON."
)


def _parse_structured(text: str) -> dict:
    """Extract {"reply", "analysis", "command", "steps"} from the model output.

    Falls back to the raw text when the model does not return valid JSON.
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)

    data = None
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                data = None

    if not isinstance(data, dict):
        return {"reply": text.strip(), "analysis": None, "command": None, "steps": None}

    reply = data.get("reply")
    analysis = data.get("analysis")
    command = data.get("command")
    if not reply:
        return {"reply": text.strip(), "analysis": None, "command": None, "steps": None}
    if not isinstance(analysis, dict):
        analysis = None
    if not isinstance(command, dict):
        command = None

    # Steps array (compound commands). Falls back to a single "command" for
    # older-model responses.
    steps = data.get("steps")
    if isinstance(steps, list):
        steps = [s for s in steps if isinstance(s, dict)] or None
    else:
        steps = None
    if steps is None and command is not None:
        steps = [command]

    return {
        "reply": str(reply).strip(),
        "analysis": analysis,
        "command": command,
        "steps": steps,
    }


class AIProvider(ABC):
    """A text-generation backend (an "AI brain")."""

    name = "base"

    @abstractmethod
    def generate(self, message: str, history: list) -> str:
        """Return the model's raw output for the message + history."""


class GroqProvider(AIProvider):
    """Groq (https://console.groq.com) via its OpenAI-compatible endpoint."""

    name = "groq"
    url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, message: str, history: list) -> str:
        import requests  # lazy import

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(
            {"role": item["role"], "content": item["content"]} for item in history
        )
        messages.append({"role": "user", "content": message})

        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {config.AI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": config.AI_MODEL or "llama-3.3-70b-versatile",
                "messages": messages,
                "temperature": 0.7,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()


class GeminiProvider(AIProvider):
    """Google Gemini via the google-generativeai package."""

    name = "gemini"

    def generate(self, message: str, history: list) -> str:
        import google.generativeai as genai  # lazy import

        genai.configure(api_key=config.AI_API_KEY)
        model = genai.GenerativeModel(
            config.AI_MODEL or "gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT,
        )
        parts = [f"{item['role']}: {item['content']}" for item in history]
        parts.append(f"user: {message}")
        response = model.generate_content("\n".join(parts))
        return response.text.strip()


class OpenAIProvider(AIProvider):
    """OpenAI-compatible chat completions API."""

    name = "openai"

    def generate(self, message: str, history: list) -> str:
        from openai import OpenAI  # lazy import

        client = OpenAI(api_key=config.AI_API_KEY)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(
            {"role": item["role"], "content": item["content"]} for item in history
        )
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model=config.AI_MODEL or "gpt-4o-mini",
            messages=messages,
        )
        return response.choices[0].message.content.strip()


class OllamaProvider(AIProvider):
    """Local Ollama server (http://localhost:11434) — fully offline."""

    name = "ollama"

    def generate(self, message: str, history: list) -> str:
        import requests  # lazy import

        prompt = "\n".join(
            [f"{item['role']}: {item['content']}" for item in history]
            + [f"user: {message}"]
        )
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": config.AI_MODEL or "llama3.2",
                "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()


_PROVIDERS = {
    provider.name: provider
    for provider in (GroqProvider, GeminiProvider, OpenAIProvider, OllamaProvider)
}


def get_provider() -> AIProvider:
    """Return the provider selected by AI_PROVIDER in .env."""
    provider = _PROVIDERS.get(config.AI_PROVIDER)
    if provider is None:
        raise ValueError(
            f"Unknown AI provider '{config.AI_PROVIDER}'. "
            f"Choose one of: {', '.join(_PROVIDERS)}"
        )
    return provider()


def generate_reply(message: str, history: list) -> dict:
    """Ask the configured AI provider for a structured reply.

    Returns {"reply": str, "analysis": dict | None, "command": dict | None}.
    """
    raw = get_provider().generate(message, history)
    return _parse_structured(raw)
