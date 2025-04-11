from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect   
from django.views import View
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy


class RegisterView(View):

    def get(self, request):
        user_form = CustomUserCreationForm()
        next_url = request.GET.get('next', '')
        return render(request, 'register.html', {'user_form': user_form, 'next': next_url})

    
    def post(self, request):
        user_form = CustomUserCreationForm(request.POST)
        next_url = request.POST.get('next')
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect(next_url)
            
        messages.error(request, "O formulário contém erros. Por favor, corrija os campos destacados.")
        return render(request, 'register.html', {'user_form': user_form, 'next': next_url,})
    
    
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
        return self.get_redirect_url() or reverse_lazy('events_internal')


def logout_view(request):
    logout(request)
    return redirect('events_internal')