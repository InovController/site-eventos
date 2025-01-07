from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Participation
from events_manager.models import Event


@login_required(login_url='login')
def subscribe_event(request, pk):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=pk)
        Participation.objects.create(event=event, user=request.user, signed_up=True)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required(login_url='login')
def unsubscribe_event(request, pk):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=pk)
        Participation.objects.filter(event=event, user=request.user).delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required(login_url='login')
def validate_presence(request, token):
    event = get_object_or_404(Event, token=token)
    
    if event.status == 'encerrado':
        return render(request, 'no_validate_participation.html', {
            'object': event,
            'message': 'Desculpe, este evento já foi encerrado.',
        })
        

    participation, created = Participation.objects.get_or_create(event=event, user=request.user)

    if participation.is_present:
        return render(request, 'validate_participation.html', {
            'object': event,
            'message': 'Você já registrou sua presença.',  # Adiciona uma mensagem informativa
            'participation': participation,
        })

    participation.is_present = True
    participation.save()

    return render(request, 'validate_participation.html', {
        'object': event,
        'message': 'Sua presença foi registrada com sucesso!',  # Mensagem de sucesso
        'participation': participation,
    })
