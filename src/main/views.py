import io

from django.http import JsonResponse, FileResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from . import services
from .forms import PDFFileUploadForm


class IndexView(TemplateView):
    template_name = 'home.html'


class ImageProcessingView(TemplateView):
    template_name = 'image_processing.html'


# class QrCodeGenerationView(FormView):
#     template_name = 'qrcode.html'
#     form_class = QrCodeForm
#
#     def form_valid(self, form):
#         qrcode = services.generate_qrcode(form.cleaned_data['text_data'])
#         return self.render_to_response(self.get_context_data(qrcode=services.image_to_base64(qrcode, 'JPEG')))
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['qrcode'] = kwargs.get('qrcode')
#         return context

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
