from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
# from django.utils import timezone
from .models import AuthAuditLog, RefreshToken as CustomRefreshToken
from django.db import models
from django.shortcuts import get_object_or_404
from django.db import transaction
from accounts.users.models import Users as User, UserProfile
from datetime import timezone

from .models import (UserOTP, ForgotOrResetPassword)
from .serializers import (
    ForgotOrResetPasswordSerializer,
    LoginSerializer,
    UserOTPSerializer,
    RegisterSerializer,
    # ForgotOrResetPasswordSerializer
)
from accounts.users.serializers import (
    UserSerializer, 
)

@api_view(['POST'])
@permission_classes([AllowAny])
def register11(request):
    print("Register endpoint called with data:", request.data)
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = User.objects.create(
            CODE=serializer.validated_data['Code'],
            USERNAME=serializer.validated_data['Username'],
            EMAIL=serializer.validated_data['Email'],
            USER_TYPE=serializer.validated_data.get('UserType', 'USER'),
            STATUS='PENDING',
            CREATED_BY_id=None  # anonymous system
        )

        user.set_password(serializer.validated_data['Password'])
        user.save()

        UserProfile.objects.create(
            USER_ID=user,
            NAME=serializer.validated_data.get('Name'),
            NAME_ENGLISH=serializer.validated_data.get('NameEnglish'),
            GENDER=serializer.validated_data.get('Gender'),
            DOB=serializer.validated_data.get('DateOfBirth'),
            POB=serializer.validated_data.get('PlaceOfBirth'),
            CREATED_BY_id=None
        )

        return Response({
            "message": "User registered successfully",
            "user_id": user.ID
        }, status=201)

    return Response(serializer.errors, status=400)

