from django.urls import path

from src.pdf_processing import views

app_name = 'pdf'

urlpatterns = [
    path('protect/', views.PdfProtectView.as_view(), name='protect'),
    path('text-extract/', views.PdfTextExtractView.as_view(), name='text_extract'),
]
