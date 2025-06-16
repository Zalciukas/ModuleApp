from django.contrib import admin
from .models import Module

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = [
        'subject_name_english', 'user', 's', 'am', 'language', 
        'planned_credits', 'credits_received', 'level_achieved'
    ]
    list_filter = ['language', 'selection_type', 'assessment_form', 'study_part', 'level_achieved']
    search_fields = ['subject_name_english', 'subject_name_lithuanian', 'user__username']
    ordering = ['-s', 'subject_name_english']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)