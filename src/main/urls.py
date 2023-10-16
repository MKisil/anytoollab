from django.urls import path

from src.main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('processing_image/', views.ImageProcessingView.as_view(), name='processing_image'),
    path('pdf/', views.ProcessingPdfView.as_view(), name='pdf')
    # path('generation_qrcode/', views.QrCodeGenerationView.as_view(), name='generation_qrcode'),
]
