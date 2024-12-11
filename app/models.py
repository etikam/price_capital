from django.db import models
from django.conf import settings


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
        ("ongoing", "En cours"),
        ("completed", "Terminé"),
        ("upcoming", "À venir"),
    ]

    CURRENCY_CHOICES = [
        ("GNF", "GNF - Franc guinéen"),
        ("USD", "USD - Dollar américain"),
        ("EUR", "EUR - Euro"),
        ("XOF", "XOF - Franc CFA"),
        # Ajoutez d'autres monnaies si nécessaire
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Utilisateur",
    )
    owner = models.ForeignKey(
        PorteurProject,
        related_name="projects",
        on_delete=models.CASCADE,
        verbose_name="Porteur de projet",
    )
    title = models.CharField(max_length=255, verbose_name="Titre du projet")
    description = models.TextField(
        max_length=1000, verbose_name="Description du projet"
    )
    # category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, 
    # verbose_name="Catégorie", help_text="Catégorie du projet")
    category = models.ForeignKey(
        ProjectCategory,
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
    # exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0, help_text="Taux de change par rapport au GNF", verbose_name="Taux de change")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming",
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

    def __str__(self):
        return self.title

    @property
    def progress(self):
        """Calcule le pourcentage d'évolution du financement."""
        if self.goal == 0:
            return 0
        return min((self.current_funding / self.goal) * 100, 100)

    @property
    def converted_budget(self):
        """Convertit le budget en monnaie locale (GNF) si une autre monnaie est utilisée."""
        self.budget = self.goal * self.exchange_rate
        return self.budget

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'owner', 'title'], name='unique_project')
        ]