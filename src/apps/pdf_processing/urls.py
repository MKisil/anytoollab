from django.urls import path

from src.apps.pdf_processing import views

app_name = 'pdf'

urlpatterns = [
    path('test/', views.TestView.as_view(), name='test'),
    path('rotate/', views.PdfRotateView.as_view(), name='rotate'),
    path('split/', views.PdfSplitView.as_view(), name='split'),
    path('encrypt/', views.PdfEncryptView.as_view(), name='encrypt'),
    path('decrypt/', views.PdfDecryptView.as_view(), name='decrypt'),
    path('compress/', views.PdfCompressView.as_view(), name='compress'),
    path('img-to-pdf/', views.ImgToPdfView.as_view(), name='img_to_pdf'),
    path('text-extract/', views.PdfTextExtractView.as_view(), name='text_extract'),
    path('delete-pages/', views.PdfDeletePagesView.as_view(), name='delete_pages'),
    path('add-page-numbers/', views.PdfAddPageNumbersView.as_view(), name='add_page_numbers'),
    path('download-result/<str:file_id>/', views.DownloadResultView.as_view(), name='download_result')
]
