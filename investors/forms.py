from django import forms
from investors.models import Investor
from investors.models import Investissement

from django.core.exceptions import ValidationError

class InvestorForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address',
            'available_budget', 'preferred_sectors', 'preferred_currency',
            'minimum_investment', 'maximum_investment', 'investment_type',
            'expertise_domain', 'investment_experience'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse postale', 'rows': 3}),
            'available_budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Budget disponible'}),
            'preferred_sectors': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'preferred_currency': forms.Select(attrs={'class': 'form-select'}),
            'minimum_investment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant minimal'}),
            'maximum_investment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant maximal'}),
            'investment_type': forms.Select(attrs={'class': 'form-select'}),
            'expertise_domain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domaine d\'expertise'}),
            'investment_experience': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        minimum_investment = cleaned_data.get('minimum_investment')
        maximum_investment = cleaned_data.get('maximum_investment')

        if minimum_investment and maximum_investment and minimum_investment > maximum_investment:
            raise ValidationError({
                'minimum_investment': "Le montant minimal doit être inférieur ou égal au montant maximal."
            })

        return cleaned_data
    
    
    

class InvestissementForm(forms.ModelForm):
    class Meta:
        model = Investissement
        fields = ['investor', 'project', 'anonymity', 'amount', 'currency']
        widgets = {
            'investor': forms.HiddenInput(),
            'project': forms.HiddenInput(),
            'anonymity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
           
        }
