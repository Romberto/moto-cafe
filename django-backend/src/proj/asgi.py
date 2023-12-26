import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from admin_p.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
        'websocket': AuthMiddlewareStack(
                URLRouter(
                    websocket_urlpatterns
                )
        )
    }
)
