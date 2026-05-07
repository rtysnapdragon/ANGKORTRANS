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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from cms.artworks.models import Artwork

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
import uuid
from .models import CHAT_USERS, CHAT_SESSIONS, CHAT_MESSAGES, AI_DOCUMENTS, CHAT_FEEDBACK
from .serializers import CHAT_USER_SERIALIZER, CHAT_SESSION_SERIALIZER, CHAT_MESSAGE_SERIALIZER, AI_DOCUMENT_SERIALIZER

from .services.ai_service import AIChatService

ai_service = AIChatService()

@api_view(['POST'])
def init_chat(request):
    """Initialize or get existing chat session"""
    try:
        visitor_id = request.data.get('VISITOR_ID')
        user_uuid = request.data.get('USER_UUID')
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        
        if not visitor_id:
            visitor_id = str(uuid.uuid4())
        
        with transaction.atomic():
            # Get or create user
            user, created = CHAT_USERS.objects.get_or_create(
                VISITOR_ID=visitor_id,
                defaults={
                    'USER_UUID': user_uuid or uuid.uuid4(),
                    'IP_ADDRESS': ip_address,
                    'USER_AGENT': user_agent
                }
            )
            
            if not created:
                # Update existing user
                user.IP_ADDRESS = ip_address
                user.USER_AGENT = user_agent
                user.LAST_ACTIVE = timezone.now()
                user.save()
            
            # Get or create active session
            session = CHAT_SESSIONS.objects.filter(
                USER=user,
                IS_ACTIVE=True
            ).first()
            
            if not session:
                session = CHAT_SESSIONS.objects.create(
                    USER=user,
                    SESSION_UUID=uuid.uuid4(),
                    IS_ACTIVE=True
                )
            
            # Get recent messages
            recent_messages = CHAT_MESSAGES.objects.filter(
                SESSION=session
            ).order_by('-CREATED_AT')[:20]
            
            messages_serializer = CHAT_MESSAGE_SERIALIZER(recent_messages, many=True)
            
            return Response({
                'SUCCESS': True,
                'USER': CHAT_USER_SERIALIZER(user).data,
                'SESSION': CHAT_SESSION_SERIALIZER(session).data,
                'RECENT_MESSAGES': messages_serializer.data,
                'VISITOR_ID': visitor_id
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'SUCCESS': False,
            'ERROR': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def send_chat_message(request):
    """Send message and get AI response"""
    try:
        session_id = request.data.get('SESSION_ID')
        user_id = request.data.get('USER_ID')
        user_message = request.data.get('MESSAGE', '').strip()
        visitor_context = request.data.get('CONTEXT', {})
        
        if not user_message:
            return Response({
                'SUCCESS': False,
                'ERROR': 'Message is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate session and user
        try:
            session = CHAT_SESSIONS.objects.get(ID=session_id, IS_ACTIVE=True)
            user = CHAT_USERS.objects.get(ID=user_id)
        except CHAT_SESSIONS.DoesNotExist:
            return Response({
                'SUCCESS': False,
                'ERROR': 'Invalid or inactive session'
            }, status=status.HTTP_404_NOT_FOUND)
        except CHAT_USERS.DoesNotExist:
            return Response({
                'SUCCESS': False,
                'ERROR': 'Invalid or inactive user'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Save user message to database
        try:
            user_message_obj = CHAT_MESSAGES.objects.create(
                SESSION=session,
                USER=user,
                ROLE='USER',
                CONTENT=user_message,
                LANGUAGE_DETECTED=ai_service.detect_language(user_message)
            )
            print("Succesfully!!!")
        except Exception as e:
            print("Error saving user message:", e)
            return Response(
                {
                    "SUCCESS": False,
                    "ERROR": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Update session message count
        session.TOTAL_MESSAGES += 1
        session.save()
        
        # Get AI response
        ai_response = ai_service.send_message(
            user_message=user_message,
            session_id=session_id,
            user_id=user_id,
            visitor_context=visitor_context
        )
        print(" ai_response ============> ", ai_response)
        
        if ai_response['success']:
            # Save AI response to database
            ai_message_obj = CHAT_MESSAGES.objects.create(
                SESSION=session,
                USER=user,
                ROLE='ASSISTANT',
                CONTENT=ai_response['message'],
                LANGUAGE_DETECTED=ai_response['detected_language'],
                TOKENS_USED=ai_response['tokens_used'],
                MODEL_USED=ai_response['model_used'],
                RESPONSE_TIME_MS=ai_response['response_time_ms'],
                PARENT_MESSAGE=user_message_obj
            )
            
            return Response({
                'SUCCESS': True,
                'MESSAGE': ai_response['message'],
                'MESSAGE_ID': ai_message_obj.ID,
                'MESSAGE_UUID': ai_message_obj.MESSAGE_UUID,
                'TOKENS_USED': ai_response['tokens_used'],
                'RESPONSE_TIME_MS': ai_response['response_time_ms'],
                'LANGUAGE': ai_response['detected_language'],
                'DOCUMENTS_USED': ai_response.get('documents_used', [])
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'SUCCESS': False,
                'ERROR': ai_response.get('error', 'Unknown error'),
                'MESSAGE': ai_response['message']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'SUCCESS': False,
            'ERROR': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_feedback(request):
    """Add user feedback for AI response"""
    try:
        message_id = request.data.get('MESSAGE_ID')
        user_id = request.data.get('USER_ID')
        feedback_type = request.data.get('FEEDBACK_TYPE')
        comment = request.data.get('COMMENT', '')
        
        # Validate feedback type
        valid_types = ['LIKE', 'DISLIKE', 'HELPFUL', 'NOT_HELPFUL']
        if feedback_type not in valid_types:
            return Response({
                'SUCCESS': False,
                'ERROR': 'Invalid feedback type'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or update feedback
        feedback, created = CHAT_FEEDBACK.objects.update_or_create(
            MESSAGE_ID=message_id,
            USER_ID=user_id,
            defaults={
                'FEEDBACK_TYPE': feedback_type,
                'COMMENT': comment
            }
        )
        
        return Response({
            'SUCCESS': True,
            'FEEDBACK_ID': feedback.ID,
            'CREATED': created
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'SUCCESS': False,
            'ERROR': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def manage_documents(request):
    """Manage AI knowledge documents"""
    if request.method == 'GET':
        # Get all active documents
        documents = AI_DOCUMENTS.objects.filter(IS_ACTIVE=True)
        category = request.GET.get('CATEGORY')
        
        if category:
            documents = documents.filter(CATEGORY=category)
        
        serializer = AI_DOCUMENT_SERIALIZER(documents, many=True)
        return Response({
            'SUCCESS': True,
            'DOCUMENTS': serializer.data,
            'COUNT': documents.count()
        })
    
    elif request.method == 'POST':
        # Upload new document
        try:
            document_data = {
                'TITLE': request.data.get('TITLE'),
                'CONTENT': request.data.get('CONTENT'),
                'DOCUMENT_TYPE': request.data.get('DOCUMENT_TYPE', 'GENERAL'),
                'CATEGORY': request.data.get('CATEGORY'),
                'TAGS': request.data.get('TAGS', {}),
                'LANGUAGE': request.data.get('LANGUAGE', 'EN'),
                'METADATA': request.data.get('METADATA', {})
            }
            
            document = AI_DOCUMENTS.objects.create(**document_data)
            serializer = AI_DOCUMENT_SERIALIZER(document)
            
            return Response({
                'SUCCESS': True,
                'DOCUMENT': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'SUCCESS': False,
                'ERROR': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_document(request, document_id):
    """Delete or deactivate document"""
    try:
        document = AI_DOCUMENTS.objects.get(ID=document_id)
        document.IS_ACTIVE = False
        document.save()
        
        return Response({
            'SUCCESS': True,
            'MESSAGE': 'Document deactivated successfully'
        })
    except AI_DOCUMENTS.DoesNotExist:
        return Response({
            'SUCCESS': False,
            'ERROR': 'Document not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_chat_history(request, session_id):
    """Get chat history for a session"""
    try:
        messages = CHAT_MESSAGES.objects.filter(
            SESSION_ID=session_id
        ).order_by('CREATED_AT')
        
        serializer = CHAT_MESSAGE_SERIALIZER(messages, many=True)
        
        return Response({
            'SUCCESS': True,
            'MESSAGES': serializer.data,
            'COUNT': messages.count()
        })
        
    except Exception as e:
        return Response({
            'SUCCESS': False,
            'ERROR': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_gallery_context(request):
    """Provide context about gallery content for AI"""
    user_agent = request.headers.get('User-Agent', '')
    referer = request.headers.get('Referer', '')
    
    # Get recent popular content
    recent_artworks = Artwork.objects.filter(is_published=True)[:10]
    # recent_blogs = Blog.objects.filter(is_published=True)[:5]
    
    context = {
        'artworks': [
            {'title': a.title, 'description': a.description, 'medium': a.medium}
            for a in recent_artworks
        ],
        # 'blogs': [
        #     {'title': b.title, 'excerpt': b.excerpt, 'tags': b.tags}
        #     for b in recent_blogs
        # ],
        'visitor_context': {
            'is_mobile': 'Mobile' in user_agent,
            'referer_source': referer
        }
    }
    
    return Response(context)

@api_view(['POST'])
def track_chat_interaction(request):
    """Track user chat interactions for analytics"""
    data = request.data
    UserInteraction.objects.create(
        question=data['question'],
        answer=data['answer'],
        user_agent=request.headers.get('User-Agent'),
        timestamp=timezone.now()
    )
    return Response({'status': 'recorded'})

    

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