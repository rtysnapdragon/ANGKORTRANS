# permissions.py# accounts/permissions.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from riththy_app.users.models import USERS
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from riththy_app.utils.jwt import decode_jwt_token   # adjust import


class IsSystemUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request, "user", None) and request.user.USER_TYPE == "SYSTEM")

class IsGeneralCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request, "user", None) and request.user.USER_TYPE == "GENERAL")


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Authorization token missing')

        token = auth_header.replace('Bearer ', '').strip()

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

            user_id = payload.get("user_id")
            if not user_id:
                raise AuthenticationFailed('Invalid token payload')

            user = USERS.objects.get(
                ID=user_id,
                IS_ACTIVE=True
            )

            # ✅ Attach to DRF-standard attribute
            request.user = user
            request.auth = token

            return True

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('JWT token has expired')

        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid JWT token')

        except USERS.DoesNotExist:
            raise AuthenticationFailed('User not found or inactive')

class IsJWTAuthenticated(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Token missing or invalid')

        token = auth_header.split(' ')[1]
        payload = decode_jwt_token(token)

        if not payload:
            raise AuthenticationFailed('Invalid or expired token')

        try:
            request.user = USERS.objects.get(ID=payload['user_id'])
        except USERS.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return True
