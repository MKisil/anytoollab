import io

from django.http import JsonResponse, FileResponse
from django.views.generic import FormView

from src.pdf_processing import services
from src.pdf_processing.forms import PDFFileUploadForm


class PdfProcessingView(FormView):
    form_class = PDFFileUploadForm
    template_name = 'pdf_processing/pdf_text_extract.html'

    def form_invalid(self, form):
        return JsonResponse({'message': 'Некорректний pdf файл'})

    def form_valid(self, form):
        try:
            text = services.extract_text_from_pdf(form.cleaned_data['file']).replace('\n', '\r\n')
            buffer = io.BytesIO()
            buffer.write(text.encode('utf-8'))
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='result.txt', content_type='text/plain')
        except Exception:
            return JsonResponse({'message': 'Некорректний pdf файл.'})
