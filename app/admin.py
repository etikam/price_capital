from django.contrib import admin
from .models import PorteurProject, ProjectCategory, Project, ValidatedProject
from .models import Contact, ProjectType , Realisation
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
    list_display = ('uid','title', 'category', 'goal',  'status', 'created_at')
    list_filter = ('category', 'status')
    search_fields = ('title', 'location')
    readonly_fields = ('progress', 'converted_budget')

    def progress(self, obj):
        return f"{obj.progress:.2f}%"

    def converted_budget(self, obj):
        return f"{obj.converted_budget:.2f} GNF"

    progress.short_description = 'Progression du financement'
    converted_budget.short_description = 'Budget converti (GNF)'
    

@admin.register(ValidatedProject)
class ValidatedProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "category",
        "goal",
        "current_funding",
        "location",
        "currency",
        "is_approved",
        "approved_at",
        "progress",
        "gains"
    )
    list_filter = ("is_approved", "category", "currency", "approved_at")
    search_fields = ("title", "project__title", "category__name", "location")
    readonly_fields = ("created_at", "updated_at", "approved_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Informations générales", {
            "fields": ("project", "title", "category", "context", "summary", "problem_statement")
        }),
        ("Objectifs et Livrables", {
            "fields": ("general_objective", "specific_objectives", "deliverables")
        }),
        ("Détails supplémentaires", {
            "fields": ("target_audience", "key_partners", "additional_details")
        }),
        ("Budget et Localisation", {
            "fields": ("goal", "current_funding", "currency", "location","gains")
        }),
        ("Documents et Images", {
            "fields": ("documents", "image")
        }),
        ("Validation", {
            "fields": ("is_approved", "approved_at", "reformulated_by")
        }),
        ("Audit", {
            "fields": ("created_at", "updated_at")
        }),
    )



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Champs affichés dans la liste des contacts
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    list_filter = ('created_at',)  # Filtres par date de création
    search_fields = ('name', 'email', 'subject', 'message')  # Champs pour la recherche
    ordering = ('-created_at',)  # Tri par défaut (les plus récents en premier)

    # Affichage des détails d'un contact dans l'interface d'administration
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',),  # Cache les informations de date par défaut
        }),
    )
    readonly_fields = ('created_at',)  # Champs en lecture seule


@admin.register(ProjectType)
class AdminProjectType(admin.ModelAdmin):
    list_display = ['name']
    
    
@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    class Meta:
        list_display = "__all__"