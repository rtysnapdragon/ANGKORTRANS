from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    user_list,create_user, user_update, user_delete,
    user_profile_list, user_profile_create, user_profile_update,
)

urlpatterns = [
   # User Management
    path('api/users/list', user_list, name='user-list'),
    path('api/users/create', create_user, name='user-create'),
    path('api/users/update', user_update, name='user-update'),
    path('api/users/delete', user_delete, name='user-delete'),

    # User Profile
    path('api/user_profiles/list', user_profile_list, name='user-profile-list'),
    path('api/user_profiles/create', user_profile_create, name='user-profile-create'),
    path('api/user_profiles/update', user_profile_update, name='user-profile-update'),
]