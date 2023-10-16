from django import forms


class QrCodeForm(forms.Form):
    text_data = forms.CharField(
        max_length=200,
        label='Дані',
        help_text="Введіть посилання на веб-сайт, текстові дані і т. п."
    )


class PDFFileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        cleaned_data = self.clean()
        file = cleaned_data['file']
        if file.name.split('.')[-1] != 'pdf':
            raise forms.ValidationError('Некорректний pdf файл.')
        return file