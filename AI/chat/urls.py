from django.urls import path
from . import views

urlpatterns = [
    path('v1/api/chat', views.chat_message, name='chat-message'),
    path('v1/api/chat/upload', views.upload_document, name='upload-document'),
    path('v1/api/chat/reload', views.reload_docs, name='reload-docs'),
    path('v1/api/health', views.health_check, name='health-check'),


    path('v2/api/chat', views.chat, name='chat'),  #OK now


]