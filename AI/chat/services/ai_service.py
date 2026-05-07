import requests
import time
import json
from django.conf import settings
from django.db.models import Q
from ..models import AI_DOCUMENTS, CHAT_MESSAGES

class AIChatService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.api_url = settings.OPENROUTER_API_URL
    
    def search_documents(self, query, language='EN', limit=5):
        """Search relevant documents from database"""
        try:
            print("query ============> ", query)
            print("language ============> ", language)
            # Search in documents using full-text search
            documents = AI_DOCUMENTS.objects.filter(
                IS_ACTIVE=True,
                LANGUAGE=language
            ).filter(
                Q(TITLE__icontains=query) | 
                Q(CONTENT__icontains=query) |
                Q(CATEGORY__icontains=query)
            )[:limit]
            
            return documents
        except Exception as e:
            print(f"Document search error: {e}")
            return []
    
    def build_context_from_documents(self, documents, user_query):
        """Build context string from retrieved documents"""
        if not documents:
            return ""
        
        context_parts = ["Here is relevant information from RamaGallery:\n"]
        
        for doc in documents:
            context_parts.append(f"--- {doc.TITLE} ---")
            # Take first 500 characters of content
            content_preview = doc.CONTENT[:1000] if doc.CONTENT else ""
            context_parts.append(content_preview)
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def get_recent_conversation(self, session_id, limit=10):
        """Get recent conversation history"""
        try:
            messages = CHAT_MESSAGES.objects.filter(
                SESSION=session_id
            ).order_by('-CREATED_AT')[:limit]
            
            # Reverse to get chronological order
            conversations = []
            for msg in reversed(messages):
                conversations.append({
                    'role': msg.ROLE.lower(),
                    'content': msg.CONTENT
                })
            
            return conversations
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return []
    
    def detect_language(self, text):
        """Simple language detection"""
        # Check for Khmer Unicode
        khmer_patterns = range(0x1780, 0x1800)
        for char in text:
            if ord(char) in khmer_patterns:
                return 'km'
        return 'en'
    
    def send_message(self, user_message, session_id, user_id, visitor_context=None):
        """Process and send message to OpenRouter API"""
        start_time = time.time()
        
        # Detect language
        detected_lang = self.detect_language(user_message)
        
        # Search for relevant documents
        relevant_docs = self.search_documents(user_message, detected_lang.upper())
        print(" Relevant docs : ", relevant_docs)
        # Build context from documents
        doc_context = self.build_context_from_documents(relevant_docs, user_message)
        print(" doc_context : ", doc_context)
        # Get recent conversation
        conversation_history = self.get_recent_conversation(session_id, limit=10)
        print(" conversation_history : ", conversation_history)
        
        # Enhanced system prompt with document context
        system_prompt = f"""You are an AI assistant for RamaGallery, an artist's personal website specializing in Khmer art and culture.

CRITICAL LANGUAGE REQUIREMENTS:
- The user's message language is: {'Khmer (ភាសាខ្មែរ)' if detected_lang == 'km' else 'English'}
- You MUST respond in EXACTLY the same language as the user
- If user writes in Khmer, respond in Khmer using proper Unicode script
- Use appropriate cultural context and honorifics

GALLERY CONTEXT FROM DATABASE:
{doc_context if doc_context else "No specific documents found. Use general knowledge about RamaGallery."}

YOUR CAPABILITIES:
- Help visitors with information about artworks, techniques, and artist background
- Navigate gallery content including blogs, exhibitions, and events
- Answer questions about user engagement (likes, comments, shares)
- Provide insights into Khmer art traditions and contemporary works

Guidelines:
- Be knowledgeable, friendly, and specific to RamaGallery
- Reference actual artworks and content from the documents when possible
- Keep responses concise (2-3 paragraphs max)
- If unsure about something, be honest and offer to help find the information

Current visitor context: {json.dumps(visitor_context or {})}
"""
        
        # Prepare messages for API
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Call OpenRouter API
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://ramagallery.com',
                    'X-Title': 'RamaGallery AI Assistant'
                },
                json={
                    # 'model': 'qwen/qwen-3.5-max',  # Best for Khmer
                    'model': settings.OPENROUTER_MODEL,
                    'messages': messages,
                    'temperature': 0.7,
                    'max_tokens': 500
                },
                timeout=30
            )
            
            response_time = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['choices'][0]['message']['content']
                tokens_used = result.get('usage', {}).get('total_tokens', 0)
                
                return {
                    'success': True,
                    'message': assistant_message,
                    'tokens_used': tokens_used,
                    'response_time_ms': response_time,
                    'model_used': 'qwen/qwen-3.5-max',
                    'detected_language': detected_lang,
                    'documents_used': [doc.TITLE for doc in relevant_docs]
                }
            else:
                print("OpenRouter response:", response.text)

                return {
                    'success': False,
                    'error': f"API Error: {response.status_code} - {response.text}",
                    'message': self.get_fallback_message(detected_lang)
                }
                                
        except Exception as e:
            print(f"OpenRouter API error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': self.get_fallback_message(detected_lang)
            }
    
    def get_fallback_message(self, language):
        """Fallback message when API fails"""
        if language == 'km':
            return "សូមទោស ខ្ញុំកំពុងមានបញ្ហាក្នុងការតភ្ជាប់។ សូមព្យាយាមម្តងទៀតនៅពេលក្រោយ។"
        return "I apologize, but I'm having trouble connecting right now. Please try again in a moment."