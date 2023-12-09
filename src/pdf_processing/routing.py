from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/download_result/<str:file_id>/", consumers.NotificationConsumer.as_asgi()),
]