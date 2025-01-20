from django.contrib import admin
from events_manager.models import EventGroup, Event


class EventInline(admin.TabularInline):
    model = Event
    extra = 1
    fields = ['title', 'location', 'date', 'time', 'duration', 'kind', 'status', 'description', 'photo']
    show_change_link = True  # Permite acessar o link de edição do evento


@admin.register(EventGroup)
class EventGroupAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    list_display = ['title', 'start_date', 'end_date', 'description']
    search_fields = ['title', 'description']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'date', 'location')
    search_fields = ('title',)
    readonly_fields = ('qrcode', 'token')