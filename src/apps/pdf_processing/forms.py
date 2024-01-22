import re

from django import forms
from pypdf.errors import PdfReadError, FileNotDecryptedError
from pypdf import PdfReader
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PDFFileUploadForm(forms.Form):
    file = forms.FileField(label='Файл', widget=forms.FileInput(attrs={'accept': 'application/pdf'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Здійснити', css_class='btn btn-primary'))
        self.helper.form_id = 'pdf_form'

    def clean_file(self):
        file = self.cleaned_data['file']
        try:
            reader = PdfReader(file)
        except PdfReadError:
            raise forms.ValidationError('Incorrect pdf file.')
        else:
            return file


class PDFFileEncryptForm(PDFFileUploadForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(), label='Пароль',
                               help_text='Пароль може містити латинські букви, цифри і !@#$%^&*()')

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 3:
            raise forms.ValidationError('Пароль надто короткий.')

        elif not bool(re.match('^[0-9a-zA-Z!@#$%^&*()]{3,}$', password)):
            raise forms.ValidationError('Пароль містить некорректні символи.')

        return password


class PDFFileDecryptForm(PDFFileUploadForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(), label='Пароль',
                               help_text='Введіть пароль, яким зашифровано pdf файл')

    def clean(self):
        super(PDFFileDecryptForm, self).clean()
        file = self.cleaned_data['file']
        password = self.cleaned_data['password']
        try:
            reader = PdfReader(file)
            if not reader.is_encrypted:
                raise forms.ValidationError('PDF файл не зашифрований.')
            if not reader.decrypt(password):
                raise forms.ValidationError('Невірний пароль.')
        except PdfReadError:
            raise forms.ValidationError('Некорректний pdf файл.')

        return self.cleaned_data

    def clean_file(self):
        return self.cleaned_data['file']


class PDFFileSplitForm(PDFFileUploadForm):
    password = forms.CharField(max_length=30)
    selected_pages = forms.CharField(max_length=1000)
    save_separate = forms.BooleanField()

    def clean_password(self):
        return self.cleaned_data['password']

    def clean_selected_pages(self):
        selected_pages = self.cleaned_data['selected_pages']

        if not selected_pages.replace(',', '').isdigit():
            raise forms.ValidationError('Incorrect page numbers.')

        return selected_pages