import uuid
from rest_framework_simplejwt.tokens import RefreshToken
import random

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    data = request.data
    print("Register endpoint called with data:", data)

    # =========================
    # 1. REQUIRED FIELD CHECK
    # =========================
    required_fields = ["Name", "Username", "Email", "Password"]

    errors = {}
    for field in required_fields:
        if not data.get(field):
            errors[field] = "This field is required"

    if errors:
        return Response({
            "message": "Validation error",
            "errors": errors
        }, status=400)

    try:
        with transaction.atomic():

            # =========================
            # SYSTEM USER
            # =========================
            system_user = User.objects.filter(ID=1).first()

            if not system_user:
                return Response({
                    "message": "System user (ID=1) not found"
                }, status=500)

            # =========================
            # 2. DUPLICATE CHECK
            # =========================
            if User.objects.filter(EMAIL=data["Email"]).exists():
                return Response({"Email": "Email already exists"}, status=400)

            if User.objects.filter(USERNAME=data["Username"]).exists():
                return Response({"Username": "Username already exists"}, status=400)

            # =========================
            # 3. GENERATE CODE
            # =========================
            # generated_code = str(uuid.uuid4())[:8].upper()
            # generated_code = "ANONYMOUS0000" + ''.join(str(random.randint(0, 9)) for _ in range(8))
            # counter = 1
            # generated_code = f"ANONYMOUS0000{counter}"
            # counter += 1
            
            user_count = User.objects.count()
            generated_code = f"ANONYMOUS0000{user_count}"
            
            print(" Generated code ::::::::::: ", generated_code)
            print(" system_user  ======>   ", system_user)
            print(" system_user.ID  ======>   ", system_user.ID)
            
            # =========================
            # 4. CREATE USER
            # =========================
            user = User.objects.create(
                CODE=generated_code,
                USERNAME=data["Username"],
                EMAIL=data["Email"],
                USER_TYPE="USER",
                STATUS="ACTIVE",

                IS_SUPERUSER=False,
                EMAIL_VERIFIED=False,
                PHONE_VERIFIED=False,
                FAILED_LOGIN_ATTEMPTS=0,
                IS_DELETED=False,

                CREATED_BY=system_user
            )

            user.set_password(data["Password"])
            user.save()

            # =========================
            # 5. CREATE PROFILE
            # =========================
            UserProfile.objects.create(
                user_profile_user_id=user,
                NAME=data["Name"],
                CREATED_BY=system_user
            )

            # =========================
            # 6. GENERATE JWT TOKEN
            # =========================
            refresh = RefreshToken.for_user(user)

            return Response({
                "Message": "User registered successfully",
                "AccessToken": str(refresh.access_token),
                "RefreshToken": str(refresh),
                "User": {
                    "id": user.ID,
                    "username": user.USERNAME,
                    "email": user.EMAIL,
                    "name": data["Name"]
                }
            }, status=201)

    except Exception as e:
        return Response({
            "message": "Registration failed",
            "error": str(e)
        }, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):

    data = request.data
    print("Register endpoint called with data:", data)

    # =========================
    # 1. REQUIRED FIELD CHECK
    # =========================
    required_fields = ["Name", "Username", "Email", "Password"]

    errors = {}
    for field in required_fields:
        if not data.get(field):
            errors[field] = "This field is required"

    if errors:
        return Response({
            "message": "Validation error",
            "errors": errors
        }, status=400)

    try:
        with transaction.atomic():

            # =========================
            # SYSTEM USER (CREATED_BY fallback)
            # =========================
            # system_user = User.objects.filter(USERNAME="admin").first()
            # system_user = User.objects.get(ID=1)
            system_user = User.objects.filter(ID=1).first()
            print(" System user ::::::::::: ", system_user)

            if not system_user:
                return Response({
                    "message": "System user (ID=1) not found. Please create admin user first."
                }, status=500)
    
            # fallback safety (if not created yet)
            if not system_user:
                system_user = None

            # =========================
            # 2. DUPLICATE CHECK
            # =========================
            if User.objects.filter(EMAIL=data["Email"]).exists():
                return Response({"Email": "Email already exists"}, status=400)

            if User.objects.filter(USERNAME=data["Username"]).exists():
                return Response({"Username": "Username already exists"}, status=400)


            # =========================
            # 3. CREATE USER
            # =========================
            user = User.objects.create(
                CODE=data["Code"],
                USERNAME=data["Username"],
                EMAIL=data["Email"],
                PASSWORD=data["Password"],  # Will be hashed in set_password()
                USER_TYPE=data.get("UserType", "USER"),
                STATUS="PENDING",

                IS_SUPERUSER=False,
                EMAIL_VERIFIED=False,
                PHONE_VERIFIED=False,
                FAILED_LOGIN_ATTEMPTS=0,
                IS_DELETED=False,

                CREATED_BY= system_user.ID   # SYSTEM AUDIT
            )

            user.set_password(data["Password"])
            user.save()

            # =========================
            # 4. CREATE PROFILE
            # =========================
            UserProfile.objects.create(
                USER_ID=user,

                NAME=data["Name"],
                NAME_ENGLISH=data.get("NameEnglish"),
                GENDER=data.get("Gender"),
                DOB=data.get("DateOfBirth"),
                POB=data.get("PlaceOfBirth"),

                MARITAL_STATUS=data.get("MaritalStatus"),
                NATIONAL_ID=data.get("NationalId"),
                NATIONALITY=data.get("Nationality"),
                OCCUPATION=data.get("Occupation"),

                ADDRESS_LINE1=data.get("AddressLine1"),
                ADDRESS_LINE2=data.get("AddressLine2"),

                ZIP_CODE=data.get("ZipCode"),
                POSTAL_CODE=data.get("PostalCode"),

                PROFILE_PICTURE_URL=data.get("ProfilePictureUrl"),
                SIGNATURE_URL=data.get("SignatureUrl"),
                BIO=data.get("Bio"),

                LANGUAGE_PREFERENCE=data.get("LanguagePreference", "km"),
                TIMEZONE=data.get("Timezone", "Asia/Phnom_Penh"),
                IS_VERIFIED=False,

                FACEBOOK_LINK=data.get("FacebookLink"),
                TIKTOK_LINK=data.get("TiktokLink"),
                LINKEDIN_LINK=data.get("LinkedinLink"),
                WEBSITE=data.get("Website"),

                CREATED_BY=system_user
            )

            return Response({
                "message": "User registered successfully",
                "user_id": user.ID,
                "status": user.STATUS,
                "is_superuser": user.IS_SUPERUSER
            }, status=201)

    except Exception as e:
        return Response({
            "message": "Registration failed",
            "error": str(e)
        }, status=400)
        
        
