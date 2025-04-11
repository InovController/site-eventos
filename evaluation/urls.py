from django.urls import path
from .views import EvaluationView, evaluation_dashboard

urlpatterns = [
    path('evento/<int:pk>/dashboard/', evaluation_dashboard, name='evaluation_dashboard'),
    path('evento/<int:pk>/avaliacao/', EvaluationView.as_view(), name='evaluation_form'),
]