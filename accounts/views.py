from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect   
from django.views import View
from users.forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(View):

    def get(self, request):
        user_form = CustomUserCreationForm()
        url_name = request.resolver_match.url_name
        return render(request, 'register.html', {'user_form': user_form, 'url_name': url_name})

    
    def post(self, request):
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()

            messages.success(request, "Cadastro realizado com sucesso! Você já pode fazer login.")
            return redirect('login')
            
        messages.error(request, "O formulário contém erros. Por favor, corrija os campos destacados.")
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


def logout_view(request):
    logout(request)
    return redirect('events_internal')