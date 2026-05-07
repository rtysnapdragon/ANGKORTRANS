# accounts/jwt_utils.py
from django.utils import timezone
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import jwt  # Make sure this is PyJWT
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

JWT_SECRET = getattr(settings, "JWT_SECRET_KEY", settings.SECRET_KEY)
JWT_ALGO = getattr(settings, "JWT_ALGORITHM", "HS256")
ACCESS_EXP = getattr(settings, "JWT_ACCESS_TOKEN_EXPIRES_SECONDS", 60*60*4)
REFRESH_EXP = getattr(settings, "JWT_REFRESH_TOKEN_EXPIRES_SECONDS", 60*60*24*7)


def create_access_token(user):
    now = timezone.now()
    exp = now + timedelta(seconds=ACCESS_EXP)
    payload = {
        "id": user.ID,            # ⚡ must match access token
        "user_id": user.ID,
        "username": user.USERNAME,
        "role": user.USER_TYPE,
        "exp": int(exp.timestamp()),  # MUST be UNIX timestamp
        "iat": int(now.timestamp()),
        "type": "access"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def create_refresh_token(user):
    now = timezone.now()
    exp = now + timedelta(seconds=REFRESH_EXP)
    payload = {
        "id": user.ID,            # ⚡ must match access token
        "user_id": user.ID,
        "exp": int(exp.timestamp()),
        "iat": int(now.timestamp()),
        "type": "refresh"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_token(token):
    """
    Decode a JWT token and return the payload.
    If invalid or expired, returns a dict with an 'error' key.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except Exception as e:
        # Catch all JWT errors without importing specific exceptions
        msg = str(e).lower()
        if "expired" in msg:
            return {"Error": "expired"}
        return {"Error": "invalid"}
    

def is_token_expired(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.utcfromtimestamp(exp):
            return True
        return False
    except jwt.ExpiredSignatureError:
        return True
    except jwt.InvalidTokenError:
        return True