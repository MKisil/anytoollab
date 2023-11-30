import time

from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView

from src.pdf_processing import services
from src.pdf_processing.forms import PDFFileUploadForm, PDFFileProtectForm
from src.pdf_processing.models import File


class DownloadResultView(TemplateView):
    template_name = 'pdf_processing/download_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_file = get_object_or_404(File, id=self.kwargs['file_uuid'])
        context['url'] = obj_file.file.url
        return context


class PdfTextExtractView(FormView):
    form_class = PDFFileUploadForm
    template_name = 'pdf_processing/pdf_processing.html'

    def form_valid(self, form):
        obj_file = File.objects.create(file=form.cleaned_data['file'])
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_uuid': obj_file.id}))
        # text = services.extract_text_from_pdf(form.cleaned_data['file'])
        # headers = {'Content-Disposition': 'attachment; filename="text_from_pdf.txt"'}
        # return FileResponse(
        #     text,
        #     content_type='text/plain',
        #     headers=headers
        # )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Витягти текст із pdf'
        context['form_btn_text'] = 'Витягти текст'
        return context


class PdfProtectView(FormView):
    form_class = PDFFileProtectForm
    template_name = 'pdf_processing/pdf_processing.html'

    def form_invalid(self, form):
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

# class TestView(FormView):
#     form_class = PDFFileUploadForm
#     template_name = 'pdf_processing/pdf_processing.html'
#     success_url = 'home'
#
#     def form_valid(self, form):
#         time.sleep(100)
#         super().form_valid()
