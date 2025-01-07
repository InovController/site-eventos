from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    company = forms.CharField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'company', 'phone', 'password1', 'password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.company = self.cleaned_data['company']
        user.phone = self.cleaned_data['phone']
        user.username = user.email
        if commit:
            user.save()
        return user
    
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")