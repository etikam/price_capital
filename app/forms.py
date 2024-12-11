from django import forms
from .models import Project
from .models import PorteurProject
from .models import ProjectCategory

class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'goal', 'location', 'currency', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Titre du projet'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Description du projet', 
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'goal': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Budget estimé'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Localisation (Pays où le projet sera réalisé) '
            }),
            'currency': forms.Select(attrs={
                'class': 'form-select', 
                'placeholder': 'Sélectionnez la devise'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }





class PorteurProjectForm(forms.ModelForm):
    class Meta:
        model = PorteurProject
        fields = ['first_name', 'last_name', 'phone', 'adress', 'birthday', 'photo']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
            'adress': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse', 'rows': 4}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
        

class ProjectCategoryForm(forms.ModelForm):
    class Meta:
        model = ProjectCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'})
        }