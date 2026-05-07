from django.urls import path, include,re_path
from .consumer import NotificationConsumer

# websocket_urlpatterns = [
#     path("ws/notifications/", NotificationConsumer.as_asgi()),
# ]

# notifications/routing.py

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]