# ====================== LOGIN WITH JWT ======================

@api_view(['POST'])
@permission_classes([AllowAny])
def auth_login(request):
    print("Login endpoint called with data:", request.data)
    """Login - Returns JWT Access + Refresh Token"""
    serializer = LoginSerializer(data=request.data)
    print("Login serializer: ", serializer)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username_or_email = serializer.validated_data['UsernameOrEmail']
    password = serializer.validated_data['Password']
    print("Login username_or_email: ", username_or_email)
    print("Login password: ", password)

    try:
        user = User.objects.get(EMAIL=username_or_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(USERNAME=username_or_email)
        except User.DoesNotExist:
            log_auth_event(None, 'LOGIN_FAILED', f'User not found: {username_or_email}', request)
            return Response({"Message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if user.STATUS != 'ACTIVE':
        log_auth_event(user, 'LOGIN_FAILED', 'Account inactive or locked', request)
        return Response({"Message": "Account is not locked/active"}, status=status.HTTP_403_FORBIDDEN)

    if not check_password(password, user.PASSWORD_HASH):
        if user.STATUS == 'LOCKED':
            return Response({
                "Message": "Account is locked"
            }, status=403)
        if user.LOCKED_UNTIL and user.LOCKED_UNTIL > timezone.now():
            return Response({"Message": "Temporarily locked"}, status=403)

        user.FAILED_LOGIN_ATTEMPTS += 1
        if user.FAILED_LOGIN_ATTEMPTS >= 5:
            user.STATUS = 'LOCKED'
        user.save()
        log_auth_event(user, 'LOGIN_FAILED', 'Invalid password', request)
        return Response({"Message": "Invalid credentials (Password)"}, status=status.HTTP_401_UNAUTHORIZED)

    # Reset failed attempts on success
    user.FAILED_LOGIN_ATTEMPTS = 0
    user.LAST_LOGIN = timezone.now()
    user.save()

    # Generate JWT tokens
    user = User.objects.get(ID=user.ID)
    # user_profile = UserProfile.objects.get(USER_ID=user)
    print("User: ", user)
    # print("User profile: ", user_profile)
    refresh = RefreshToken.for_user(user)   # SimpleJWT handles this

    log_auth_event(user, 'LOGIN', 'Login successful', request, success=True)

    return Response({
        "AccessToken": str(refresh.access_token),
        "RefreshToken": str(refresh),
        "User": UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username_or_email = serializer.validated_data['UsernameOrEmail']
    password = serializer.validated_data['Password']

    user = None
    try:
        user = User.objects.get(EMAIL=username_or_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(USERNAME=username_or_email)
        except User.DoesNotExist:
            return Response({"Message": "Invalid credentials (Username or Email)"}, status=status.HTTP_401_UNAUTHORIZED)

    if user.STATUS != 'ACTIVE':
        return Response({"Message": "Account is not active"}, status=status.HTTP_403_FORBIDDEN)

    if not check_password(password, user.PASSWORD_HASH):
        return Response({"Message": "Invalid credentials (Password)"}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT
    refresh = RefreshToken.for_user(user)
    
    print("Generated JWT Refresh Token:", str(refresh))
    print("Generated JWT Access Token:", str(refresh.access_token))

    return Response({
        "AccessToken": str(refresh.access_token),
        "RefreshToken": str(refresh),
        "User": UserSerializer(user).data
    })

def log_auth_event(user, event_type, description, request, success=True):
    print("User ========== > ", user)
    SYSTEM_USER = User.objects.filter(USERNAME="sysadmin").first()
    print("System user for audit log:", SYSTEM_USER)
    
    print(f"Auth Event - User: {user.ID if user else 'Anonymous'}, Event: {event_type}, Success: {success}")
    """Helper to log security events"""
    AuthAuditLog.objects.create(
        USER_ID=user,
        EVENT_TYPE=event_type,
        EVENT_DESCRIPTION=description,
        IP_ADDRESS=request.META.get('REMOTE_ADDR'),
        USER_AGENT=request.META.get('HTTP_USER_AGENT'),
        SUCCESS=success,
        CREATED_BY=user if user else SYSTEM_USER
    )


# ====================== LOGIN (Basic) ======================
@api_view(['POST'])
@permission_classes([AllowAny])
def auth_login11(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username_or_email = serializer.validated_data['UsernameOrEmail']
    password = serializer.validated_data['Password']

    try:
        user = User.objects.get(EMAIL=username_or_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(USERNAME=username_or_email)
        except User.DoesNotExist:
            return Response({"Message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if user.STATUS != 'ACTIVE':
        return Response({"Message": "Account is not active"}, status=status.HTTP_403_FORBIDDEN)

    if not check_password(password, user.PASSWORD_HASH):
        user.FAILED_LOGIN_ATTEMPTS += 1
        user.save()
        return Response({"Message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Success
    user.FAILED_LOGIN_ATTEMPTS = 0
    user.LAST_LOGIN = models.functions.Now()
    user.save()

    return Response({
        "Message": "Login successful",
        "UserId": user.ID,
        "Username": user.USERNAME,
        "Email": user.EMAIL
    })


@api_view(['POST'])
def auth_refresh(request):
    """Refresh Access Token"""
    try:
        refresh_token = request.data.get('RefreshToken')
        if not refresh_token:
            return Response({"Message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken(refresh_token)
        return Response({
            "AccessToken": str(refresh.access_token),
            "RefreshToken": str(refresh)
        })
    except Exception as e:
        return Response({"Message": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def auth_logout(request):
    """Logout - Blacklist the refresh token"""
    try:
        refresh_token = request.data.get('RefreshToken')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()   # Requires Blacklist app enabled in settings (optional)
        log_auth_event(request.user if request.user.is_authenticated else None, 'LOGOUT', 'User logged out', request)
        return Response({"Message": "Logged out successfully"})
    except Exception:
        return Response({"Message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def auth_me(request):
    """Get current user info (requires valid AccessToken in header)"""
    if not request.user.is_authenticated:
        return Response({"Message": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(UserSerializer(request.user).data)



# import uuid
# from django.utils import timezone
# from datetime import timedelta
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from accounts.models import User
# from .models import ForgotOrResetPasswordSerializer

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def forgot_password(request):

#     email = request.data.get("Email")

#     if not email:
#         return Response({"Email": "This field is required"}, status=400)

#     user = User.objects.filter(EMAIL=email).first()

#     if not user:
#         return Response({"Email": "User not found"}, status=404)

#     token = str(uuid.uuid4())

#     ForgotOrResetPasswordSerializer.objects.create(
#         USER_ID=user,
#         TOKEN_HASH=token,
#         EXPIRES_AT=timezone.now() + timedelta(minutes=30),
#         IS_USED=False,
#         CREATED_BY=user
#     )

#     # 👉 Normally send email here
#     return Response({
#         "message": "Password reset token generated",
#         "token": token   # (REMOVE in production email only)
#     }, status=200)
    
# from django.contrib.auth.hashers import make_password

# # ====================== RESET PASSWORD FOR ANONYMOUS User WEB======================
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def reset_password(request):

#     token = request.data.get("Token")
#     new_password = request.data.get("NewPassword")

#     if not token or not new_password:
#         return Response({
#             "Token": "Required",
#             "NewPassword": "Required"
#         }, status=400)

#     reset_obj = ForgotOrResetPasswordSerializer.objects.filter(TOKEN=token).first()

#     if not reset_obj:
#         return Response({"Token": "Invalid token"}, status=400)

#     if not reset_obj.is_valid():
#         return Response({"Token": "Token expired or already used"}, status=400)

#     user = reset_obj.USER

#     user.PASSWORD_HASH = make_password(new_password)
#     user.save()

#     reset_obj.IS_USED = True
#     reset_obj.save()

#     return Response({
#         "message": "Password reset successful"
#     }, status=200)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
import hashlib


# ====================== FORGOT PASSWORD ======================
@api_view(['POST'])
def forgot_password(request):
    """Request password reset - sends reset token"""
    serializer = ForgotOrResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['Email']

    try:
        user = User.objects.get(EMAIL=email, IS_DELETED=False)
    except User.DoesNotExist:
        # Don't reveal if email exists (security best practice)
        return Response({
            "Message": "If your email exists, you will receive a password reset link."
        }, status=status.HTTP_200_OK)

    # Delete old unused tokens for this user
    ForgotOrResetPasswordSerializer.objects.filter(USER=user, IS_USED=False).delete()

    # Generate secure token
    raw_token = hashlib.sha256(f"{user.ID}{timezone.now()}".encode()).hexdigest()
    token_hash = make_password(raw_token)

    # Create reset token (valid for 1 hour)
    ForgotOrResetPasswordSerializer.objects.create(
        USER=user,
        TOKEN_HASH=token_hash,
        EXPIRES_AT=timezone.now() + timedelta(hours=1),
        CREATED_BY=user
    )

    # In real production, send email with reset link containing raw_token
    # For now, return token (you can replace with email sending later)
    return Response({
        "Message": "Password reset link has been sent to your email.",
        "ResetToken": raw_token,          # Remove this line in production!
        "Note": "In production, this token should be sent via email only."
    })


# ====================== RESET PASSWORD ======================
@api_view(['POST'])
def reset_password(request):
    """Reset password using token"""
    serializer = ForgotOrResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = serializer.validated_data['Token']
    new_password = serializer.validated_data['NewPassword']

    # Find valid token
    try:
        reset_token = ForgotOrResetPassword.objects.get(
            EXPIRES_AT__gt=timezone.now(),
            IS_USED=False
        )
    except ForgotOrResetPassword.DoesNotExist:
        return Response({"Message": "Invalid or expired reset token"}, status=status.HTTP_400_BAD_REQUEST)

    # Verify token (compare hashed version)
    if not check_password(token, reset_token.TOKEN_HASH):
        return Response({"Message": "Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST)

    # Update user password
    user = reset_token.USER
    user.set_password(new_password)
    user.save()

    # Mark token as used
    reset_token.IS_USED = True
    reset_token.save()

    return Response({
        "Message": "Your password has been reset successfully. You can now login with your new password."
    }, status=status.HTTP_200_OK)
    
    
# Add this function to views.py

@api_view(['POST'])
def admin_reset_password(request):
    """Admin resets user password (requires admin privileges)"""
    username_or_email = request.data.get('UsernameOrEmail')
    new_password = request.data.get('NewPassword')

    if not username_or_email or not new_password:
        return Response({"Message": "Username/Email and NewPassword are required"}, status=400)

    # Find user
    try:
        user = User.objects.get(EMAIL=username_or_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(USERNAME=username_or_email)
        except User.DoesNotExist:
            return Response({"Message": "User not found"}, status=404)

    # Optional: Check if requester is admin
    # if not request.user.is_superuser:
    #     return Response({"Message": "Admin permission required"}, status=403)

    # Reset password
    user.set_password(new_password)
    user.save()

    return Response({
        "Message": f"Password for user '{user.USERNAME}' has been reset successfully."
    })
    
    
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def reset_password_no_token(request):

    user = request.user  # JWT authenticated user

    old_password = request.data.get("OldPassword")
    new_password = request.data.get("NewPassword")

    # =========================
    # 1. VALIDATION
    # =========================
    if not old_password or not new_password:
        return Response({
            "OldPassword": "Required",
            "NewPassword": "Required"
        }, status=400)

    # =========================
    # 2. VERIFY OLD PASSWORD
    # =========================
    if not user.check_password(old_password):
        return Response({
            "OldPassword": "Incorrect password"
        }, status=400)

    # =========================
    # 3. SET NEW PASSWORD
    # =========================
    user.PASSWORD_HASH = make_password(new_password)
    user.save()

    return Response({
        "message": "Password updated successfully"
    }, status=200)
    

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def reset_password_and_renew(request):
    user = request.user
    print("Authenticated user for password reset:", user)

    old_password = request.data.get("OldPassword")
    new_password = request.data.get("NewPassword")

    # =========================
    # 1. VALIDATION
    # =========================
    if not old_password or not new_password:
        return Response({
            "OldPassword": "Required",
            "NewPassword": "Required"
        }, status=400)

    # =========================
    # 2. VERIFY OLD PASSWORD
    # =========================
    if not user.check_password(old_password):
        return Response({
            "OldPassword": "Incorrect password"
        }, status=400)

    # =========================
    # 3. UPDATE PASSWORD
    # =========================
    user.PASSWORD_HASH = make_password(new_password)
    user.save()

    # =========================
    # 4. GENERATE NEW JWT
    # =========================
    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Password updated successfully",
        "AccessToken": str(refresh.access_token),
        "RefreshToken": str(refresh),
        "User": {
            "ID": user.ID,
            "USERNAME": user.USERNAME,
            "EMAIL": user.EMAIL
        }
    }, status=200)
    
    
# ====================== USER OTP ======================
@api_view(['POST'])
def user_otp_list(request):
    otps = UserOTP.objects.all().order_by('-CREATED_AT')
    serializer = UserOTPSerializer(otps, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def user_otp_create(request):
    serializer = UserOTPSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from urllib.parse import parse_qs

@api_view(['GET'])
@permission_classes([AllowAny])
def oauth_token(request):
    print("oauth_token")

    # 🔥 READ RAW BODY (important)
    body = request.body.decode('utf-8')
    parsed = parse_qs(body)

    username_or_email = parsed.get('UsernameOrEmail', [None])[0]
    password = parsed.get('Password', [None])[0]

    if not username_or_email or not password:
        return Response({"Message": "Missing credentials"}, status=400)

    # =========================
    # FIND USER
    # =========================
    try:
        user = User.objects.get(EMAIL=username_or_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(USERNAME=username_or_email)
        except User.DoesNotExist:
            return Response({"Message": "Invalid credentials"}, status=401)

    # =========================
    # CHECK LOCK
    # =========================
    if user.STATUS == 'LOCKED':
        return Response({"Message": "Account is locked"}, status=403)

    # =========================
    # CHECK PASSWORD
    # =========================
    if not check_password(password, user.PASSWORD_HASH):
        user.FAILED_LOGIN_ATTEMPTS += 1

        if user.FAILED_LOGIN_ATTEMPTS >= 5:
            user.STATUS = 'LOCKED'

        user.save()

        return Response({"Message": "Invalid credentials"}, status=401)

    # =========================
    # SUCCESS LOGIN
    # =========================
    user.FAILED_LOGIN_ATTEMPTS = 0
    user.LAST_LOGIN = timezone.now()
    user.save()

    refresh = RefreshToken.for_user(user)

    return Response({
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh)
    })
    
import os
import json
from sqlite3 import DatabaseError, OperationalError
import random, string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt       
from tokenize import TokenError
from django.http import JsonResponse
from django.contrib.auth import authenticate, login,logout
from core.utils.response import RTYError
from core.utils import jwt
from core.utils.jwt import create_access_token, create_refresh_token, decode_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from accounts.authentication import JWTAuthentication

# ACCESS_EXP = 60 * 60            # 1 hour
# REFRESH_EXP = 7 * 24 * 60 * 60  # 7 days

"""Custom import"""
from core.utils.decryption import decrypt_cryptojs
from core.utils.jwt import generate_jwt_token, decode_jwt_token
from core.utils.jwt_handler import generate_tokens
from accounts.users.models import Users as User
from accounts.auth.serializers import UserLoginSerializer,LoginSerializer
from accounts.users.serializers import UserSerializer
# from accounts.auth_serializers import LoginSerializer
from core.utils.jwt import GENERATE_REMEMBER_TOKEN

# Determine if running in production
IS_PRODUCTION = os.environ.get('DJANGO_ENV') == 'production'
ACCESS_EXP = getattr(settings, "JWT_ACCESS_TOKEN_EXPIRES_SECONDS",900)         # fallback 15 min
REFRESH_EXP=  getattr(settings, "JWT_REFRESH_TOKEN_EXPIRES_SECONDS", 604800)  # fallback 7 days

# @csrf_exempt
class RegisterView(APIView):
    def post(self, request):
        data = request.data

        if User.objects.filter(CODE=data["Code"]).exists():
            print("User code already exist!")
            return Response({"Error": "User code already exist!"}, status=400)

        if User.objects.filter(USERNAME=data["Username"]).exists():
            print("Username already taken")
            return Response({"Error": "Username already taken"}, status=400)
    
        if User.objects.filter(EMAIL=data["Email"]).exists():
            print("Email already exists")
            return Response({"Error": "Email already exists"}, status=400)

        user = User.objects.create(
            # CODE="USR" + ''.join(random.choices(string.digits, k=5)),
            CODE = data["Code"],
            NAME=data["Name"],
            USERNAME=data["Username"],
            EMAIL=data["Email"],
            PASSWORD=make_password(data["Password"]),
            USER_TYPE=data.get("UserType", "GENERAL"),
            PHONE_NUMBER=data.get("PhoneNumber", ""),
            IMAGE_PATH=data.get("ImagePath", "")
        )

        tokens = generate_tokens(user)

        # Use PascalCase in response
        response_data = {
            "Code": user.CODE,
            "Name": user.NAME,
            "Username": user.USERNAME,
            "Email": user.EMAIL,
            "UserType": user.USER_TYPE,
            "PhoneNumber": user.PHONE_NUMBER,
            "ImagePath": user.IMAGE_PATH,
            "Tokens": tokens
        }

        return Response(response_data, status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            print("Login data received:", data)
            remember = data.get('IsRemember', False)
            raw_username = data.get('Username')
            raw_password = data.get('Password')
            raw_device_id = data.get('DeviceId')

            if raw_username is None:
                return RTYError(
                    error_message="Missing Username",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if raw_password is None:
                return RTYError(
                    error_message="Missing Password",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # -----------------------------
            # Now safe to decrypt  node
            # 1. DECRYPT
            # -----------------------------
            username = decrypt_cryptojs(raw_username)
            password = decrypt_cryptojs(raw_password)
            device_id = decrypt_cryptojs(raw_device_id) if raw_device_id else None
            
            print("Decrypted username:", username)
            print("Decrypted password:", password)
            print("Decrypted device_id:", device_id)
            if username is None:
                return RTYError(
                    error_message="Missing Username",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if password is None:
                return RTYError(
                    error_message="Missing Password",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
           
            # -----------------------------
            # 2. FETCH USER
            # -----------------------------
            try:
                user = User.objects.get(USERNAME=username)
            except User.DoesNotExist:
                return RTYError(
                        error_message='Username incorrect',
                        error_code='invalid_username',
                        status_code=status.HTTP_401_UNAUTHORIZED
                    )

            if not check_password(password, user.PASSWORD):
                return RTYError(
                    error_message='Password incorrect',
                    error_code='invalid_password',
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

            # -----------------------------
            # 3. CREATE CUSTOM TOKENS
            # -----------------------------
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)

            # -----------------------------
            # 4. RESPONSE BODY
            # -----------------------------
            response = Response({
                "AccessToken": access_token,
                "RefreshToken": refresh_token,
                "AccessTokenExpiresIn": ACCESS_EXP,
                "RefreshTokenExpiresIn": REFRESH_EXP,
                "Name": user.NAME,
                "Username": user.USERNAME,
                "UserType": user.USER_TYPE,
                "IsRemember": remember,
            })

            # -----------------------------
            # 5. HTTP-ONLY COOKIES
            # -----------------------------
            response.set_cookie(
                key='rty_access_token',
                value=access_token,
                httponly=True,
                secure=IS_PRODUCTION,
                samesite='Lax',
                max_age=ACCESS_EXP,
                path='/'
            )

            response.set_cookie(
                key='rty_refresh_token',
                value=refresh_token,
                httponly=True,
                secure=IS_PRODUCTION,
                samesite='Lax',
                max_age=REFRESH_EXP,
                path='/'
            )

            # -----------------------------
            # 6. REMEMBER ME
            # -----------------------------
            if remember:
                response.set_cookie(
                    key='remembered',
                    value=username,
                    max_age=30 * 24 * 60 * 60,
                    samesite='Lax'
                )
                user.IS_REMEMBER = True
            else:
                response.delete_cookie('remembered')
                user.IS_REMEMBER = False

            user.IS_LOGIN = True
            # user.save()
            user.save(update_fields=['IS_LOGIN', 'IS_REMEMBER'])
            return response

        except Exception as e:
            print("Login error:", e)
            return Response(
                {'Success': False, 'Message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except (OperationalError, DatabaseError):
            # Database connection failed
            return Response({'Error': 'Login failed, please try again later'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            # Other unexpected errors
            print("Login error:", e)
            return Response({'Error': 'Unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # 1️⃣ Get refresh token (cookie preferred)
            refresh_token = request.COOKIES.get("rty_refresh_token") \
                            or request.data.get("refreshToken")
            print("Refresh token received------------:", refresh_token)
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2️⃣ Decode token using your existing function
            payload = decode_token(refresh_token)  # must return dict or raise Exception

            # 3️⃣ Check token type
            if payload.get("type") != "refresh":
                return Response(
                    {"error": "Invalid token type"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 4️⃣ Get user
            try:
                user = User.objects.get(ID=payload["user_id"], IS_ACTIVE=True)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Optional: prevent refresh if user logged out
            if not user.IS_LOGIN:
                return Response(
                    {"error": "User is logged out"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 5️⃣ Create new access token
            new_access_token = create_access_token(user)

            response = Response({
                "AccessToken": new_access_token,
                # "AccessTokenExpiresAt": ACCESS_EXP,
            })

            # 6️⃣ Set cookie for access token
            response.set_cookie(
                key="rty_access_token",
                value=new_access_token,
                httponly=True,
                secure=getattr(settings, "IS_PRODUCTION", False),
                samesite="Lax",
                max_age=ACCESS_EXP,
                path="/"
            )

            return response

        except Exception as e:
            print("Refresh error:", e)
            return Response(
                {"Error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logout the user by blacklisting the refresh token and clearing cookies.
        """
        try:
            # -----------------------------
            # 1. Get refresh token from request data or cookie
            # -----------------------------
            refresh_token = request.data.get("refresh") or request.COOKIES.get("rty_refresh_token")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # -----------------------------
            # 2. Blacklist the token
            # -----------------------------
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                # Token invalid, expired, or already blacklisted
                pass  # Still proceed to clear cookies

            # -----------------------------
            # 3. Clear cookies
            # -----------------------------
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie("rty_access_token", path="/")
            response.delete_cookie("rty_refresh_token", path="/")
            response.delete_cookie("remembered", path="/")

            # -----------------------------
            # 4. Update user status in DB
            # -----------------------------
            user = request.user
            if user.is_authenticated:
                user.IS_LOGIN = False
                user.save(update_fields=["IS_LOGIN"])

            return response

        except Exception as e:
            print("Logout error:", e)
            return Response(
                {"error": "Logout failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print("Requested user -----> ", request.user)
        user = request.user  # AUTO populated

        data = {
            "Id": user.ID,
            "Username": user.USERNAME,
            "Email": user.EMAIL,
            "Name": user.NAME,
            "UserType": user.USER_TYPE,
            "PhoneNumber": user.PHONE_NUMBER,
        }
        return Response(data, status=status.HTTP_200_OK)

    
class ProtectedProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You are authenticated!'})


"""5. How Django Stores This
Without Remember Me
Session expires → browser closed

With Remember Me
sessionid cookie saved to disk
expires in 14 days

"""
    
"""
FLOW SUMMARY

    User → Forgot Password
        ↓
    Generate Token (UUID)
        ↓
    Store in DB (30 min expiry)
        ↓
    User → Reset Password
        ↓
    Validate Token
        ↓
    Update PASSWORD_HASH
        ↓
    Mark token USED
"""