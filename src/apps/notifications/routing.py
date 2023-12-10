from django.urls import path

from src.apps.notifications import consumers

websocket_urlpatterns = [
    path("ws/download_result/<str:file_id>/", consumers.NotificationConsumer.as_asgi()),
]