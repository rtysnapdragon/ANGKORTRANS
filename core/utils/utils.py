# app/utils.py

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import requests
from riththy_app.users.models import USERS

def refresh_google_token(user):
    creds = Credentials(
        token=user.AccessToken,
        refresh_token=user.RefreshToken,
        token_uri=user.TokenUri,
        client_id=user.ClientId,
        client_secret=user.ClientSecret,
        scopes=user.Scope.split(',')
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        user.AccessToken = creds.token
        user.TokenExpiry = datetime.now() + timedelta(seconds=3500)
        user.save()
    return creds


def get_drive_service(user):
    creds = refresh_google_token(user)
    return build('drive', 'v3', credentials=creds)

from django.http import JsonResponse

def api_login_required1(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'Detail': 'Authentication required'},
                status=401
            )
        return view_func(request, *args, **kwargs)
    return wrapper



from django.http import JsonResponse
from django.conf import settings

def api_login_required(view_func):
    """
    Decorator to check authentication for API views
    using a custom USERS model.
    Returns 401 JSON if user is not authenticated.
    """
    def wrapper(request, *args, **kwargs):
        # Make sure request.user is populated
        user = getattr(request, 'user', None)
        print("user log -----------> ", user)
        # Check if user is authenticated and exists in custom USERS model
        if not user or not hasattr(user, 'username'):
            return JsonResponse({'Detail': 'Authentication required=============='}, status=401)

        try:
            # Ensure user exists in your custom USERS table
            # Match by username or email
            custom_user = USERS.objects.get(USERNAME=user.username)
            print("Custom user log -----------> ", custom_user)
        except USERS.DoesNotExist:
            return JsonResponse({'Detail': 'Authentication required'}, status=401)

        # Attach custom_user to request for convenience
        request.custom_user = custom_user

        return view_func(request, *args, **kwargs)

    return wrapper
