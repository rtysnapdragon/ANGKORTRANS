"""
AI Service — Google Gemini via REST API (AI Studio)
Uses direct HTTP calls — no SDK dependency issues.
"""
import json
import traceback
import urllib.request
import urllib.error
from django.conf import settings
from .document_loader import get_knowledge_base


def build_system_prompt() -> str:
    knowledge_base = get_knowledge_base()
    return f"""You are a professional, friendly customer support assistant.

Your ONLY knowledge source is the business documentation provided below.
Read it carefully and answer customer questions using ONLY the information found in it.

RULES:
- Answer questions related to the business, services, pricing, process, or contact info in the documents.
- If a question is outside the scope of the documents, politely say you can only help with topics in your knowledge base.
- Be concise, warm, and helpful. Use bullet points or numbered steps where appropriate.
- If a customer asks about pricing, always mention that custom quotes are available.
- Greet the user warmly on first message and ask how you can help.
- Speak in the same language the customer uses.

=== BUSINESS KNOWLEDGE BASE ===
{knowledge_base}
=== END OF KNOWLEDGE BASE ===
"""


def _safe_history(history) -> list:
    """
    Normalize history to Gemini REST format.
    Accepts list of dicts. Ignores any non-list / invalid values gracefully.
    """
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


def chat_with_ai(user_message: str, history) -> str:
    """
    Call Gemini REST API directly (no SDK required).
    Uses gemini-2.0-flash — available on AI Studio free tier.
    """
    api_key = settings.GOOGLE_AI_API_KEY
    model = "gemini-2.0-flash"
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )

    system_prompt = build_system_prompt()
    safe_history = _safe_history(history)

    contents = safe_history + [
        {"role": "user", "parts": [{"text": user_message}]}
    ]

    payload = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        candidates = result.get("candidates", [])
        if not candidates:
            print(f"[AIService] No candidates in response: {result}")
            return "I didn't receive a response from the AI. Please try again."

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()
        return text or "I couldn't generate a response. Please try again."

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[AIService] HTTP {e.code}: {body}")
        return f"AI service returned an error (HTTP {e.code}). Please try again."

    except urllib.error.URLError as e:
        print(f"[AIService] Network error: {e.reason}")
        return "Cannot reach AI service. Check internet connection and try again."

    except Exception as e:
        print(f"[AIService] Unexpected error: {e}")
        traceback.print_exc()
        return "An unexpected error occurred. Please try again."