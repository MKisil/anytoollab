from django.urls import path

from src.image_processing import views

urlpatterns = [
    path('', views.ImageProcessingView.as_view(), name='image_processing'),
]
