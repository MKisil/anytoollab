from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView

from src.apps.pdf_processing import services
from src.apps.pdf_processing import tasks
from src.apps.pdf_processing import forms
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
    form_class = forms.PDFFileUploadForm
    template_name = 'pdf_processing/file_upload.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.extract_text_from_pdf.delay(services.full_path(file_obj.file.path), str(file_obj.id))
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_id': file_obj.id}))


class PdfEncryptView(FormView):
    form_class = forms.PDFFileEncryptForm
    template_name = 'pdf_processing/file_upload.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_encrypt.delay(services.full_path(file_obj.file.path), str(file_obj.id), form.cleaned_data['password'])
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_id': file_obj.id}))


class PdfDecryptView(FormView):
    form_class = forms.PDFFileDecryptForm
    template_name = 'pdf_processing/file_upload.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_decrypt.delay(services.full_path(file_obj.file.path), str(file_obj.id), form.cleaned_data['password'])
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_id': file_obj.id}))


class PdfCompressView(FormView):
    form_class = forms.PDFFileUploadForm
    template_name = 'pdf_processing/file_upload.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_compress.delay(services.full_path(file_obj.file.path), str(file_obj.id))
        return HttpResponseRedirect(reverse('pdf:download_result', kwargs={'file_id': file_obj.id}))


@method_decorator(csrf_exempt, name='dispatch')
class PdfSplitView(TemplateView):
    template_name = 'pdf_processing/pdf_split.html'

    def post(self, request, *args, **kwargs):
        form = forms.PDFFileSplitForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = File.objects.create(file=form.cleaned_data['file'])
            tasks.pdf_split.delay(
                file_path=services.full_path(file_obj.file.path),
                file_id=str(file_obj.id),
                selected_pages=form.cleaned_data.get('selected_pages', []),
                save_separate=form.cleaned_data.get('save_separate', False),
                password=form.cleaned_data.get('password', ''),
            )
            return JsonResponse({'message': 'success', 'file_id': file_obj.id})
        else:
            return JsonResponse({'message': 'error'})


@method_decorator(csrf_exempt, name='dispatch')
class PdfAddPageNumbersView(TemplateView):
    template_name = 'pdf_processing/pdf_addpagenumbers.html'

    def post(self, request, *args, **kwargs):
        form = forms.PDFFileAddPageNumbersForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = File.objects.create(file=form.cleaned_data['file'])
            tasks.pdf_addpagenumbers.delay(
                file_path=services.full_path(file_obj.file.path),
                file_id=str(file_obj.id),
                password=form.cleaned_data.get('password', ''),
                number_on_first_page=form.cleaned_data.get('number_on_first_page', False),
                number_position=form.cleaned_data.get('number_position', 'c-bottom')
            )
            return JsonResponse({'message': 'success', 'file_id': file_obj.id})
        else:
            return JsonResponse({'message': 'error'})


@method_decorator(csrf_exempt, name='dispatch')
class PdfRotateView(TemplateView):
    template_name = 'pdf_processing/pdf_rotate.html'

    def post(self, request, *args, **kwargs):
        form = forms.PDFFileRotateForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = File.objects.create(file=form.cleaned_data['file'])
            tasks.pdf_rotate.delay(
                file_path=services.full_path(file_obj.file.path),
                file_id=str(file_obj.id),
                password=form.cleaned_data.get('password', ''),
                document_rotation=form.cleaned_data.get('document_rotation', 0),
                pages_rotation=form.cleaned_data.get('pages_rotation', {})
            )
            return JsonResponse({'message': 'success', 'file_id': file_obj.id})
        else:
            return JsonResponse({'message': 'error'})

# class TestView(FormView):
#     form_class = forms.PDFFileAddPageNumbersForm
#     template_name = 'pdf_processing/test.html'
#
#     def post(self, request, *args, **kwargs):
#         form = forms.PDFFileAddPageNumbersForm(request.POST, request.FILES)
#         form.is_valid()
#         print(request.POST)
#         return JsonResponse({'message': 'error'})
