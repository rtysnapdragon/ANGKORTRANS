
import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from riththy_app.users.models import USERS

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.headers.get("Authorization")

        if not auth:
            request.user = None
            return

        token = auth.replace("Bearer ", "")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = USERS.objects.get(ID=payload["user_id"])
            request.user = user
        except:
            request.user = None


def is_customer(user):
    return user.USER_TYPE == "GENERAL"

def is_fleet_manager(user):
    return user.USER_TYPE == "SYSTEM"
def is_admin(user):
    return user.USER_TYPE == "SYSTEM"