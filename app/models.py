from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
import uuid


# porteur de projet, au cas où un utilisateur peut soumettre un projet avec d'autre informations
class PorteurProject(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    adress = models.TextField()
    birthday = models.DateField()
    photo = models.ImageField(upload_to="img_porteur")


class ProjectCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("submited", "Soumis"),     #quand le projet est soumis (uniquement pour les soumetteurs )
        ("ongoing", "En cours"),  #quand la collecte des fond sur le projet a debuté
        ("reformulated", "Reformulé"),  #quand la reformulation du  projet est terminée
        ("completed", "Terminé"),   #quand le projet est réalisé
        ("published", "Publié"),   #quand le projet est publié
        ("rejected", "Rejeté"),     #quand le projet est rejeté (pour quelque raison que ce soit) avant meme d'être reformulé
        ("accepted", "Accepté"),    #quand le projet est accepté
    ]

    CURRENCY_CHOICES = [
        ("GNF", "GNF - Franc guinéen"),
        ("USD", "USD - Dollar américain"),
        ("EUR", "EUR - Euro"),
        ("XOF", "XOF - Franc CFA"),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Utilisateur",
    )
    
    owner = models.ForeignKey(
        "PorteurProject",
        related_name="projects",
        on_delete=models.CASCADE,
        verbose_name="Porteur de projet",
    )
    
    uid = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    unique=True,
    verbose_name="Identifiant unique",
        )
    
    title = models.CharField(max_length=255, verbose_name="Titre du projet")
    description = models.TextField(
        max_length=1000,
        verbose_name="Description du projet",
        default="Description du projet",
    )
    
    presentation_document = models.FileField(
        upload_to="project_documents/",
        blank=True,
        null=True,
        verbose_name="Document de présentation",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "docx", "ppt", "pptx"])
        ],
    )
    
    business_plan = models.FileField(
        upload_to="project_documents/",
        blank=True,
        null=True,
        verbose_name="Business Plan",
        validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "docx", "ppt", "pptx"])
        ],
    )
    category = models.ForeignKey(
        "ProjectCategory",
        related_name="projects",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Categorie du projet",
    )
    goal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Budget estimé en GNF",
        verbose_name="Objectif du projet (Budget)",
    )

    location = models.CharField(
        max_length=255, help_text="Localisation du projet", verbose_name="Localisation"
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="GNF",
        verbose_name="Monnaie",
        help_text="Sélectionnez la monnaie pour le budget",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submited",
        verbose_name="Statut du projet",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    image = models.ImageField(
        upload_to="project_images/",
        blank=True,
        null=True,
        verbose_name="Image du projet",
    )

    is_approved = models.BooleanField(
        default=False, verbose_name="Validé ?", help_text="Indique si le projet est approuvé pour publication"
    )
    
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'approbation",
        help_text="Date à laquelle le projet a été validé",
    )
    def __str__(self):
        return self.title


    @property
    def converted_budget(self):
        """Convertit le budget en monnaie locale (GNF) si une autre monnaie est utilisée."""
        self.budget = self.goal * self.exchange_rate
        return self.budget

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "owner", "title"], name="unique_project"
            )
        ]

#Projets reformurlés par le cabinet


class ValidatedProject(models.Model):

    CURRENCY_CHOICES = [
        ("GNF", "GNF - Franc guinéen"),
        ("USD", "USD - Dollar américain"),
        ("EUR", "EUR - Euro"),
        ("XOF", "XOF - Franc CFA"),
    ]
    project = models.OneToOneField(
        "Project", on_delete=models.CASCADE, related_name="validated_project", verbose_name="Projet soumis"
    )
    
    title = models.CharField(
        max_length=255, verbose_name="Titre reformulé", help_text="Titre final du projet présenté aux investisseurs"
    )
    
    description = models.TextField(
    max_length=1000,
    verbose_name="Description résumé",
    default="Description du projet",
    )
    
    context = models.TextField(
        verbose_name="Contexte", help_text="Description générale du contexte du projet"
    )
    
    summary = models.TextField(
        verbose_name="Résumé", help_text="Résumé succinct du projet"
    )
    
    problem_statement = models.TextField(
        verbose_name="Problématique", help_text="Décrivez le problème que le projet vise à résoudre"
    )
    
    general_objective = models.TextField(
        verbose_name="Objectif général", help_text="Objectif principal que le projet vise à atteindre"
    )
    
    specific_objectives = models.TextField(
        verbose_name="Objectifs spécifiques", help_text="Liste des objectifs spécifiques du projet"
    )
    
    deliverables = models.TextField(
        verbose_name="Livrables", help_text="Ce que le projet produira (produits, services, résultats mesurables)"
    )
    
    target_audience = models.TextField(
        verbose_name="Public cible", help_text="Décrivez les bénéficiaires ou utilisateurs finaux"
    )
    
    key_partners = models.TextField(
        verbose_name="Partenaires clés", blank=True, null=True, help_text="Liste des partenaires du projet"
    )
    
    additional_details = models.TextField(
        verbose_name="Informations supplémentaires", blank=True, null=True, help_text="Autres détails pertinents"
    )
    
    
    category = models.ForeignKey(
        "ProjectCategory",
        related_name="validated_project",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Categorie du projet",
    )
    goal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Budget estimé en GNF",
        verbose_name="Objectif du projet (Budget)",
        null=True, blank=True
    )
    current_funding = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="Montant financé en GNF",
        verbose_name="Montant financé",
    )
    location = models.CharField(
        max_length=255, help_text="Localisation du projet", verbose_name="Localisation"
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="GNF",
        verbose_name="Monnaie",
        help_text="Sélectionnez la monnaie pour le budget",
    )

    
    documents = models.FileField(
        upload_to="validated_project_docs/",
        blank=True,
        null=True,
        verbose_name="Documents associés",
        help_text="Documents validés (business plan, présentation, etc.)",
    )
    
    reformulated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Validé par",
        help_text="L'utilisateur ou l'administrateur ayant validé et reformulé le projet",
    )
    
    image = models.ImageField(
        upload_to="project_reformulated_images/",
        blank=True,
        null=True,
        verbose_name="Image de couverture du projet",
    )
    
    
    is_approved = models.BooleanField(
        default=False, verbose_name="Validé ?", help_text="Indique si le projet est approuvé pour publication"
    )
    
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'approbation",
        help_text="Date à laquelle le projet a été validé",
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return self.title
    
    @property
    def progress(self):
        """Calcule le pourcentage d'évolution du financement."""
        if not self.goal or not self.current_funding:  # Vérifie si goal ou current_funding est None ou égal à 0
            return 0
        return min((self.current_funding / self.goal) * 100, 100)
