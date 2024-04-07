import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .middlewares.ws_auth import JwtAuthMiddleware
from .routing import websocket_urlpatterns

django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':  JwtAuthMiddleware(URLRouter(websocket_urlpatterns))
})

