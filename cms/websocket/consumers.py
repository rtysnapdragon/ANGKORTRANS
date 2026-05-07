# backend/rama_gallery/apps/websocket/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import CHAT_MESSAGES
from rama_gallery.apps.users.models import USERS

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'dashboard_live'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial stats
        await self.send_initial_stats()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'get_realtime_stats':
            await self.send_realtime_stats()
        elif action == 'send_chat_message':
            await self.handle_chat_message(data)
    
    async def send_initial_stats(self):
        stats = await self.get_dashboard_stats()
        await self.send(json.dumps({
            'type': 'initial_stats',
            'data': stats
        }))
    
    async def send_realtime_stats(self):
        stats = await self.get_dashboard_stats()
        await self.send(json.dumps({
            'type': 'realtime_stats',
            'data': stats
        }))
    
    @database_sync_to_async
    def get_dashboard_stats(self):
        from rama_gallery.apps.analytics.models import analytics_manager
        return analytics_manager.get_dashboard_stats()
    
    @database_sync_to_async
    def handle_chat_message(self, data):
        message = CHAT_MESSAGES.objects.create(
            SENDER_ID_id=data['sender_id'],
            RECEIVER_ID_id=data['receiver_id'] if 'receiver_id' in data else None,
            MESSAGE_TEXT=data['message'],
            MESSAGE_TYPE=data.get('message_type', 'TEXT')
        )
        return message
    
    async def dashboard_update(self, event):
        await self.send(json.dumps({
            'type': 'dashboard_update',
            'data': event['data']
        }))
    
    async def new_activity(self, event):
        await self.send(json.dumps({
            'type': 'new_activity',
            'data': event['data']
        }))