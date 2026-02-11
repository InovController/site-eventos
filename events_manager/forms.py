from django import forms
from events_manager.models import Event
from evaluation.models import EvaluationTemplate


class EventModelForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Só templates ativos no dropdown
        if "evaluation_template" in self.fields:
            self.fields["evaluation_template"].queryset = EvaluationTemplate.objects.filter(is_active=True)
            self.fields["evaluation_template"].required = False
            self.fields["evaluation_template"].empty_label = "Sem avaliação"