import jwt
import datetime
from django.conf import settings
import secrets
import hashlib
from datetime import timedelta
from django.utils import timezone

import jwt
import datetime
from django.conf import settings


def create_access_token(user):
    payload = {
        "user_id": user.ID,
        "username": user.USERNAME,
        "role": user.USER_TYPE,
        "type": "access",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(
            seconds=settings.JWT_ACCESS_TOKEN_LIFETIME
        ),
        "iat": datetime.datetime.utcnow(),
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def create_refresh_token(user):
    payload = {
        "user_id": user.ID,
        "type": "refresh",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(
            days=settings.JWT_REFRESH_TOKEN_LIFETIME
        ),
        "iat": datetime.datetime.utcnow(),
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload

    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}

    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
        
def generate_jwt_token(user):
    payload = {
        'UserId': user.ID,
        'Username': user.USERNAME,
        "role": user.USER_TYPE,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token):
    print("Decoding JWT token:", token)
    print("Using secret key:", settings.JWT_SECRET_KEY)

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,       # must match SIMPLE_JWT["SIGNING_KEY"]
            algorithms=['HS256']
        )
        print("Decoded JWT payload:", payload)
        return payload

    except jwt.ExpiredSignatureError:
        print("Token expired.")
        return None

    except jwt.InvalidTokenError as e:
        print("Invalid token:", e)
        return None

    

REMEMBER_TOKEN_DAYS = 14

def GENERATE_REMEMBER_TOKEN():
    raw_token = secrets.token_urlsafe(64)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    expires_at = timezone.now() + timedelta(days=REMEMBER_TOKEN_DAYS)

    return raw_token, token_hash, expires_at

# def decode_jwt_token(token):
#     print("Decoding JWT token---:", token)
#     try:
#         access_token = AccessToken(token)
#         print("Decoded JWT payload----:", dict(access_token))
#         return dict(access_token)  # payload dictionary
#     except TokenError as e:
#         print("Token error:", e)
#         return None
#     except Exception as e:
#         print("General error decoding token:", e)
#         return None

