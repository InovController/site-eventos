from django.contrib import admin
from departaments.models import Departament

    

@admin.register(Departament)
class EventDepartamentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)