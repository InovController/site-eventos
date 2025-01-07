from django.db import models
from events_manager.models import Event


class Material(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participations')