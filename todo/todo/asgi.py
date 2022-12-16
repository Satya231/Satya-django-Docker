import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application,URLRouter
import app.routing
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket' : AuthMiddlewareStack(URLRouter(
            app.routing.websocket_urlpatterns
        )
        ),
        # Just HTTP for now. (We can add other protocols later.)
    }
)