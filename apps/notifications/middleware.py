from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
def some_function():
    from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        access = AccessToken(token)
        user = User.objects.get(id=access["user_id"])
        return user
    except:
        return None


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        from rest_framework_simplejwt.tokens import AccessToken
        self.AccessToken = AccessToken
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)

        token = params.get("token", [None])[0]  

        scope["user"] = await get_user(token)

        return await self.app(scope, receive, send)