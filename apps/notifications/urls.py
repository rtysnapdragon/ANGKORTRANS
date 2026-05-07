from django.urls import path
from .views import *

urlpatterns = [
    path('api/notifications', notifications, name='notifications'),
    path('api/notifications/read', read_notification, name='read_notification'),
    path('api/notifications/read-all', read_all, name='read_all'),
    path('api/notifications/count', unread_notifications_count, name='unread_notifications_count'),
    path("api/notifications/clear", clear_all_notifications,name="clear_all_notifications"),
    path("api/notifications/delete-all", clear_all_notifications,name="delete_all_notifications"),
    path("api/notifications/delete", delete_notification,name="delete_notification"),
]