"""
ASGI config for proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from pprint import pprint

import django
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
django.setup()
application = get_default_application()
import admin_p.routing

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(admin_p.routing.websocket_urlpatterns))
        ),

})