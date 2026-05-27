from django.urls import path

from accounts.telegram.views import (
    telegram_login_view
)

urlpatterns = [

    path(
        '/api/auth/telegram/login',
        telegram_login_view,
        name='telegram-login'
    ),

]