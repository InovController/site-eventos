from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from evaluation.models import Evaluation, EvaluationQuestion, EvaluationResponse, EvaluationTheme
from events_manager.models import Event
from participations.models import Participation
from django.db.models import Avg, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class EvaluationView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, id=pk)
        
        evaluation = Evaluation.objects.filter(user=request.user, event=event).first()
        evaluation_complete = evaluation.is_complete if evaluation else False
        
        participation_validated = Participation.objects.filter(event=event, user=request.user, is_present=True).exists()

        themes = EvaluationTheme.objects.all()
        questions_by_theme = {}
        
        for theme in themes:
            questions_by_theme[theme] = EvaluationQuestion.objects.filter(theme=theme)

        total_pages = 1 + themes.count()

        return render(request, 'evaluation_form.html', {
            'object': event,
            'evaluation': evaluation,
            'questions_by_theme': questions_by_theme,
            'total_pages': total_pages,
            'active_page': 'evaluation_form',
            'evaluation_complete': evaluation_complete,
            'participation_validated': participation_validated
        })
    
    
    def post(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, id=pk)

        if event.status != 'encerrado':
            return render(request, 'evaluation_form.html', {
                'object': event,
                'error_message': 'O evento ainda não foi encerrado. Você só pode avaliar após o encerramento.',
            })
        
        evaluation, created = Evaluation.objects.get_or_create(
            user=request.user,
            event=event
        )
        
        if evaluation.is_complete:
            return redirect('event_detail', pk=event.id)
        
        questions = EvaluationQuestion.objects.all()
        for question in questions:
            answer_key = f'question_{question.id}'

            if answer_key in request.POST:
                answer_value = request.POST[answer_key]

                if question.question_type == 'multiple_choice':
                    answer = int(answer_value)
                    EvaluationResponse.objects.create(
                        evaluation=evaluation,
                        question=question,
                        answer=answer
                    )
                
                elif question.question_type == 'open_text':
                    answer = str(answer_value)
                    EvaluationResponse.objects.create(
                        evaluation=evaluation,
                        question=question,
                        answer_text=answer
                    )

        evaluation.is_complete = True
        evaluation.save()

        return redirect('evaluation_form', pk=pk)
    

@method_decorator(login_required, name='dispatch')
def evaluation_dashboard(request, pk):
    event = Event.objects.get(id=pk)

    themes = EvaluationTheme.objects.all()
    
    numeric_questions_by_theme = {}
    text_questions_by_theme = {}

    for theme in themes:
        questions = EvaluationQuestion.objects.filter(theme=theme)
        numeric_theme_data = []
        text_theme_data = []
        
        for question in questions:
            numeric_responses = EvaluationResponse.objects.filter(
                evaluation__event=event,
                question=question,
                answer__isnull=False
            )

            distribution = numeric_responses.values('answer').annotate(count=Count('answer')).order_by('answer')
            response_distribution = {i: 0 for i in range(1, 6)}
            for item in distribution:
                response_distribution[item['answer']] = item['count']

            if numeric_responses.exists():
                avg_score = numeric_responses.aggregate(Avg('answer'))['answer__avg']
                numeric_theme_data.append({
                    'question_text': question.question_text,
                    'avg_score': round(avg_score, 2),
                    'distribution': response_distribution
                })

            text_responses = EvaluationResponse.objects.filter(
                evaluation__event=event,
                question=question,
                answer__isnull=True,
                answer_text__isnull=False
            )

            if text_responses.exists():
                answers = [response.answer_text for response in text_responses]
                text_theme_data.append({
                    'question_text': question.question_text,
                    'answers': answers
                })

        if numeric_theme_data:
            numeric_questions_by_theme[theme.name] = numeric_theme_data
        
        if text_theme_data:
            text_questions_by_theme[theme.name] = text_theme_data

    return render(request, 'evaluation_dashboard.html', {
        'object': event,
        'text_questions_by_theme': text_questions_by_theme,
        'numeric_questions_by_theme': numeric_questions_by_theme,
        'active_page': request.resolver_match.url_name
    })