from django.urls import path, include
from main.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    path('ads/', ChatConsumer.as_asgi()),
]