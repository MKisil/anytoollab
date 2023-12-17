from django.urls import path

from src.apps.pdf_processing import views

app_name = 'pdf'

urlpatterns = [
    path('encrypt/', views.PdfEncryptView.as_view(), name='encrypt'),
    path('decrypt/', views.PdfDecryptView.as_view(), name='decrypt'),
    path('text-extract/', views.PdfTextExtractView.as_view(), name='text_extract'),
    path('download-result/<str:file_id>/', views.DownloadResultView.as_view(), name='download_result')
]
