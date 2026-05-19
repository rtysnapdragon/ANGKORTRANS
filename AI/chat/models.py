from django.db import models
import uuid

class ChatUser(models.Model):
    ID = models.AutoField(primary_key=True)
    USER_UUID = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    USERNAME = models.CharField(max_length=100, null=True, blank=True)
    EMAIL = models.EmailField(max_length=255, null=True, blank=True)
    VISITOR_ID = models.CharField(max_length=255)
    IP_ADDRESS = models.GenericIPAddressField(null=True, blank=True)
    USER_AGENT = models.TextField(null=True, blank=True)
    CREATED_AT = models.DateTimeField(auto_now_add=True)
    LAST_ACTIVE = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'CHAT_USERS'
        indexes = [
            models.Index(fields=['USER_UUID']),
            models.Index(fields=['VISITOR_ID']),
        ]

class ChatSession(models.Model):
    ID = models.AutoField(primary_key=True)
    SESSION_UUID = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    USER = models.ForeignKey(ChatUser, on_delete=models.CASCADE, db_column='USER_ID')
    START_TIME = models.DateTimeField(auto_now_add=True)
    END_TIME = models.DateTimeField(null=True, blank=True)
    IS_ACTIVE = models.BooleanField(default=True)
    TOTAL_MESSAGES = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'CHAT_SESSIONS'
        indexes = [
            models.Index(fields=['SESSION_UUID']),
            models.Index(fields=['USER']),
            models.Index(fields=['IS_ACTIVE']),
        ]

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ASSISTANT', 'Assistant'),
        ('SYSTEM', 'System'),
    ]
    
    ID = models.AutoField(primary_key=True)
    MESSAGE_UUID = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    SESSION = models.ForeignKey(ChatSession, on_delete=models.CASCADE,related_name='chat_messages_session_id', db_column='SESSION_ID')
    USER = models.ForeignKey(ChatUser, on_delete=models.CASCADE,related_name='chat_messages_user_id', db_column='USER_ID')
    ROLE = models.CharField(max_length=10, choices=ROLE_CHOICES)
    CONTENT = models.TextField()
    LANGUAGE_DETECTED = models.CharField(max_length=5, null=True, blank=True)
    TOKENS_USED = models.IntegerField(default=0)
    MODEL_USED = models.CharField(max_length=100, null=True, blank=True)
    RESPONSE_TIME_MS = models.IntegerField(null=True, blank=True)
    CREATED_AT = models.DateTimeField(auto_now_add=True)
    IS_EDITED = models.BooleanField(default=False)
    PARENT_MESSAGE = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='PARENT_MESSAGE_ID')
    
    class Meta:
        db_table = 'CHAT_MESSAGES'
        ordering = ["CREATED_AT"]
        indexes = [
            models.Index(fields=['SESSION']),
            models.Index(fields=['USER']),
            models.Index(fields=['CREATED_AT']),
            models.Index(fields=['ROLE']),
        ]

class AIDocument(models.Model):
    ID = models.AutoField(primary_key=True)
    DOCUMENT_UUID = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    TITLE = models.CharField(max_length=500)
    CONTENT = models.TextField()
    DOCUMENT_TYPE = models.CharField(max_length=50, null=True, blank=True)
    CATEGORY = models.CharField(max_length=100, null=True, blank=True)
    TAGS = models.JSONField(default=dict, null=True, blank=True)
    LANGUAGE = models.CharField(max_length=5, default='EN')
    IS_ACTIVE = models.BooleanField(default=True)
    VERSION = models.IntegerField(default=1)
    METADATA = models.JSONField(default=dict, null=True, blank=True)
    CREATED_AT = models.DateTimeField(auto_now_add=True)
    UPDATED_AT = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'AI_DOCUMENTS'
        indexes = [
            models.Index(fields=['DOCUMENT_UUID']),
            models.Index(fields=['TITLE']),
            models.Index(fields=['CATEGORY']),
            models.Index(fields=['IS_ACTIVE']),
        ]

class ChatFeedback(models.Model):
    FEEDBACK_TYPES = [
        ('LIKE', 'Like'),
        ('DISLIKE', 'Dislike'),
        ('HELPFUL', 'Helpful'),
        ('NOT_HELPFUL', 'NotHelpful'),
    ]
    
    ID = models.AutoField(primary_key=True)
    MESSAGE = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, db_column='MESSAGE_ID')
    USER = models.ForeignKey(ChatUser, on_delete=models.CASCADE, db_column='USER_ID')
    FEEDBACK_TYPE = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    COMMENT = models.TextField(null=True, blank=True)
    CREATED_AT = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'CHAT_FEEDBACK'
        unique_together = ['MESSAGE', 'USER']
        indexes = [
            models.Index(fields=['MESSAGE']),
        ]