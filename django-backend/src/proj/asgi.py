"""
ASGI config for proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
import sys
print(sys.path)
application = get_asgi_application()
import admin_p.routing

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(admin_p.routing.websocket_urlpatterns))
        ),

})