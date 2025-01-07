from django import forms
from events_manager.models import Event


class EventModelForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'