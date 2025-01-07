from django.contrib import admin
from .models import Evaluation, EvaluationResponse, EvaluationTheme, EvaluationQuestion


class EvaluationResponseInline(admin.TabularInline):
    model = EvaluationResponse
    extra = 1
    can_delete = True  # Habilita a exclusão de registros inline


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date_submitted', 'is_complete')  # Campos que serão mostrados na lista
    search_fields = ('user__email', 'event__title')  # Campos de pesquisa
    inlines = [EvaluationResponseInline]  # Mostra respostas da avaliação embutidas
    readonly_fields = ('date_submitted',)

    class Meta:
        model = Evaluation


class EvaluationThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EvaluationQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'theme__name')
    search_fields = ('theme__name',)
    

admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(EvaluationTheme, EvaluationThemeAdmin)
admin.site.register(EvaluationQuestion, EvaluationQuestionAdmin)