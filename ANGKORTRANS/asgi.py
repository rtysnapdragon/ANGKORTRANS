"""
ASGI config for ANGKORTRANS project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANGKORTRANS.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

django_asgi_app = get_asgi_application()

from apps.notifications.websoket.routing import websocket_urlpatterns


# ❗ Lazy import to avoid AppRegistryNotReady
from apps.notifications.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})

"""
No token from frontend, use below
"""
# application = ProtocolTypeRouter({
#     "http": http_application,
#     "websocket": AuthMiddlewareStack(
#         URLRouter(websocket_urlpatterns)
#     ),
# })
