from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('',include('accounts.auth.urls')),
    path('',include('accounts.users.urls')),
    path('', include('accounts.rbac.urls')),
]