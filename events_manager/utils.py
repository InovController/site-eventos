import secrets
import string
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings


def generate_short_token(length=6):
    """
    Gera um slug alfanumérico único de tamanho especificado.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_event_qr_code(event):
    qr_data = f"{settings.SITE_URL}/validar/{event.token}/"
    
    # Generate QR code
    qr_img = qrcode.make(qr_data)
    qr_io = BytesIO()
    qr_img.save(qr_io, 'PNG')
    qr_io.seek(0)

    # Save to the ImageField of the event
    event.qrcode.save(f'qrcode_{event.id}.png', File(qr_io))