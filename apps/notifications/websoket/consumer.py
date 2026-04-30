from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

User = get_user_model()


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        try:
            query = parse_qs(self.scope["query_string"].decode())
            token = query.get("token", [None])[0]

            if not token:
                await self.close(code=4001)
                return

            self.user = await self.get_user_from_token(token)

            if not self.user:
                await self.close(code=4002)
                return

            print( " self.user.Id   ==== > " ,self.user.ID)
            self.group_name = f"user_{self.user.ID}"

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()

            print("WS CONNECTED:", self.user.USERNAME)

        except Exception as e:
            print("JWT ERROR========>:", e)
            await self.close(code=4003)

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

        print("WS CLOSED:", close_code)

    async def receive(self, text_data=None, bytes_data=None):
        print("WS RECEIVE:", text_data)

    async def send_notification(self, event):
        await self.send_json(event["data"])

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            access = AccessToken(token)
            user_id = access["user_id"]

            return User.objects.get(pk=user_id)

        except Exception as e:
            print("JWT PARSE FAIL:", e)
            return Noneself.user.Id 