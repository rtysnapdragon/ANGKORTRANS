from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from .models import User
from accounts.auth.models import User, AuthAuditLog, RefreshToken
from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from accounts.users.models import User, UserProfile
from accounts.auth.models import UserOTP
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import User, UserProfile
from accounts.auth.serializers import (
    LoginSerializer,
    UserOTPSerializer
)
from accounts.users.serializers import UserSerializer, UserProfileSerializer


# ====================== USER ======================
# ====================== GET USER LIST ======================
@api_view(['POST'])
def user_list(request):
    print("Received user list request with data:", request.data)  # Debugging line
    """
    Get list of users
    Supports optional filtering via POST body
    """
    try:
        # Base queryset - exclude soft deleted users
        queryset = User.objects.filter(IS_DELETED=False).order_by('-CREATED_AT')

        # Optional filtering from request body
        username = request.data.get('Username')
        email = request.data.get('Email')
        status = request.data.get('Status')
        user_type = request.data.get('UserType')

        if username:
            queryset = queryset.filter(USERNAME__icontains=username)
        if email:
            queryset = queryset.filter(EMAIL__icontains=email)
        if status:
            queryset = queryset.filter(STATUS=status)
        if user_type:
            queryset = queryset.filter(USER_TYPE=user_type)

        # Pagination (optional)
        page = int(request.data.get('Page', 1))
        page_size = int(request.data.get('PageSize', 20))
        start = (page - 1) * page_size
        end = start + page_size

        users = queryset[start:end]
        total = queryset.count()

        serializer = UserSerializer(users, many=True)

        return Response({
            "Message": "Users retrieved successfully",
            "Users": serializer.data,
            "Total": total,
            "Page": page,
            "PageSize": page_size
        })

    except Exception as e:
        return Response({
            "Message": f"Error retrieving users: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(CREATED_BY=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk, IS_DELETED=False)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(UPDATED_BY=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.IS_DELETED = True
    user.save()
    return Response({"Message": "User soft deleted successfully"})


# ====================== USER PROFILE ======================
@api_view(['POST'])
def user_profile_list(request):
    profiles = UserProfile.objects.all()
    serializer = UserProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def user_profile_create(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(CREATED_BY=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_profile_update(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(UPDATED_BY=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def create_user(request):

    data = request.data

    try:
        with transaction.atomic():

            # ======================
            # 1. CREATE USER
            # ======================
            user = User.objects.create(
                CODE=data.get('Code'),
                USERNAME=data.get('Username'),
                EMAIL=data.get('Email'),
                USER_TYPE=data.get('UserType', 'USER'),
                STATUS=data.get('Status', 'ACTIVE'),
                IS_SUPERUSER=data.get('IsSuperuser', False),

                FAILED_LOGIN_ATTEMPTS=0,
                IS_DELETED=False,

                CREATED_BY=request.user
            )

            user.set_password(data.get('Password'))
            user.save()

            # ======================
            # 2. CREATE PROFILE
            # ======================
            profile = UserProfile.objects.create(
                USER_ID=user,

                # ---- BASIC INFO ----
                NAME=data.get('Name'),
                NAME_ENGLISH=data.get('NameEnglish'),
                GENDER=data.get('Gender'),
                DOB=data.get('DateOfBirth'),
                POB=data.get('PlaceOfBirth'),
                MARITAL_STATUS=data.get('MaritalStatus'),
                NATIONAL_ID=data.get('NationalId'),
                NATIONALITY=data.get('Nationality'),
                OCCUPATION=data.get('Occupation'),

                # ---- ADDRESS (FKs) ----
                COUNTRY_ID_id=data.get('CountryId', 1),
                PROVINCE_ID_id=data.get('ProvinceId'),
                DISTRICT_ID_id=data.get('DistrictId'),
                COMMUNE_ID_id=data.get('CommuneId'),
                VILLAGE_ID_id=data.get('VillageId'),

                # ---- ADDRESS TEXT ----
                ADDRESS_LINE1=data.get('AddressLine1'),
                ADDRESS_LINE2=data.get('AddressLine2'),
                ZIP_CODE=data.get('ZipCode'),
                POSTAL_CODE=data.get('PostalCode'),

                # ---- MEDIA ----
                PROFILE_PICTURE_URL=data.get('ProfilePictureUrl'),
                SIGNATURE_URL=data.get('SignatureUrl'),

                # ---- EXTRA INFO ----
                BIO=data.get('Bio'),
                LANGUAGE_PREFERENCE=data.get('LanguagePreference', 'km'),
                TIMEZONE=data.get('Timezone', 'Asia/Phnom_Penh'),
                IS_VERIFIED=data.get('IsVerified', False),

                # ---- SOCIAL ----
                FACEBOOK_LINK=data.get('FacebookLink'),
                TIKTOK_LINK=data.get('TiktokLink'),
                LINKEDIN_LINK=data.get('LinkedinLink'),
                WEBSITE=data.get('Website'),

                CREATED_BY=request.user
            )

            return Response({
                "message": "User created successfully",
                "user_id": user.ID,
                "profile_id": profile.USER_ID
            }, status=status.HTTP_201_CREATED)


    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)