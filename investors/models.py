import random
import string
import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from app.models import ProjectCategory
from app.models import ValidatedProject, ValidatedProductInfo
from django.db.models import Sum

class Investor(models.Model):
    def generate_investor_id():
        """
        Génère un identifiant unique de 6 caractères (4 lettres et 2 chiffres).
        Vérifie que l'ID généré n'existe pas déjà dans la base de données.
        """
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=4))
            digits = ''.join(random.choices(string.digits, k=2))
            investor_id = f"{letters}{digits}"
            if not Investor.objects.filter(investor_id=investor_id).exists():
                return investor_id

    # Identifiant unique de l'investisseur
    investor_id = models.CharField(
        max_length=6,
        unique=True,
        default=generate_investor_id,
        verbose_name="Identifiant Investisseur"
    )

    # Association avec un utilisateur existant
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investor",
        verbose_name="Utilisateur"
    )

    # Identité de l'investisseur
    first_name = models.CharField(max_length=255, verbose_name="Prénom")
    last_name = models.CharField(max_length=255, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email", help_text="Adresse email de l'investisseur")
    phone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    address = models.TextField(verbose_name="Adresse postale")
    
    # Informations financières
    available_budget = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="Budget disponible", 
        help_text="Montant que l'investisseur est prêt à investir (ex. 10,000 GNF)"
    )
    
    # Préférences d'investissement
    preferred_sectors = models.ManyToManyField(
        ProjectCategory,
        blank=True,
        related_name="interested_investors",
        verbose_name="Secteurs d'intérêt"
    )

    preferred_currency = models.CharField(
        max_length=3,
        choices=[
            ("GNF", "GNF - Franc guinéen"),
            ("USD", "USD - Dollar américain"),
            ("EUR", "EUR - Euro"),
        ],
        default="GNF",
        verbose_name="Monnaie préférée"
    )
    
    minimum_investment = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0,
        verbose_name="Montant minimal d'investissement",
        help_text="Seuil minimum que l'investisseur est prêt à investir"
    )
    
    maximum_investment = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0,
        verbose_name="Montant maximal d'investissement",
        help_text="Seuil maximum que l'investisseur est prêt à investir"
    )
    
    investment_type = models.CharField(
        max_length=50,
        choices=[
            ("short_term", "Projets à court terme"),
            ("long_term", "Projets à long terme"),
            ("innovation", "Innovation et technologie"),
        ],
        default="long_term",
        verbose_name="Type de projets recherchés"
    )

    # Informations supplémentaires
    expertise_domain = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Domaine d'expertise",
        help_text="Domaine professionnel ou secteur de l'investisseur"
    )
    
    investment_experience = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Débutant"),
            ("intermediate", "Intermédiaire"),
            ("expert", "Expert"),
        ],
        default="beginner",
        verbose_name="Expérience en investissement"
    )

    # Champs automatiques
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return f"{self.investor_id} - {self.full_name}"

    @property
    def full_name(self):
        """Retourne le nom complet de l'investisseur."""
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        """Validation personnalisée pour s'assurer que le montant minimal est inférieur ou égal au montant maximal."""
        if self.minimum_investment > self.maximum_investment:
            raise ValidationError({
                'minimum_investment': "Le montant minimal doit être inférieur ou égal au montant maximal."
            })

    def is_active(self):
        """Vérifie si l'investisseur est actif (budget disponible > 0)."""
        return self.available_budget > 0

    class Meta:
        verbose_name = "Investisseur"
        verbose_name_plural = "Investisseurs"


