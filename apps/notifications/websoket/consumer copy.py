from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs
class NotificationConsumer(
    AsyncJsonWebsocketConsumer
):

    # async def connect(self):
    #     print("WS CONNECT")

    #     print("headers =", self.scope["headers"])
    #     print("path =", self.scope["path"])
    #     print("query =", self.scope["query_string"])

    #     # self.user = self.scope.get("user", None) or self.user = self.scope["user"]
    #     # token = self.scope["query_string"].decode().split("token=")[1]
    #     query_string = self.scope["query_string"].decode()

    #     token = None
    #     for param in query_string.split("&"):
    #         if param.startswith("token="):
    #             token = param.split("=", 1)[1]

    #     print("TOKEN =>", token)

    #     if not token:
    #         print("No token provided")
    #         await self.close(code=4003)
    #         return
        
    #     self.user = await get_user(token)
        
    #     if not self.user or self.user.is_anonymous:
    #         print("Anonymous blocked")
    #         await self.close(code=4001)
    #         return

    #     self.group_name = f"user_{self.user.id}"

    #     self.group = f"user_{self.user.id}"

    #     await self.channel_layer.group_add(
    #         self.group,
    #         self.channel_name
    #     )

    #     await self.accept()

    #     print("WS CONNECTED:", self.group_name)
    #     print("Accepted:", self.group)

    async def connect(self):
        print("WS CONNECT ======>>>")

        self.user = self.scope.get("user", None)

        query_string = self.scope["query_string"].decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        print("TOKEN =>", token)

        if not token:
            await self.close(code=4003)
            return

        if not self.user or self.user.is_anonymous:
            print("Anonymous blocked")
            await self.close(code=4001)
            return

        self.group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        print("WS CONNECTED: =======>", self.group_name)

    async def disconnect(self, code):
        print("WS CLOSED: =======>", code)

        # if hasattr(self, "group"):
        #     await self.channel_layer.group_discard(
        #         self.group,
        #         self.channel_name
        #     )
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        print("WS DISCONNECTED: =======>", code)

    async def receive(
        self,
        text_data=None,
        bytes_data=None
    ):
        print("WS RECEIVE:", text_data)

    async def notify(self, event):
        print("WS SEND:", event)

        await self.send_json(event["data"])

    async def send_notification(self, event):
        print("WS SEND:", event)

        await self.send_json(event["data"])