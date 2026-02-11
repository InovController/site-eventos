from django.contrib import admin
from .models import (
    Evaluation, EvaluationResponse,
    EvaluationTheme, EvaluationQuestion,
    EvaluationTemplate,
)

class EvaluationResponseInline(admin.TabularInline):
    model = EvaluationResponse
    extra = 0
    can_delete = True

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "date_submitted", "is_complete")
    search_fields = ("user__email", "event__title")
    inlines = [EvaluationResponseInline]
    readonly_fields = ("date_submitted",)

@admin.register(EvaluationTheme)
class EvaluationThemeAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(EvaluationTemplate)
class EvaluationTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)

@admin.register(EvaluationQuestion)
class EvaluationQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "question_type", "template", "theme")
    search_fields = ("question_text", "template__name", "theme__name")
    list_filter = ("template", "theme", "question_type")
