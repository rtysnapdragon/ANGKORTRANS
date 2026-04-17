import jwt
import datetime
from django.conf import settings
import secrets
import hashlib
from datetime import timedelta
from django.utils import timezone


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