class Investissement(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Identifiant unique"
        )
        
    # Lien avec l'investisseur
    investor = models.ForeignKey(
        Investor,
        on_delete=models.CASCADE,
        related_name="investissements",
        verbose_name="Investisseur"
    )

    # Lien avec le projet (si applicable)
    project = models.ForeignKey(
        ValidatedProject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="investissements",
        verbose_name="Projet à investir"
    )

    anonymity = models.BooleanField(default=False, 
                                    help_text="Si vous ne voulez pas être vu par le porteur de projet (s'applique pour les projets de type Don)",
                                    verbose_name="Je Veux Rester Anonyme"
                                    )
    # Montant de l'investissement
    amount = models.DecimalField(
        default = 0,
        max_digits=15,
        decimal_places=2,
        verbose_name="Montant à Investir",
        help_text="Montant que vous voulez investir (ex. 10,000 GNF)"
    )

    currency = models.CharField(
        max_length=3,
        choices=[
            ("GNF", "GNF - Franc guinéen"),
            ("USD", "USD - Dollar américain"),
            ("EUR", "EUR - Euro"),
        ],
        default="GNF",
        verbose_name="Devise D'investissement",
        help_text="Dans quelle devise est votre montant"
    )


     # Niveau d'avancement (en pourcentage)
    progress = models.IntegerField(
        choices=[
            (0, "Initié"),
            (50,"Payment en cours"),
            (100, "Terminé"),
        ],
        default=0,
        verbose_name="Progression"
    )
    
    payment_done = models.BooleanField(default=False) #pour savoir si le payement est efectué ou pas

    # Champs automatiques
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    @property
    def percentage_on_goal(self):
        """
        Calcule le pourcentage que cet investissement représente par rapport au goal du projet.
        Si le projet n'a pas de goal ou n'est pas défini, retourne 0.
        """
        if self.project and self.project.goal:
            return (self.amount / self.project.goal) * 100
        return 0

    @property
    def gains(self):
        """
        Calculer les gains totaux pour cet investissement en fonction des enregistrements de gains du projet.
        """
        if self.percentage_on_goal:
            total_project_gains = self.project.gain_records.aggregate(total_gains=Sum('amount'))['total_gains'] or 0
            return total_project_gains * (self.percentage_on_goal / 100)
        return 0

    def __str__(self):
        return f"Investissement #{self.id} - {self.investor.full_name} - {self.amount} {self.currency}"

    class Meta:
        verbose_name = "Investissement"
        verbose_name_plural = "Investissements"
        unique_together = (('project', 'investor'),)
        

class Achat(models.Model):
    STATUS_CHOICES = [
        (1, 'Commande validée'),
        (2, 'En cours de production'),
        (3, 'Livraison'),
        (4, 'Terminé')
    ]

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Identifiant unique"
    )

    # Lien avec l'acheteur
    buyer = models.ForeignKey(
        Investor,
        on_delete=models.CASCADE,
        related_name="achats",
        verbose_name="Acheteur"
    )

    # Lien avec le produit
    product = models.ForeignKey(
        ValidatedProductInfo,
        on_delete=models.CASCADE,
        related_name="achats",
        verbose_name="Produit"
    )

    # Quantité achetée
    quantity = models.PositiveIntegerField(
        verbose_name="Quantité",
        help_text="Quantité que vous souhaitez acheter",
        default=1
    )

    # Montant total
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Montant total",
        help_text="Montant total de l'achat"
    )

    # Statut de la commande
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    progress = models.IntegerField(default=0)

    currency = models.CharField(
        max_length=3,
        choices=[
            ("GNF", "GNF - Franc Guinéen"),
            ("USD", "USD - Dollar Américain"),
            ("EUR", "EUR - Euro"),
        ],
        default="GNF",
        verbose_name="Devise",
        help_text="Dans quelle devise est votre montant"
    )

    # Champs automatiques
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    estimated_delivery_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Achat de {self.product.product_name} par {self.buyer.email}"

    def get_progress_display(self):
        """Retourne une description lisible et descriptive du progrès"""
        progress_text = {
            1: "Commande validée",
            2: "En production",
            3: "Livraison",
            4: "Terminé"
        }
        return progress_text.get(self.order_status, "Statut inconnu")

    def save(self, *args, **kwargs):
        # Calculer le montant total
        if not self.total_amount:
            self.total_amount = self.quantity * self.product.unit_price
        
        # Mettre à jour le progress en fonction du order_status
        if self.order_status == 1:  # Production
            self.progress = 25
        elif self.order_status == 2:  # Contrôle
            self.progress = 50
        elif self.order_status == 3:  # Livraison
            self.progress = 75
        elif self.order_status == 4:  # Terminé
            self.progress = 100
            
        super().save(*args, **kwargs)

    def get_status_color(self):
        """Retourne la couleur Bootstrap en fonction du statut"""
        status_colors = {
            1: 'info',      # Production - Bleu
            2: 'warning',   # Contrôle - Orange
            3: 'primary',   # Livraison - Bleu foncé
            4: 'success'    # Terminé - Vert
        }
        return status_colors.get(self.order_status, 'secondary')

    def get_status_step(self):
        """Retourne les informations de l'étape actuelle pour le stepper"""
        return {
            'current_step': self.order_status,
            'progress': self.progress,
            'status_text': self.get_order_status_display()
        }

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Achat"
        verbose_name_plural = "Achats"
        unique_together = ['product','buyer']

#Gains/Interet sur les projet
class GainRecord(models.Model):
    project = models.ForeignKey(ValidatedProject, on_delete=models.CASCADE, related_name='gain_records')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant du gain")
    created_at = models.DateField(verbose_name="Date du gain")
    
    def __str__(self):
        return f"{self.amount} {self.project.currency} le {self.created_at}"