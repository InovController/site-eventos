from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from .utils import generate_short_token, generate_event_qr_code


@receiver(post_save, sender=Event)
def create_envet_qr_code_and_token(sender, instance, **kwargs):
    if not instance.token:
        instance.token = generate_short_token()

    if not instance.qrcode:
        generate_event_qr_code(instance)