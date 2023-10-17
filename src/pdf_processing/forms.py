from django import forms


class PDFFileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        cleaned_data = self.clean()
        file = cleaned_data['file']
        if file.name.split('.')[-1] != 'pdf':
            raise forms.ValidationError('Некорректний pdf файл.')
        return file