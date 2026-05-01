from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/follow', follow, name='follow'),
    path('api/v1/unfollow', unfollow, name='unfollow'),
    path('api/v1/followers', follower, name='followers'),
    path('api/v1/following', following, name='following'),
    path('api/v1/follow-status', follow_status, name='follow_status'),
]