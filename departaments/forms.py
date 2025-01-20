from django import forms
from departaments.models import Departament


class DepartamentModelForm(forms.ModelForm):

    class Meta:
        model = Departament
        fields = '__all__'