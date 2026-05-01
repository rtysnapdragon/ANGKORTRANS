from django.urls import path
from .views import *

urlpatterns = [
    path('api/notifications', notifications, name='notifications'),
    path('api/notifications/read', read_notification, name='read_notification'),
    path('api/notifications/read-all', read_all, name='read_all'),
    path('api/notifications/count', unread_notifications_count, name='unread_notifications_count'),
]