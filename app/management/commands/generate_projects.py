import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Project, PorteurProject, ProjectCategory
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Insère 30 projets avec des données aléatoires'

    def handle(self, *args, **kwargs):
        # Récupérer l'utilisateur
        user = User.objects.get(email="etiennedheleine2000@gmail.com")

        # Récupérer les catégories disponibles
        categories = ProjectCategory.objects.all()

        # Liste des informations du porteur de projet
        porteurs = [
            {"first_name": "Etienne", "last_name": "Kamano", "phone": "123456789", "adress": "Conakry, Guinée", "birthday": "1990-01-01"},
            {"first_name": "Gilbert", "last_name": "Diakité", "phone": "987654321", "adress": "Labé, Guinée", "birthday": "1992-03-15"},
            {"first_name": "Mamadou", "last_name": "Sory", "phone": "135792468", "adress": "Kindia, Guinée", "birthday": "1988-05-22"},
            {"first_name": "Aissatou", "last_name": "Diallo", "phone": "112233445", "adress": "Conakry, Guinée", "birthday": "1995-11-10"},
            {"first_name": "Amadou", "last_name": "Camara", "phone": "223344556", "adress": "Kankan, Guinée", "birthday": "1985-07-25"},
            {"first_name": "Mariam", "last_name": "Keita", "phone": "334455667", "adress": "Boké, Guinée", "birthday": "1998-02-17"},
            {"first_name": "Ibrahime", "last_name": "Toure", "phone": "445566778", "adress": "Nzérékoré, Guinée", "birthday": "1987-04-30"},
            {"first_name": "Sadio", "last_name": "Bah", "phone": "556677889", "adress": "Mamou, Guinée", "birthday": "1991-06-09"},
            {"first_name": "Oumar", "last_name": "Camara", "phone": "667788990", "adress": "Faranah, Guinée", "birthday": "1989-12-19"},
            {"first_name": "Nadia", "last_name": "Diallo", "phone": "778899001", "adress": "Conakry, Guinée", "birthday": "1994-05-13"},
            {"first_name": "Sekou", "last_name": "Diakité", "phone": "889900112", "adress": "Labé, Guinée", "birthday": "1993-08-20"},
            {"first_name": "Fanta", "last_name": "Sow", "phone": "990011223", "adress": "Boké, Guinée", "birthday": "1996-09-04"},
            {"first_name": "Alhassane", "last_name": "Fofana", "phone": "101223344", "adress": "Kindia, Guinée", "birthday": "1986-11-05"},
            {"first_name": "Fatoumata", "last_name": "Bah", "phone": "112344556", "adress": "Conakry, Guinée", "birthday": "1999-01-18"},
            {"first_name": "Lamine", "last_name": "Koné", "phone": "223455667", "adress": "Kankan, Guinée", "birthday": "1990-03-03"},
            {"first_name": "Moussa", "last_name": "Barry", "phone": "334566778", "adress": "Nzérékoré, Guinée", "birthday": "1984-10-15"},
            {"first_name": "Mariama", "last_name": "Diarra", "phone": "445677889", "adress": "Mamou, Guinée", "birthday": "1997-02-12"},
            {"first_name": "Kadiatou", "last_name": "Touré", "phone": "556788990", "adress": "Faranah, Guinée", "birthday": "1992-07-21"},
            {"first_name": "Abdoulaye", "last_name": "Sory", "phone": "667899001", "adress": "Labé, Guinée", "birthday": "1987-06-11"},
            {"first_name": "Saran", "last_name": "Keita", "phone": "778990112", "adress": "Conakry, Guinée", "birthday": "1994-04-28"},
        ]


        for i in range(30):
            # Choisir un porteur de projet au hasard
            owner_info = random.choice(porteurs)
            owner = PorteurProject.objects.create(
                first_name=owner_info["first_name"],
                last_name=owner_info["last_name"],
                phone=owner_info["phone"],
                adress=owner_info["adress"],
                birthday=owner_info["birthday"],
                photo="path_to_photo"  # Vous pouvez spécifier un chemin de photo ici si nécessaire
            )

            # Choisir une catégorie au hasard
            category = random.choice(categories)

            # Créer un projet
            project = Project.objects.create(
                user=user,  # Assigner l'utilisateur à ce projet
                owner=owner,  # Assigner le porteur de projet
                title=f"Projet {i+1}",
                description="Description aléatoire pour le projet.",
                category=category,
                goal=random.randint(50000, 1000000),  # Un budget aléatoire entre 50 000 et 1 000 000
                location="Conakry, Guinée",  # Localisation générique
                currency="GNF",  # Monnaie par défaut
                status="submited",  # Statut initial
                is_approved=False,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

            # Afficher un message pour chaque projet créé
            self.stdout.write(self.style.SUCCESS(f"Projet {i+1} créé avec succès !"))
