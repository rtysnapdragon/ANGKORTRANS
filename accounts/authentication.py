# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from accounts.users.models import User as USERS
from core.utils.exceptions import JWTExpiredException, JWTInvalidException

class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication.
    - Returns (user, token) if valid token exists
    - Returns None if no token (allows AllowAny views)
    - Raises AuthenticationFailed if token invalid/expired
    """
     
    def authenticate(self, request):
        
        auth_header = request.headers.get('Authorization')
        # print("JWTAuthentication called====================", auth_header)

        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # public route, unauthenticated

        token = auth_header.replace('Bearer ', '').strip()

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

            user_id = payload.get("user_id") or payload.get("UserId")
            if not user_id:
                raise AuthenticationFailed("Invalid token: missing user_id")

            user = USERS.objects.get(ID=user_id, IS_ACTIVE=True)

            # Patch user for DRF
            user.is_authenticated = True

            # DRF expects (user, auth)
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise JWTExpiredException

        except jwt.InvalidTokenError:
            raise JWTInvalidException

        except USERS.DoesNotExist:
            raise AuthenticationFailed('User not found')
