from django.urls import path

from src.pdf_processing import views

urlpatterns = [
    path('text-extract/', views.PdfProcessingView.as_view(), name='text_extract')
]
