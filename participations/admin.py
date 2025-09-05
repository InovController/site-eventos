from django.contrib import admin
from participations.models import Participation

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date_joined')
    search_fields = ('event__title', 'user__email')