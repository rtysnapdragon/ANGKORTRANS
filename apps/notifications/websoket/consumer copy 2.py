from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
import jwt
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("settings.SECRET_KEY ======> ", settings.SECRET_KEY)
        print("WS CONNECT")
        query_string = self.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]
        if token:
            token = token.strip()
        print("QUERY STRING =>", query_string)

        # SAFE TOKEN PARSING
        token = None
        if "token=" in query_string:
            token = query_string.split("token=")[-1]

        print("TOKEN =>", token)

        if not token:
            await self.close(code=4001)
            return
        # TEMP: fallback auth (you can replace with JWT decode later)
        # self.user = self.scope.get("user")
        # self.user_id = self.scope.get("user_id")
        # print("USER ID =>", self.user_id)
       # ----------------------------
        # JWT DECODE (IMPORTANT FIX)
        # ----------------------------
        user_id = None


        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)

            self.user = user
            self.user_id = user.id

        except (InvalidToken, TokenError, Exception) as e:
            print("JWT ERROR========>:", e)
            await self.close(code=4003)
            return

        # if token:
        #     try:
        #         payload = jwt.decode(
        #             token,
        #             settings.SECRET_KEY,
        #             algorithms=["HS256"]
        #         )
        #         user_id = payload.get("user_id")
        #     except Exception as e:
        #         print("JWT ERROR:", e)
        #         await self.close(code=4003)
        #         return

        # print("USER ID =>", user_id)

        # if not user_id:
        #     print("No user => blocked")
        #     await self.close(code=4001)
        #     return

        # if not self.user_id:
        #     print("================= No user ===============")
        #     await self.close(code=4001)
        #     return

        # if not self.user or self.user.is_anonymous:
        #     print("Anonymous blocked")
        #     await self.close(code=4001)
        #     return
        
        if self.user.is_anonymous:
            print("Anonymous blocked")
            await self.close(code=4003)
            return
        self.user_id = user_id
        self.group_name = f"user_{user_id}"

        # self.group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        print("WS CONNECTED:", self.group_name)

    async def disconnect(self, code):
        print("WS CLOSED:", code)

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

        print("WS DISCONNECTED")

    async def receive(self, text_data=None, bytes_data=None):
        print("WS RECEIVE ============>:", text_data)

    async def notify(self, event):
        print("WS SEND =============>:", event)

        await self.send_json(event["data"])