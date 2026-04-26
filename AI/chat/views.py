"""
Chat API Views
POST /api/chat/         — send a message, get AI reply
POST /api/chat/upload/  — upload a .txt document to knowledge base
GET  /api/chat/reload/  — reload documents cache
GET  /api/health/       — health check
"""
import os
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .ai_service import chat_with_ai
from .document_loader import reload_documents, get_knowledge_base


@api_view(['POST'])
def chat_message(request):
    """
    Body: {
        "message": "user text",
        "history": [{"role": "user"|"model", "parts": "text"}]  <- optional, can be []
    }
    """
    message = request.data.get('message', '')
    if isinstance(message, str):
        message = message.strip()

    history = request.data.get('history', [])

    # Gracefully handle history being sent as a non-list (e.g. a string)
    if not isinstance(history, list):
        history = []

    if not message:
        return Response(
            {'error': 'message field is required and cannot be empty.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    print(f"[Chat] message={message!r}  history_len={len(history)}")

    reply = chat_with_ai(message, history)

    print(f"[Chat] reply={reply[:80]!r}...")
    return Response({'reply': reply})


@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_document(request):
    """Upload a .txt file to the documents folder and reload cache."""
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'No file provided.'}, status=400)

    if not file.name.endswith('.txt'):
        return Response({'error': 'Only .txt files are supported.'}, status=400)

    docs_dir = settings.DOCUMENTS_DIR
    docs_dir.mkdir(parents=True, exist_ok=True)

    save_path = docs_dir / file.name
    with open(save_path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    reload_documents()
    return Response({'message': f'Document "{file.name}" uploaded and knowledge base reloaded.'})


@api_view(['GET'])
def reload_docs(request):
    """Force reload the documents cache."""
    kb = reload_documents()
    char_count = len(kb)
    return Response({
        'message': 'Knowledge base reloaded.',
        'characters_loaded': char_count
    })


@api_view(['GET'])
def health_check(request):
    kb = get_knowledge_base()
    return Response({
        'status': 'ok',
        'service': 'AI Chat Backend',
        'knowledge_base_chars': len(kb),
        'api_key_set': bool(settings.GOOGLE_AI_API_KEY),
    })



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .document_loader1 import detect_domain, load_domain
from .ai_service1 import call_gemini   # your Gemini function


def build_prompt(query: str, context: str) -> str:
    return f"""
You are an AI assistant for a business system.

Use the context below to answer the user clearly and accurately.

CONTEXT:
{context}

USER QUESTION:
{query}

Answer:
""".strip()


@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body)
        message = body.get("message", "")

        if not message:
            return JsonResponse({"error": "Empty message"}, status=400)

        print(f"[Chat] message='{message}'")

        # 🧠 STEP 1: detect domain (agriculture, business, general)
        domain = detect_domain(message)
        print(f"[Chat] detected domain: {domain}")

        # 📄 STEP 2: load relevant documents
        context = load_domain(domain)

        # 🧠 STEP 3: build prompt
        prompt = build_prompt(message, context)

        # 🤖 STEP 4: call AI
        reply = call_gemini(prompt)

        return JsonResponse({
            "reply": reply,
            "domain": domain
        })

    except Exception as e:
        print("[Chat ERROR]", str(e))
        return JsonResponse({
            "error": "Internal error",
            "detail": str(e)
        }, status=500)