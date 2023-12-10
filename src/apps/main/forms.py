from django import forms


class QrCodeForm(forms.Form):
    text_data = forms.CharField(
        max_length=200,
        label='Дані',
        help_text="Введіть посилання на веб-сайт, текстові дані і т. п."
    )
