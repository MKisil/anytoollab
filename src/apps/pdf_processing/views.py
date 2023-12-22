from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from src.apps.pdf_processing import services
from src.apps.pdf_processing import tasks
from src.apps.pdf_processing.forms import PDFFileUploadForm, PDFFileEncryptForm, PDFFileDecryptForm
from src.apps.pdf_processing.models import File


class DownloadResultView(TemplateView):
    template_name = 'pdf_processing/download_result.html'

    def get(self, request, *args, **kwargs):
        file_obj = get_object_or_404(File, id=self.kwargs['file_id'])
        if file_obj.is_used:
            return HttpResponseRedirect(reverse('home'))
        else:
            file_obj.is_used = True
            file_obj.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file_id'] = self.kwargs.get('file_id')
        return context


class PdfTextExtractView(FormView):
    form_class = PDFFileUploadForm
    template_name = 'pdf_processing/pdf_processing.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.extract_text_from_pdf.delay(services.full_path(file_obj.file.path), str(file_obj.id))
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_id': file_obj.id}))


class PdfEncryptView(FormView):
    form_class = PDFFileEncryptForm
    template_name = 'pdf_processing/pdf_processing.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_encrypt.delay(services.full_path(file_obj.file.path), str(file_obj.id), form.cleaned_data['password'])
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_id': file_obj.id}))


class PdfDecryptView(FormView):
    form_class = PDFFileDecryptForm
    template_name = 'pdf_processing/pdf_processing.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_decrypt.delay(services.full_path(file_obj.file.path), str(file_obj.id), form.cleaned_data['password'])
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_id': file_obj.id}))


class PdfCompressView(FormView):
    form_class = PDFFileUploadForm
    template_name = 'pdf_processing/pdf_processing.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_compress.delay(services.full_path(file_obj.file.path), str(file_obj.id))
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_id': file_obj.id}))

# class TestView(FormView):
#     form_class = PDFFileUploadForm
#     template_name = 'pdf_processing/pdf_processing.html'
#     success_url = 'home'
#
#     def form_valid(self, form):
#         time.sleep(100)
#         super().form_valid()
