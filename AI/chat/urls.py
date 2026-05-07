from django.urls import path
from .views import *

urlpatterns = [
    path('v1/api/chat', chat_message, name='chat-message'),
    path('v1/api/chat/upload', upload_document, name='upload-document'),
    path('v1/api/chat/reload', reload_docs, name='reload-docs'),
    path('v1/api/health', health_check, name='health-check'),

    path('v2/api/chat', chat, name='chat'),  #OK now

    path('api/v2/chat/init', init_chat, name='init_chat'),
    path('api/v2/chat/send', send_chat_message, name='send_message'),
    path('api/v2/chat/feedback', add_feedback, name='add_feedback'),
    path('api/v2/chat/history', get_chat_history, name='chat_history'),
    path('api/v2/chat/documents', manage_documents, name='manage_documents'),
    path('api/v2/chat/documents/delete', delete_document, name='delete_document'), # by id
]