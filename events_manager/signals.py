import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Event
from .utils import generate_short_token, generate_event_qr_code


@receiver(post_save, sender=Event)
def create_envet_qr_code_and_token(sender, instance, **kwargs):
    if not instance.token:
        instance.token = generate_short_token()

    if not instance.qrcode:
        generate_event_qr_code(instance)


@receiver(post_delete, sender=Event)
def delete_qrcode_file(sender, instance, **kwargs):
    if instance.qrcode:
        if os.path.isfile(instance.qrcode.path):
            os.remove(instance.qrcode.path)