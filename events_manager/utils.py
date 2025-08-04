import secrets
import string
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.core.files import File
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont


def generate_short_token(length=6):
    """
    Gera um slug alfanumérico único de tamanho especificado.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_event_qr_code(event):
    qr_data = f"{settings.SITE_URL}/validar/{event.token}"
    
    # Generate QR code
    qr_img = qrcode.make(qr_data)
    qr_io = BytesIO()
    qr_img.save(qr_io, 'PNG')
    qr_io.seek(0)

    # Save to the ImageField of the event
    event.qrcode.save(f'qrcode_{event.id}.png', File(qr_io))


def generate_certificate_response(user, event, for_download=False):
    user_name = f"{user.first_name} {user.last_name}"
    certificate_path = event.certificate.url.lstrip('/')

    image = Image.open(certificate_path)
    draw = ImageDraw.Draw(image)

    center_x = 525
    y = 205
    font_size = 18

    if 33 < len(user_name) < 45:
        font_size = 16
    elif len(user_name) >= 45:
        font_size = 12
        y = 210

    font = ImageFont.truetype('media/fonts/Sora-Medium.ttf', font_size)
    name_text = user_name.upper()

    bbox = draw.textbbox((0, 0), name_text, font=font)
    text_width = bbox[2] - bbox[0]
    position = (center_x - text_width // 2, y)

    draw.text(position, name_text, font=font, fill="white")

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='image/png')
    if for_download:
        response['Content-Disposition'] = f'attachment; filename="certificate_{user_name}.png"'

    return response