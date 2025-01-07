from django.apps import AppConfig


class EventsManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events_manager'

    def ready(self):
        # Importa os signals para garantir que sejam registrados
        import events_manager.signals