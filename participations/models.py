from django.db import models
from django.conf import settings
from events_manager.models import Event
    

class Participation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participations')
    signed_up = models.BooleanField(default=False)
    is_present = models.BooleanField(default=False)  # Presença começa como False
    date_joined = models.DateTimeField(blank=True, null=True)  # Somente será preenchido quando a presença for True

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']