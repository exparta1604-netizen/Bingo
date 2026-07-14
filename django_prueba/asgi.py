"""
ASGI config for django_prueba project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_prueba.settings')


# 2. ¡MUY IMPORTANTE! Encendemos el motor de Django ANTES de importar los WebSockets
django_asgi_app = get_asgi_application()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django_prueba.routing import websocket_urlpatterns



# 3. Declaramos la aplicación principal que usará Daphne
application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AuthMiddlewareStack(
    URLRouter(
      websocket_urlpatterns
    )
  ),
})


