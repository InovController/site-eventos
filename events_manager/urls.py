from django.urls import path
from .views import (EventsFilteredListView,
EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, 
EventParticipantsView, view_certificate, download_certificate)

urlpatterns = [
    path('', EventsFilteredListView.as_view(), name='events_internal'),
    path('eventos/internos', EventsFilteredListView.as_view(), name='events_internal'),
    path('eventos/pendentes', EventsFilteredListView.as_view(), name='events_pending'),
    path('eventos/encerrados', EventsFilteredListView.as_view(), name='events_closed'),
    path('eventos_participados', EventsFilteredListView.as_view(), name='my_events'),
    path('evento/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('evento/<int:pk>/detalhes/', EventDetailView.as_view(), name='event_detail'),
    path('evento/<int:pk>/qrcode/', EventDetailView.as_view(), name='event_qrcode'),
    path('evento/<int:pk>/material/', EventDetailView.as_view(), name='event_material'),
    path('evento/<int:pk>/certificado/', EventDetailView.as_view(), name='event_certificate'),
    path('evento/novo', EventCreateView.as_view(), name='event_create'),
    path('evento/<int:pk>/editar', EventUpdateView.as_view(), name='event_update'),
    path('evento/<int:pk>/apagar', EventDeleteView.as_view(), name='event_delete'),
    path('evento/<int:pk>/participantes', EventParticipantsView.as_view(), name='event_participants'),
    path('certificado/visualizar/<int:pk>/',  view_certificate, name='view_certificate'),
    path('certificado/download/<int:pk>/', download_certificate, name='download_certificate'),
]