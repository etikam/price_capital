from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvestorForm
from django.contrib.auth.decorators import login_required
from .models import Investor
from django.contrib import messages
from investors.models import Investissement
from investors.forms import InvestissementForm
from app.models import ValidatedProject
from django.db.models import Sum, Count
from django.utils.timezone import now
from datetime import timedelta
import calendar
from django.db.models.functions import ExtractMonth  
from .forms import InvestissementForm
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

@login_required
def become_investor(request):
    if request.method == "POST":
        form = InvestorForm(request.POST)
        if form.is_valid():
            investor = form.save(commit=False)
            investor.user = request.user
            investor.save()
            form.save_m2m()  # Sauvegarde les relations ManyToMany (comme preferred_sectors)
            return redirect(
                "my-space"
            )  # Redirige vers l'espace personnel de l'utilisateur
    else:
        form = InvestorForm()

    return render(request, "investors/become_investor.html", {"form": form})

from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone
from datetime import timedelta

@login_required
def investment_dashboard(request):
    # Récupérer les investissements en cours (progression < 100) de l'utilisateur connecté
    investments = Investissement.objects.filter(
        investor=request.user.investor,
        progress__lt=100  # Filtre pour les investissements non terminés
    ).order_by("-updated_at")

    # Calculer les statistiques clés
    total_invested = investments.aggregate(Sum('amount'))['amount__sum'] or 0
    total_gains = sum(
        investment.percentage_on_goal * investment.gains / 100
        for investment in investments
    )
    nombre_project_investi = Investissement.objects.filter(investor=request.user.investor).count() #à remedier la requette(parce qu'il faut que le payement soit fait pour que le projet soit compte comme investi)
  
    # Calculer les données pour les graphiques
    six_months_ago = timezone.now() - timedelta(days=180)  # Données des 6 derniers mois

    # Fréquence des investissements par mois
    frequency_data = (
        investments.filter(created_at__gte=six_months_ago)
        .annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'))
        .values('year', 'month')
        .annotate(count=Count('id'))
        .order_by('year', 'month')
    )

    # Évolution des gains par mois
    interest_data = (
        investments.filter(created_at__gte=six_months_ago)
        .annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'))
        .values('year', 'month')
        .annotate(total_gains=Sum('gains'))
        .order_by('year', 'month')
    )

    # Préparer les labels et les données pour les graphiques
    frequency_labels = []
    frequency_values = []
    interest_labels = []
    interest_values = []

    for data in frequency_data:
        month_name = timezone.datetime(year=data['year'], month=data['month'], day=1).strftime('%B')
        frequency_labels.append(month_name)
        frequency_values.append(data['count'])

    for data in interest_data:
        month_name = timezone.datetime(year=data['year'], month=data['month'], day=1).strftime('%B')
        interest_labels.append(month_name)
        interest_values.append(data['total_gains'] or 0)

    # Gérer la soumission du formulaire d'investissement
    if request.method == 'POST':
        # Récupérer l'UID de l'investissement depuis le formulaire
        investment_uid = request.POST.get('investment_uid')
        investment = get_object_or_404(Investissement, uid=investment_uid, investor=request.user.investor)

        # Traiter la soumission du formulaire
        form = InvestissementForm(request.POST, instance=investment)
        if form.is_valid():
            form.save()
            return redirect('investor:investment_dashboard')  # Rediriger vers le tableau de bord
    else:
        # Afficher le formulaire vide (pour la modale)
        form = InvestissementForm()

    # Contexte pour le template
    context = {
        'investments': investments,
        'total_invested': total_invested,
        'total_gains': total_gains,
        'nombre_project_investi': nombre_project_investi,
        'investment_frequency_labels': frequency_labels,
        'investment_frequency_data': frequency_values,
        'interest_evolution_labels': interest_labels,
        'interest_evolution_data': interest_values,
        'form': form,  # Ajouter le formulaire au contexte
    }

    return render(request, "investors/investment_dashboard.html", context)


@login_required
def check_investor_profile(request):
    # Vérifie si l'utilisateur a un profil investisseur
    try:
        investor = Investor.objects.get(user=request.user)
        # Si oui, redirige vers la page d'investissement
        return redirect(
            "investor:investment-dashboard"
        )  # Remplace par le nom de ta vue pour le tableau de bord des investissements
    except Investor.DoesNotExist:
        # Si non, affiche une page pour proposer de devenir investisseur
        return render(request, "investors/not_investor.html")


# initilistaion de l'investissemnt:
@login_required
def initiate_investment(request, uid):
    
    project = get_object_or_404(ValidatedProject, uid=uid)
    investor = None
    if request.user.investor:
        investor = request.user.investor

    if investor:
        if Investissement.objects.filter(investor=investor, project=project).exists():
            messages.info(request,"vous avez deja initialisé l'investissement pource projet, veuillez le consulter dans votre espace Investissement")
            return redirect("home")
        else:
            
            try:
                investissement = Investissement.objects.create(project=project, investor=investor)
                messages.success(
                    request,
                    f"Felicatation, Nous vous remercions de vouloir etre financier "
                        f"du projet {project.title}, Veuillez continuer le processuces"
                        "d'investissement dans votre espace Investissement",
            )
            except Exception as e:  # Capturer l'exception spécifique
                messages.error(
                    request,
                    f"Erreur lors de l'initialisation du processus d'investissement : Si le problème persiste, Veuillez contacter les Administrateur"
                    "Veuillez réessayer ou contacter les administrateurs.")
                return redirect("home")
    else:
        return render(request,"investors/not_investor.html")
            
    return redirect('investor:investment-dashboard')





def investissement(request, uid=None):
    # Récupérer l'investissement existant ou en créer un nouveau
    if uid:
        investissement = get_object_or_404(Investissement, uid=uid)


    # Gérer la soumission du formulaire
    if request.method == 'POST':
        form = InvestissementForm(request.POST, instance=investissement)
        if form.is_valid():
            investissement = form.save()
            investissement.progress = 50
            investissement.save()
            messages.success(request, "Investissement enregistré avec succès Veuillez continuez vers le payment pour terminé le processus d'investissement!")
        else:
            
            # Supprimer les balises HTML des erreurs
            clean_errors = strip_tags(str(form.errors))
            messages.error(request, f"Veuillez corriger les erreurs ci-dessous : {clean_errors}")
    else:
        # Initialiser le formulaire
        form = InvestissementForm(instance=investissement)

    # Rendre le template avec le formulaire
    return redirect("investor:investment-dashboard")



@require_POST
def annuler_investissement(request, uid):
    # Récupérer l'investissement
    investissement = get_object_or_404(Investissement, uid=uid, investor=request.user.investor)

    # Annuler l'investissement (par exemple, marquer comme annulé)
    investissement.delete()
    # Afficher un message de succès
    messages.success(request, "L'investissement a été annulé avec succès.")

    # Rediriger vers le tableau de bord
    return redirect("investor:investment-dashboard")