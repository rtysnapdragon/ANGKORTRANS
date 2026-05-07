"""
AI Service — Google Gemini REST API with multi-model fallback.
Tries models in order until one works (handles quota exhaustion).
Free tier models: gemini-1.5-flash, gemini-1.0-pro, gemini-pro
"""
import json
import time
import traceback
import urllib.request
import urllib.error
from django.conf import settings
from .document_loader import get_knowledge_base


# Models tried in order — all free tier on AI Studio
# Get a fresh key at: https://aistudio.google.com/apikey
FALLBACK_MODELS = [
    # "gemini-1.5-flash",
    # "gemini-1.5-flash-8b",
    # "gemini-1.0-pro",
    # "gemini-pro",
    # "gemini-2.0-flash",
    # "gemini-3.1-flash-preview",
    # "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite-preview"
]


def build_system_prompt() -> str:
    knowledge_base = get_knowledge_base()
    return f"""You are a professional, friendly customer support assistant.

Your ONLY knowledge source is the business documentation provided below.
Read it carefully and answer customer questions using ONLY the information found in it.

RULES:
- Answer questions related to the business, services, pricing, process, or contact info in the documents.
- If a question is outside scope, politely say you can only help with topics in your knowledge base.
- Be concise, warm, and helpful. Use bullet points or numbered steps where appropriate.
- If asked about pricing, always mention custom quotes are available.
- Greet the user warmly on first message and ask how you can help.
- Speak in the same language the customer uses.

=== BUSINESS KNOWLEDGE BASE ===
{knowledge_base}
=== END OF KNOWLEDGE BASE ===
"""


def _safe_history(history) -> list:
    """Normalize history to Gemini REST format. Ignores invalid values."""
    if not isinstance(history, list):
        return []
    result = []
    for msg in history:
        if not isinstance(msg, dict):
            continue
        role = msg.get("role", "")
        parts = msg.get("parts", "")
        if role not in ("user", "model"):
            continue
        if not parts or not isinstance(parts, str):
            continue
        result.append({"role": role, "parts": [{"text": parts}]})
    return result


def _call_gemini(model: str, payload: dict) -> str | None:
    """
    Call one Gemini model. Returns text on success, None on quota/error.
    Raises ValueError for hard errors (bad key, invalid request).
    """
    api_key = settings.GOOGLE_AI_API_KEY
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        candidates = result.get("candidates", [])
        if not candidates:
            print(f"[AIService] {model}: no candidates — {result}")
            return None
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()
        return text or None

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[AIService] {model}: HTTP {e.code}")
        if e.code == 429:
            # Quota exhausted — try next model
            return None
        if e.code in (400, 403):
            # Bad key or invalid request — don't bother trying more models
            raise ValueError(f"HTTP {e.code}: {body[:200]}")
        return None

    except urllib.error.URLError as e:
        print(f"[AIService] {model}: network error — {e.reason}")
        return None


def chat_with_ai(user_message: str, history) -> str:
    """
    Try each model in FALLBACK_MODELS until one responds successfully.
    """
    system_prompt = build_system_prompt()
    safe_history = _safe_history(history)

    contents = safe_history + [
        {"role": "user", "parts": [{"text": user_message}]}
    ]

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }

    for model in FALLBACK_MODELS:
        print(f"[AIService] Trying model: {model}")
        try:
            text = _call_gemini(model, payload)
            if text:
                print(f"[AIService] Success with {model}")
                return text
            print(f"[AIService] {model} quota exhausted, trying next...")
        except ValueError as e:
            print(f"[AIService] Hard error on {model}: {e}")
            return (
                "⚠️ API key error. Please get a free key at "
                "https://aistudio.google.com/apikey and update GOOGLE_AI_API_KEY in backend/.env"
            )
        except Exception as e:
            print(f"[AIService] Unexpected: {e}")
            traceback.print_exc()

    # All models exhausted
    return (
        "⚠️ All AI quota limits reached on this API key.\n\n"
        "**Fix (free, 1 minute):**\n"
        "1. Go to https://aistudio.google.com/apikey\n"
        "2. Click **Create API Key**\n"
        "3. Copy the new key\n"
        "4. Open `backend/.env` → set `GOOGLE_AI_API_KEY=<your-new-key>`\n"
        "5. Restart Django\n\n"
        "Free tier gives 1,500 requests/day and 15 requests/minute."
    )