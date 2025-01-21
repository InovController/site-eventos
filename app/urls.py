"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from events_manager.views import (EventsFilteredListView,
EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, 
EventParticipantsView)
from accounts.views import RegisterView, CustomLoginView, logout_view
from participations.views import validate_presence, subscribe_event, unsubscribe_event
from evaluation.views import EvaluationView, evaluation_dashboard
from departaments.views import DepartamentsListView, DepartamentsCreateView, DepartamentsUpdateView, DepartamentsDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', EventsFilteredListView.as_view(), name='events_internal'),
    path('eventos/internos', EventsFilteredListView.as_view(), name='events_internal'),
    path('eventos/externos', EventsFilteredListView.as_view(), name='events_external'),
    path('eventos/encerrados', EventsFilteredListView.as_view(), name='events_closed'),
    path('evento/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('evento/<int:pk>/detalhes/', EventDetailView.as_view(), name='event_detail'),
    path('evento/<int:pk>/qrcode/', EventDetailView.as_view(), name='event_qrcode'),
    path('evento/<int:pk>/material/', EventDetailView.as_view(), name='event_material'),
    path('evento/<int:pk>/avaliacao/', EvaluationView.as_view(), name='evaluation_form'),
    path('evento/<int:pk>/certificado/', EventDetailView.as_view(), name='event_certificate'),
    path('evento/<int:pk>/dashboard/', evaluation_dashboard, name='evaluation_dashboard'),

    path('evento/<int:pk>/inscrever/', subscribe_event, name='subscribe_event'),
    path('evento/<int:pk>/sair/', unsubscribe_event, name='unsubscribe_event'),
    path('evento/<int:pk>/validar/<str:token>', validate_presence, name='validate'),
    path('validar/<str:token>', validate_presence, name='short_validate'),
    
    path('evento/novo', EventCreateView.as_view(), name='event_create'),
    path('evento/<int:pk>/editar', EventUpdateView.as_view(), name='event_update'),
    path('evento/<int:pk>/apagar', EventDeleteView.as_view(), name='event_delete'),
    path('evento/<int:pk>/participantes', EventParticipantsView.as_view(), name='event_participants'),

    path('departamento/', DepartamentsListView.as_view(), name='list'),
    path('departamento/criar/', DepartamentsCreateView.as_view(), name='create'),
    path('departamento/<int:pk>/editar/', DepartamentsUpdateView.as_view(), name='update'),
    path('departamento/<int:pk>/deletar/', DepartamentsDeleteView.as_view(), name='delete'),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
