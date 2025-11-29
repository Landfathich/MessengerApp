import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chat.routing  # ← убедитесь что этот импорт есть

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessangerApp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # ← используем routing из chat
        )
    ),
})
