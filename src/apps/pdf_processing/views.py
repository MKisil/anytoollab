from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView

from src.apps.pdf_processing import services
from src.apps.pdf_processing import tasks
from src.apps.pdf_processing import forms
from src.apps.pdf_processing.models import File


@method_decorator(csrf_exempt, name='dispatch')
class PdfTextExtractView(FormView):
    form_class = forms.PDFFileUploadForm
    template_name = 'pdf_processing/pdf_text_extract.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.extract_text_from_pdf.delay(services.full_path(
            file_obj.file.path),
            str(file_obj.id),
            form.cleaned_data.get('password', ''),
        )
        return JsonResponse({'message': 'success', 'file_id': file_obj.id})

    def form_invalid(self, form):
        return JsonResponse({'message': 'error'})


@method_decorator(csrf_exempt, name='dispatch')
class PdfEncryptView(FormView):
    form_class = forms.PDFFileEncryptForm
    template_name = 'pdf_processing/pdf_encrypt.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_encrypt.delay(services.full_path(
            file_obj.file.path),
            str(file_obj.id),
            form.cleaned_data.get('password', ''),
            form.cleaned_data.get('new_password')
        )
        return JsonResponse({'message': 'success', 'file_id': file_obj.id})

    def form_invalid(self, form):
        return JsonResponse({'message': 'error'})


@method_decorator(csrf_exempt, name='dispatch')
class PdfDecryptView(FormView):
    form_class = forms.PDFFileDecryptForm
    template_name = 'pdf_processing/pdf_decrypt.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_decrypt.delay(services.full_path(file_obj.file.path), str(file_obj.id), form.cleaned_data['password'])
        return JsonResponse({'message': 'success', 'file_id': file_obj.id})

    def form_invalid(self, form):
        return JsonResponse({'message': 'error'})


class PdfCompressView(FormView):
    form_class = forms.PDFFileUploadForm
    template_name = 'pdf_processing/file_upload.html'

    def form_valid(self, form):
        file_obj = File.objects.create(file=form.cleaned_data['file'])
        tasks.pdf_compress.delay(services.full_path(file_obj.file.path), str(file_obj.id))
        return JsonResponse({'message': 'success', 'file_id': file_obj.id})

    def form_invalid(self, form):
        return JsonResponse({'message': 'error'})


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
        print(request.POST)
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


@method_decorator(csrf_exempt, name='dispatch')
class ImgToPdfView(TemplateView):
    template_name = 'pdf_processing/img_to_pdf.html'

    def post(self, request, *args, **kwargs):
        form = forms.ImgToPDFForm(request.POST, request.FILES)
        if form.is_valid():
            images = form.cleaned_data["images"]

            file_id = ''
            files_path = []
            for i, img in enumerate(images):
                file_obj = File.objects.create(file=img)
                files_path.append(services.full_path(file_obj.file.path))
                if i == 0:
                    file_id = file_obj.id

            tasks.img_to_pdf.delay(
                files_path=files_path,
                file_id=str(file_id),
                images_rotation=form.cleaned_data.get('images_rotation', []),
                orientation=form.cleaned_data.get('orientation', 'Auto orientation'),
                size=form.cleaned_data.get('size', 'A4')
            )

            return JsonResponse({'message': 'success', 'file_id': file_id})
        else:
            return JsonResponse({'message': 'error'})


@method_decorator(csrf_exempt, name='dispatch')
class PdfDeletePagesView(TemplateView):
    template_name = 'pdf_processing/pdf_delete_pages.html'

    def post(self, request, *args, **kwargs):
        form = forms.PDFDeletePagesForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = File.objects.create(file=form.cleaned_data['file'])
            tasks.pdf_delete_pages.delay(
                file_path=services.full_path(file_obj.file.path),
                file_id=str(file_obj.id),
                password=form.cleaned_data.get('password', ''),
                pages_to_delete=form.cleaned_data.get('selected_pages')
            )
            return JsonResponse({'message': 'success', 'file_id': file_obj.id})
        else:
            return JsonResponse({'message': 'error'})


class PdfEditorView(TemplateView):
    template_name = 'pdf_processing/pdf_editor.html'


class TestView(FormView):
    form_class = forms.TestForm
    template_name = 'pdf_processing/test.html'

    def post(self, request, *args, **kwargs):
        form = forms.TestForm(request.POST, request.FILES)
        print(form.is_valid())
        print(request.FILES, request.POST)
        return JsonResponse({'message': 'error'})
