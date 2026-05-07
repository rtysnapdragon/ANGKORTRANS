from rest_framework import serializers
from .models import CHAT_USERS, CHAT_SESSIONS, CHAT_MESSAGES, AI_DOCUMENTS, CHAT_FEEDBACK

class CHAT_USER_SERIALIZER(serializers.ModelSerializer):
    class Meta:
        model = CHAT_USERS
        fields = ['ID', 'USER_UUID', 'USERNAME', 'EMAIL', 'VISITOR_ID', 'CREATED_AT']

class CHAT_SESSION_SERIALIZER(serializers.ModelSerializer):
    class Meta:
        model = CHAT_SESSIONS
        fields = ['ID', 'SESSION_UUID', 'USER', 'START_TIME', 'IS_ACTIVE', 'TOTAL_MESSAGES']

class CHAT_MESSAGE_SERIALIZER(serializers.ModelSerializer):
    class Meta:
        model = CHAT_MESSAGES
        fields = ['ID', 'MESSAGE_UUID', 'SESSION', 'ROLE', 'CONTENT', 'LANGUAGE_DETECTED', 'CREATED_AT']

class AI_DOCUMENT_SERIALIZER(serializers.ModelSerializer):
    class Meta:
        model = AI_DOCUMENTS
        fields = ['ID', 'DOCUMENT_UUID', 'TITLE', 'CONTENT', 'CATEGORY', 'TAGS', 'LANGUAGE', 'CREATED_AT']