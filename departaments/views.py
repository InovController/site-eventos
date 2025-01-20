from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from departaments.models import Departament
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from departaments.forms import DepartamentModelForm


@method_decorator(login_required, name='dispatch')
class DepartamentsListView(ListView):
    model = Departament
    template_name = 'departaments_list.html'
    context_object_name = 'departaments'


class DepartamentsCreateView(CreateView):
    model = Departament
    form_class = DepartamentModelForm
    template_name = 'departaments_create.html'

class DepartamentsUpdateView(UpdateView):
    model = Departament
    template_name = 'departaments_update.html'

class DepartamentsDeleteView(DeleteView):
    model = Departament
    template_name = 'departaments_delete.html'