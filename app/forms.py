from django import forms
from .models import Project
from .models import PorteurProject
from .models import ProjectCategory
from .models import ValidatedProject
from .models import Contact
from django.core.validators import FileExtensionValidator
from .models import ProductInfo
from .models import ValidatedProductInfo
from django.core.validators import MinValueValidator


class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "project_type",
            "goal",
            "location",
            "currency",
            "image",
            "presentation_document",
            "business_plan",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Titre du projet"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description du projet",
                    "rows": 4,
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "project_type": forms.Select(attrs={"class": "form-select"}),
            "goal": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Budget estimé"}
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Localisation (Pays où le projet sera réalisé) ",
                }
            ),
            "currency": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "presentation_document": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.docx,.ppt,.pptx",
                    "placeholder": "Télécharger le document de présentation",
                }
            ),
            "business_plan": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.docx,.ppt,.pptx",
                    "placeholder": "Télécharger le Business Plan",
                }
            ),
        }


class PorteurProjectForm(forms.ModelForm):
    class Meta:
        model = PorteurProject
        fields = ["first_name", "last_name", "phone", "adress", "birthday", "photo"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Prénom"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nom"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Numéro de téléphone"}
            ),
            "adress": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Adresse", "rows": 4}
            ),
            "birthday": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }


class ProjectCategoryForm(forms.ModelForm):
    class Meta:
        model = ProjectCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nom de la catégorie"}
            )
        }


class ValidatedProjectForm(forms.ModelForm):
    class Meta:
        model = ValidatedProject
        fields = [
            "title",
            "category",
            "goal",      
            "location",
            "currency",
            "context",
            "summary",
            "problem_statement",
            "general_objective",
            "specific_objectives",
            "deliverables",
            "target_audience",
            "key_partners",
            "image",
            "additional_details",
            "documents",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "goal": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Budget estimé"}
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Localisation (Pays où le projet sera réalisé) ",
                }
            ),
            "currency": forms.Select(attrs={"class": "form-select"}),
            "context": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "summary": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "problem_statement": forms.Textarea(
                attrs={"rows": 4, "class": "form-control"}
            ),
            "general_objective": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
            "specific_objectives": forms.Textarea(
                attrs={"rows": 4, "class": "form-control"}
            ),
            "deliverables": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "target_audience": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
            "key_partners": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "additional_details": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Votre Nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Votre Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Téléphone'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Sujet'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Votre message ici',
                'style': 'height: 160px;'
            }),
        }


class ProductInfoForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = [
            'product_name',
            'product_description',
            'delivery_date',
            'quantity_available',
            "product_unity",
            'unit_price',
            'media',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom du produit',
            }),
            
            'product_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le produit ou service.',
            }),
            'delivery_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'quantity_available': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Quantité disponible',
            }),
            
            'product_unity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex:kilo,litre,bidon,sac...',
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prix unitaire',
            }),
            'media': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'product_name': 'Nom du produit',
            'product_description': 'Description',
            'delivery_date': 'Date de livraison',
            'quantity_available': 'Quantité disponible',
            'quantity_unity': 'Unite de mesure',
            'unit_price': 'Prix unitaire',
            'media': 'Image du produit',
        }

class ValidatedProductInfoForm(forms.ModelForm):
    class Meta:
        model = ValidatedProductInfo
        fields = [
            'product_name',
            'product_description',
            'delivery_date',
            'order_status',
            'order_progress',
            'quantity_available',
            'product_unity',
            'unit_price',
            'media',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom du produit',
            }),
            'product_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le produit ou service',
            }),
            'delivery_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'order_status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'order_progress': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'placeholder': 'Progression en pourcentage',
            }),
            'quantity_available': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Quantité disponible',
            }),
            'product_unity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unité de mesure (ex: kg, pièces)',
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Prix unitaire',
            }),
            'media': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'product_name': 'Nom du Produit',
            'product_description': 'Description du Produit',
            'delivery_date': 'Date de Livraison',
            'order_status': 'Statut de la Commande',
            'order_progress': 'Progression de la Commande (%)',
            'quantity_available': 'Quantité Disponible',
            'product_unity': 'Unité de Mesure',
            'unit_price': 'Prix Unitaire',
            'media': 'Image du Produit',
        }
