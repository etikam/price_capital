from django.contrib import admin
from .models import PorteurProject, ProjectCategory, Project

# Enregistrement du modèle PorteurProject
@admin.register(PorteurProject)
class PorteurProjectAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'adress', 'birthday')
    search_fields = ('first_name', 'last_name', 'phone')

# Enregistrement du modèle ProjectCategory
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Enregistrement du modèle Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'goal', 'current_funding', 'status', 'created_at')
    list_filter = ('category', 'status')
    search_fields = ('title', 'location')
    readonly_fields = ('progress', 'converted_budget')

    def progress(self, obj):
        return f"{obj.progress:.2f}%"

    def converted_budget(self, obj):
        return f"{obj.converted_budget:.2f} GNF"

    progress.short_description = 'Progression du financement'
    converted_budget.short_description = 'Budget converti (GNF)'
