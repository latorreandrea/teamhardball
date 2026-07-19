"""
ASGI config for teamhardball project.

Routes both HTTP and WebSocket traffic through Django Channels.
Used by Daphne (and Cloud Run) for production deployment.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamhardball.settings')

from tactical.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns),
    ),
})