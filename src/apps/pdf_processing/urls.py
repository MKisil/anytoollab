from django.urls import path

from src.apps.pdf_processing import views

app_name = 'pdf'

urlpatterns = [
    path('split/', views.PdfSplitView.as_view(), name='split'),
    path('encrypt/', views.PdfEncryptView.as_view(), name='encrypt'),
    path('decrypt/', views.PdfDecryptView.as_view(), name='decrypt'),
    path('compress/', views.PdfCompressView.as_view(), name='compress'),
    path('text-extract/', views.PdfTextExtractView.as_view(), name='text_extract'),
    path('download-result/<str:file_id>/', views.DownloadResultView.as_view(), name='download_result')
]
