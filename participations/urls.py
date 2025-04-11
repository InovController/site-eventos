from django.urls import path
from participations.views import validate_presence, subscribe_event, unsubscribe_event, export_participants_excel, export_participants_pdf

urlpatterns = [
    path('evento/<int:pk>/inscrever/', subscribe_event, name='subscribe_event'),
    path('evento/<int:pk>/sair/', unsubscribe_event, name='unsubscribe_event'),
    path('event/<int:event_id>/export_excel/', export_participants_excel, name='export_participants_excel'),
    path('event/<int:event_id>/export_pdf/', export_participants_pdf, name='export_participants_pdf'),

    path('evento/<int:pk>/validar/<str:token>', validate_presence, name='validate'),
    path('validar/<str:token>', validate_presence, name='short_validate'),
]