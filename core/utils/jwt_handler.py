import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_tokens(user):
    payload = {
        "user_id": user.ID,
        "username": user.USERNAME,
        "role": user.USER_TYPE,
        "exp": datetime.utcnow() + timedelta(hours=4),
    }
    access = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    refresh_payload = {
        "user_id": user.ID,
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    refresh = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    return {"access": access, "refresh": refresh}


def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None