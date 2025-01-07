from django import forms
from django.forms import modelformset_factory
from evaluation.models import EvaluationResponse


class EvaluationResponseForm(forms.ModelForm):
    class Meta:
        model = EvaluationResponse
        fields = ['answer', 'answer_text']

EvaluationFormSet = modelformset_factory(
    EvaluationResponse,
    form=EvaluationResponseForm,
    extra=0,
    can_delete=False
)
