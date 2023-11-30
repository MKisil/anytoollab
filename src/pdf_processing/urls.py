from django.urls import path

from src.pdf_processing import views

app_name = 'pdf'

urlpatterns = [
    path('protect/', views.PdfProtectView.as_view(), name='protect'),
    path('text-extract/', views.PdfTextExtractView.as_view(), name='text_extract'),
    path('download-result/<str:file_uuid>/', views.DownloadResultView.as_view(), name='download_result')
]
