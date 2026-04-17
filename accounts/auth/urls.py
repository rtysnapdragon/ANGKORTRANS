from atexit import register
print("Loading auth views..register ." ,register)

from django.urls import include, path
from .views import (
    admin_reset_password,
    auth_login,
    auth_refresh,
    auth_logout,
    auth_me,
    forgot_password,
    login,
    oauth_token,
    register,
    reset_password,
    reset_password_and_renew,
    reset_password_no_token,
    user_otp_list, user_otp_create,
)

urlpatterns = [
    
    path('rtyAuth/Token', oauth_token, name='auth-oauth-token'),
    path('api/auth/register', register, name='auth-register'),
    # path('api/auth/login', login, name='auth-login'),
    # Login → POST
    # path('api/auth/login', auth_login, name='auth-login'),

    # Refresh Token → POST
    path('api/auth/refresh', auth_refresh, name='auth-refresh'),

    # Logout → POST
    path('api/auth/logout', auth_logout, name='auth-logout'),

    # Get Current User (protected) → POST (you can change to GET if you prefer)
    path('api/auth/me', auth_me, name='auth-me'),
    
    # Auth
    path('api/auth/login', auth_login, name='auth-login'),
    
    path('api/auth/reset_password', reset_password, name='auth-reset-password'),
    path('api/auth/forgot_password', forgot_password, name='auth-forgot-password'),
    path('api/auth/reset_password_no_token', reset_password_no_token, name='auth-reset-password-no-token'),
    path('api/auth/reset_password_and_renew', reset_password_and_renew, name='auth-reset-password-and-renew'),
    path('api/auth/admin_reset_password', admin_reset_password, name='auth-admin-reset-password'),

    # OTP
    path('api/user_otp/list', user_otp_list, name='user-otp-list'),
    path('api/user_otp/create', user_otp_create, name='user-otp-create'),
]
