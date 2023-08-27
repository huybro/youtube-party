import os

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import app.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    )
})

