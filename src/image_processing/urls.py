from django.urls import path

from src.image_processing import views

app_name = 'image'

urlpatterns = [
    path('', views.ImageProcessingView.as_view(), name='image_processing'),
]
