from django.urls import path
from .views import DepartamentsListView, DepartamentsCreateView, DepartamentsUpdateView, DepartamentsDeleteView

urlpatterns = [
    path('departamento/', DepartamentsListView.as_view(), name='list'),
    path('departamento/criar/', DepartamentsCreateView.as_view(), name='create'),
    path('departamento/<int:pk>/editar/', DepartamentsUpdateView.as_view(), name='update'),
    path('departamento/<int:pk>/deletar/', DepartamentsDeleteView.as_view(), name='delete')
]