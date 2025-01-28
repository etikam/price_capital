from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import MoralPerson, PhysicalPerson, User
from .utils.mailing import send_activation_email


class CustomAuthenticationForm(forms.Form):
    # Remplacer 'username' par 'email' pour correspondre à votre modèle
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Entrez votre email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Entrez votre mot de passe",
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requis. Entrez une adresse email valide.")

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email existe deja.")
        return email


class PhysicalPersonForm(forms.ModelForm):
    class Meta:
        model = PhysicalPerson
        fields = ["first_name", "last_name", "telephone", "adresse", "birthday", "id_card", "photo"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "adresse": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "birthday": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "id_card": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        if not telephone.isdigit():
            raise ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
        if len(telephone) < 8 or len(telephone) > 15:
            raise ValidationError("Le numéro de téléphone doit contenir entre 8 et 15 chiffres.")
        return telephone


class MoralPersonForm(forms.ModelForm):
    class Meta:
        model = MoralPerson
        fields = ["company_name", "telephone", "adresse", "rccm", "logo"]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "adresse": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "rccm": forms.TextInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_rccm(self):
        rccm = self.cleaned_data.get("rccm")
        if len(rccm) < 5:
            raise ValidationError("Le RCCM doit contenir au moins 5 caractères.")
        return rccm


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
