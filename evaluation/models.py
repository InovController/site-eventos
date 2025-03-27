from django.db import models
from django.conf import settings
from events_manager.models import Event
from django.core.exceptions import ValidationError


class EvaluationTheme(models.Model):
    name = models.CharField(max_length=255)  # Nome do tema (e.g., "Conteúdo / Programa")

    def __str__(self):
        return self.name


class EvaluationQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Múltipla Escolha (1-5)'),
        ('open_text', 'Resposta Aberta'),
    ]
    theme = models.ForeignKey(EvaluationTheme, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='multiple_choice')
    
    def __str__(self):
        return self.question_text


class Evaluation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'event'], name='unique_user_event')
        ]


class EvaluationResponse(models.Model):
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    question = models.ForeignKey(EvaluationQuestion, on_delete=models.CASCADE)
    answer = models.IntegerField(choices=SCORE_CHOICES, null=True, blank=True)
    answer_text = models.TextField(blank=True, null=True)

    def clean(self):
        if self.question.question_type == 'multiple_choice' and self.answer_text:
            raise ValidationError('Para perguntas numéricas, o campo de resposta textual deve estar vazio.')
        if self.question.question_type == 'open_text' and self.answer:
            raise ValidationError('Para perguntas textuais, o campo de resposta numérica deve estar vazio.')

        if self.question.question_type == 'multiple_choice' and not self.answer:
            raise ValidationError('Uma resposta numérica deve ser fornecida para perguntas numéricas.')
        if self.question.question_type == 'open_text' and not self.answer_text:
            raise ValidationError('Uma resposta textual deve ser fornecida para perguntas textuais.')

    def __str__(self):
        return f"Response to {self.question.question_text}"