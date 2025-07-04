from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from itertools import groupby
from events_manager.forms import EventModelForm
from events_manager.models import Event
from participations.models import Participation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageDraw, ImageFont
import io


class EventsFilteredListView(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = 'grouped_events'
    
    def get_queryset(self):
        url_name = self.request.resolver_match.url_name

        if url_name == 'events_internal':
            events = Event.objects.filter(kind='interno', status='aberto')
            self.template_name = 'events_internal.html'
        
        if url_name == 'events_pending':
            events = Event.objects.filter(kind='interno', status='pendente')
            self.template_name = 'events_pending.html'

        elif url_name == 'events_closed':
            events = Event.objects.filter(status='encerrado')
            self.template_name = 'events_closed.html'
            
        elif url_name == 'my_events':
            self.template_name = 'my_events.html'
            user = self.request.user
            events = Event.objects.filter(status='encerrado', id__in=Participation.objects.filter(user=user, is_present=True).values('event_id'))

        search_title = self.request.GET.get('search_title')
        if search_title:
            events = events.filter(title__contains=search_title)
        
        events = events.order_by('date', 'time')
        
        grouped_events = []
        for (year_month, group) in groupby(events, key=lambda event: event.date.strftime('%Y-%m')):
            grouped_events.append({
                'date': year_month,
                'events': list(group)
            })
        return grouped_events


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        participating_events = Participation.objects.filter(user=self.request.user).values_list('event_id', flat=True)
        context['participating_event_ids'] = participating_events
        
        url_name = self.request.resolver_match.url_name
        context['url_name'] = url_name

        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_template_names(self):
        url_name = self.request.resolver_match.url_name

        if url_name == 'event_qrcode':
            return ['event_qrcode.html']
        if url_name == 'event_material':
            return ['event_material.html']
        if url_name == 'event_certificate':
            return ['event_certificate.html']
        elif url_name == 'event_detail':
            return ['event_detail.html']
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_name = self.request.resolver_match.url_name

        context['is_participating'] = Participation.objects.filter(event=self.object, user=self.request.user).exists()
        context['participation_validated'] = Participation.objects.filter(event=self.object, user=self.request.user, is_present=True).exists()
        context['active_page'] = url_name
        context['site_url'] = settings.SITE_URL
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'event_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'create_page'
        
        url_name = self.request.resolver_match.url_name
        context['url_name'] = url_name
        return context
    
    def get_success_url(self):
        kind = self.object.kind

        if kind == 'externo':
            return reverse_lazy('events_external')
        elif kind == 'interno':
            return reverse_lazy('events_internal')


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'event_update.html'

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'update_page'
        return context

    
class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'delete_page'
        return context
    
    def get_success_url(self):
        origin = self.request.GET.get('origin', '')

        if origin == 'externo':
            return reverse_lazy('events_external')
        elif origin == 'interno':
            return reverse_lazy('events_internal')
        

class EventParticipantsView(LoginRequiredMixin, ListView):
    model = Participation
    template_name = 'event_participants.html'
    context_object_name = 'participants'
        
        
    def get_queryset(self):
        event_id = self.kwargs['pk']
        event = get_object_or_404(Event, id=event_id)
        return Participation.objects.filter(event=event)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event = get_object_or_404(Event, id=self.kwargs['pk'])
        context['active_page'] = 'event_participants'
        context['object'] = get_object_or_404(Event, id=self.kwargs['pk'])
        context['participation_validated'] = Participation.objects.filter(event=event, is_present=True).count()
        context['total_participants'] = Participation.objects.filter(event=event).count()
        return context


@login_required
def render_certificate(request, pk):
    user_name = request.user.first_name + ' ' + request.user.last_name

    template_path = 'media/certificates/Análise_de_Balanço_1.png'

    try:
        image = Image.open(template_path)
        draw = ImageDraw.Draw(image)
        
        center_x = 525
        y = 205
        font_size = 18

        if (len(user_name) > 33 and len(user_name) < 45):
            font_size = 16
        elif(len(user_name) >= 45):
            font_size = 12
            y = 210
        font = ImageFont.truetype('media/fonts/Sora-Medium.ttf', font_size)

        name_text = user_name.upper()

        bbox = draw.textbbox((0, 0), name_text, font=font)
        text_width = bbox[2] - bbox[0]

        position = (center_x - text_width // 2, y)

        draw.text(position, name_text, font=font, fill="white")

        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="certificado_{user_name}.png"'
        return response

    except Exception as e:
        return HttpResponse(f'Erro ao gerar certificado: {e}', status=500)