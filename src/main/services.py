# def image_to_base64(image, image_format):
#     import base64
#     from io import BytesIO
#     buffered = BytesIO()
#     image.save(buffered, format=image_format.upper())
#     return base64.b64encode(buffered.getvalue()).decode("utf-8")
#
#
# def set_color_tone_image(image, color_tone):
#     from PIL import Image
#     img = image.convert("RGB")
#     red, green, blue = img.split()
#     colors_tone = {
#         'red': red,
#         'green': green,
#         'blue': blue
#     }
#     if color_tone == 'default':
#         return Image.merge("RGB", (red, green, blue))
#     zeroed_band = red.point(lambda _: 0)
#     return Image.merge("RGB", tuple(colors_tone[k] if k == color_tone else zeroed_band for k in colors_tone))
#
#
# def generate_qrcode(data):
#     import qrcode
#     qr = qrcode.QRCode()
#     qr.add_data(data)
#     qr.make()
#     return qr.make_image(fill_color="black", back_color="white")
import tempfile
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from unidecode import unidecode


def extract_text_from_pdf(file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pagenos = set()

    for page in PDFPage.get_pages(file, pagenos):
        interpreter.process_page(page)

    text = retstr.getvalue()
    file.close()
    device.close()
    retstr.close()

    return text

