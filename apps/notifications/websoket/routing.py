from django.urls import path, include
from .consumer import NotificationConsumer

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]