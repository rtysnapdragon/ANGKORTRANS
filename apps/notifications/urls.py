from django.urls import path
from .views import *

urlpatterns = [
    path('api/notifications', NotificationsView.as_view()),
    path('api/notifications/read', ReadNotification.as_view()),
    path('api/notifications/read-all', ReadAll.as_view()),
    path('api/notifications/count', UnreadNotificationCount.as_view()),
]