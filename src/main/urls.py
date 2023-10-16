from django.urls import path

from src.main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('image_processing/', views.ImageProcessingView.as_view(), name='image_processing'),
    path('pdf/', views.PdfProcessingView.as_view(), name='pdf')
]
