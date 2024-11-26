# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import myapp.routing  # Make sure this matches your app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro_api3.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            myapp.routing.websocket_urlpatterns  # Import the websocket_urlpatterns
        )
    ),
})
