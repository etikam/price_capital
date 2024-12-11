from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from django.utils import timezone
from django.conf import settings

ROLE_CHOICES = [
        ('PHYSICAL', 'Personne Physique'),
        ('MORAL', 'Personne Morale'),
        ('INVESTOR', 'Investisseur'),
        ('ADMIN', 'Administrateur'),
    ]

class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(unique=True, max_length=255, verbose_name="email address")

  
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class MoralPerson(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="moral_person")
    company_name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()
    rccm = models.CharField(max_length=100, unique=True, blank=True, null=True) 
    logo = models.ImageField(upload_to="company_logos/")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PHYSICAL')

    def __str__(self):
        return self.company_name


class PhysicalPerson(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="physical_person")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()
    birthday = models.DateField()
    id_card = models.ImageField(upload_to="id_cards/")
    photo = models.ImageField(upload_to="profile_photos/")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"