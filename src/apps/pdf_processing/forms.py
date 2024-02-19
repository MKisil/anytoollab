import re

from PIL import Image
from django import forms
from pypdf.errors import PdfReadError
from pypdf import PdfReader


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = []
            for file_data in data:
                file = single_file_clean(file_data, initial)
                self.validate_image(file)
                result.append(file)
        else:
            result = single_file_clean(data, initial)
            self.validate_image(result)
        return result

    def validate_image(self, file):
        if not file.name.endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Only files with .png, .jpg or .jpeg extensions are allowed.")

        max_size = 200 * 1024 * 1024
        if file.size > max_size:
            raise forms.ValidationError("File size must be less than 200MB.")

        try:
            image = Image.open(file)
            image.verify()
        except Exception as e:
            raise forms.ValidationError("The file is not a valid image.")


class PDFFileUploadForm(forms.Form):
    file = forms.FileField()
    password = forms.CharField(max_length=250, required=False)

    def clean(self):
        super(PDFFileUploadForm, self).clean()

        file = self.cleaned_data['file']
        password = self.cleaned_data['password']

        max_size = 1024 * 1024 * 1024
        if file.size > max_size:
            raise forms.ValidationError('File size exceeds 1 GB.')

        try:
            reader = PdfReader(file)
            reader.pages

            if password:
                if not reader.decrypt(password):
                    raise forms.ValidationError('Invalid old password.')

        except PdfReadError:
            raise forms.ValidationError('Invalid pdf file.')

        return self.cleaned_data


class PDFFileEncryptForm(PDFFileUploadForm):
    new_password = forms.CharField(max_length=30,
                                   help_text='The password can contain Latin letters, numbers and !@#$%^&*()')

    def clean_new_password(self):
        password = self.cleaned_data['new_password']

        if len(password) < 3:
            raise forms.ValidationError('The password is too short.')

        elif not bool(re.match('^[0-9a-zA-Z!@#$%^&*()]{3,}$', password)):
            raise forms.ValidationError('Password contains invalid characters.')

        return password


class PDFFileDecryptForm(PDFFileUploadForm):
    password = forms.CharField(max_length=250, required=True)


class PDFFileSplitForm(PDFFileUploadForm):
    selected_pages = forms.CharField(max_length=1000)
    save_separate = forms.BooleanField()

    def clean_selected_pages(self):
        selected_pages = self.cleaned_data['selected_pages']

        if not selected_pages.replace(',', '').isdigit():
            raise forms.ValidationError('Incorrect page numbers.')

        return selected_pages

    def clean_save_separate(self):
        save_separate = self.cleaned_data['save_separate']

        if save_separate == 'on':
            return True
        else:
            return False


class PDFFileAddPageNumbersForm(PDFFileUploadForm):
    number_position = forms.CharField(max_length=10)
    number_on_first_page = forms.BooleanField(required=False)

    def clean_number_position(self):
        number_position = self.cleaned_data['number_position']

        if number_position not in ['l-top', 'c-top', 'r-top', 'l-bottom', 'c-bottom', 'r-bottom']:
            raise forms.ValidationError('Incorrect position value for page numbers.')
        return number_position


class PDFFileRotateForm(PDFFileUploadForm):
    document_rotation = forms.DecimalField(min_value=-270, max_value=270)
    pages_rotation = forms.JSONField()

    def clean_document_rotation(self):
        return int(self.cleaned_data['document_rotation'])

    def clean_pages_rotation(self):
        pages_rotation = self.cleaned_data['pages_rotation']

        if not ''.join(pages_rotation.keys()).replace('-', '0').isdigit():
            raise forms.ValidationError('Incorrect page numbers.')

        if len([angl for angl in pages_rotation.values() if angl % 10 == 0]) != len(pages_rotation.values()):
            raise forms.ValidationError('Incorrect rotating angles for pages.')

        return pages_rotation


class ImgToPDFForm(forms.Form):
    images = MultipleImageField()
    images_rotation = forms.JSONField()
    orientation = forms.CharField(max_length=20)
    size = forms.CharField(max_length=20)

    def clean_images_rotation(self):
        images_rotation = self.cleaned_data['images_rotation']

        for rotation in images_rotation:
            if not isinstance(rotation, int) and rotation is not None:
                raise forms.ValidationError('Incorrect rotating angles for images.')
            if rotation > 270 or rotation < -270:
                raise forms.ValidationError('Incorrect rotating angles for images.')

        return images_rotation

    def clean_orientation(self):
        orientation = self.cleaned_data['orientation']

        if orientation not in ['Auto orientation', 'Landscape', 'Portrait']:
            raise forms.ValidationError('Incorrect page orientation.')

        return orientation

    def clean_size(self):
        size = self.cleaned_data['size']

        if size not in ['A3', 'A4', 'A5', 'US Letter', 'US Legal', 'Original']:
            raise forms.ValidationError('Incorrect page size.')

        return size


class PDFDeletePagesForm(PDFFileUploadForm):
    selected_pages = forms.JSONField()

    def clean_selected_pages(self):
        selected_pages = list(self.cleaned_data['selected_pages'])

        if not all(isinstance(x, int) and x >= 0 for x in selected_pages):
            raise forms.ValidationError('Incorrect page numbers.')

        return selected_pages


class TestForm(forms.Form):
    images = MultipleImageField()

    def clean_files(self):
        files = self.cleaned_data['images']
        print(files)
        return files
