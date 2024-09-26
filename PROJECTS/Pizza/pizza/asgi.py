"""
ASGI config for pizza project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza.settings')
from django.urls import path
from home.consumer import OrderProgress,ChatConsumer

application = get_asgi_application()

# ws_pattern = [
#         path("ws/pizza/<order_id>/", OrderProgress),
# ]

# application = ProtocolTypeRouter({
#     "websocket": (
#         (
#             URLRouter(ws_pattern)
#         )
#     ),
# })

django_asgi_app = get_asgi_application()
ws_pattern=[path("ws/main/", ChatConsumer),]
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': URLRouter(ws_pattern)
    # Just HTTP for now. (We can add other protocols later.)
})