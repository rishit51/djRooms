"""
ASGI config for dj_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_chat.settings')

django_app=get_asgi_application()

from .import urls # noqa isort:skip



application =ProtocolTypeRouter({
    "http":django_app,
    "websocket":URLRouter(urls.websocket_urlpatterns),
})
