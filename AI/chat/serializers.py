from rest_framework import serializers
from .models import ChatUser, ChatSession, ChatMessage, AIDocument, ChatFeedback

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['ID', 'USER_UUID', 'USERNAME', 'EMAIL', 'VISITOR_ID', 'CREATED_AT']

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['ID', 'SESSION_UUID', 'USER', 'START_TIME', 'IS_ACTIVE', 'TOTAL_MESSAGES']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['ID', 'MESSAGE_UUID', 'SESSION', 'ROLE', 'CONTENT', 'LANGUAGE_DETECTED', 'CREATED_AT']

class AIDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIDocument
        fields = ['ID', 'DOCUMENT_UUID', 'TITLE', 'CONTENT', 'CATEGORY', 'TAGS', 'LANGUAGE', 'CREATED_AT']


class ChatRequestSerializer(serializers.Serializer):

    session_id = serializers.CharField()

    message = serializers.CharField()