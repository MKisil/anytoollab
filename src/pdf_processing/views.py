import time
from urllib.parse import quote

from django.http import JsonResponse, FileResponse
from django.views.generic import FormView

from src.pdf_processing import services
from src.pdf_processing.forms import PDFFileUploadForm, PDFFileProtectForm


class PdfTextExtractView(FormView):
    form_class = PDFFileUploadForm
    template_name = 'pdf_processing/pdf_processing.html'

    def form_invalid(self, form):
        return JsonResponse({'message': 'Некорректний pdf файл'})

    def form_valid(self, form):
        text = services.extract_text_from_pdf(form.cleaned_data['file'])
        headers = {'Content-Disposition': 'attachment; filename="text_from_pdf.txt"'}
        return FileResponse(
            text,
            content_type='text/plain',
            headers=headers
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Витягти текст із pdf'
        context['form_btn_text'] = 'Витягти текст'
        return context


class PdfProtectView(FormView):
    form_class = PDFFileProtectForm
    template_name = 'pdf_processing/pdf_processing.html'

    def form_invalid(self, form):
        # print([str(error) for field, error in form.errors.items()])
        return JsonResponse({'message': 'Некорректний pdf файл'})

    def form_valid(self, form):
        protected_pdf_file = services.pdf_protect(form.cleaned_data['file'], form.cleaned_data['password'])
        return FileResponse(
            protected_pdf_file,
            as_attachment=True,
            filename='protected_pdf.pdf',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Захистити pdf'
        context['form_btn_text'] = 'Створити пароль для вибраного файлу'
        return context
