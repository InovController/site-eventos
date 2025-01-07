from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect   
from django.views import View
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy


class RegisterView(View):

    def get(self, request):
        user_form = CustomUserCreationForm()
        url_name = request.resolver_match.url_name
        return render(request, 'register.html', {'user_form': user_form, 'url_name': url_name})

    
    def post(self, request):
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()

            funcionario_group = Group.objects.get(name='Funcionário')
            funcionario_group.user_set.add(user)
            return redirect('login')
            
        url_name = request.resolver_match.url_name
        return render(request, 'register.html', {'user_form': user_form, 'url_name': url_name})
    
    
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_name = self.request.resolver_match.url_name
        context['url_name'] = url_name
        return context
    

    def get_success_url(self):
        return reverse_lazy('events_external')


def logout_view(request):
    logout(request)
    return redirect('events_external')