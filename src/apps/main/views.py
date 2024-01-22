from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'home.html'

# class QrCodeGenerationView(FormView):
#     template_name = 'qrcode.html'
#     form_class = QrCodeForm
#
#     def form_valid(self, form):
#         qrcode = services.generate_qrcode(form.cleaned_data['text_data'])
#         return self.render_to_response(self.get_context_data(qrcode=services.image_to_base64(qrcode, 'JPEG')))
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['qrcode'] = kwargs.get('qrcode')
#         return context
