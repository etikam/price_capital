from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvestorForm
from django.contrib.auth.decorators import login_required
from .models import Investor
from django.contrib import messages
from investors.models import Investissement
from investors.forms import InvestissementForm
from app.models import ValidatedProject


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

@login_required
def investment_dashboard(request):
    # Récupérer les investissements de l'utilisateur connecté
    investments = Investissement.objects.filter(investor=request.user.investor)

    # Calculer les statistiques
    total_invested = sum(investment.amount for investment in investments)
    total_gains = 0 # sum(investment.project.expected_gains for investment in investments if investment.project)  # À adapter selon votre modèle
    total_balance = total_invested + total_gains  # Exemple de calcul du solde

    context = {
        'investments': investments,
        'total_invested': total_invested,
        'total_gains': total_gains,
        'total_balance': total_balance,
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
                        "du projet {project.title}, Veuillez continuer le processuces"
                        "d'investissement dans votre espace Investissement",
            )
            except:
                messages.error(request,"Erreur lors de l'initialisation du processus d'investissement, veuillez reprendre ou contacter les administrateurs")
                return redirect("home")
    else:
        return render(request,"investors/not_investor.html")
            
    return redirect('investor:investment-dashboard')

def investissement(request, uid=None):
    # Récupérer ou initialiser l'investissement
    if uid:
        investissement = get_object_or_404(Investissement, uid=uid)
    else:
        investissement = Investissement.objects.create(
            investor=request.user.investor,
            project=None,  # À définir lors de l'initialisation
        )
        investissement.save()

    step = investissement.progress

    if request.method == "POST":
        form = InvestissementForm(request.POST, instance=investissement)
        if form.is_valid():
            form.save()
            investissement.progress = min(investissement.progress + 25, 100)
            investissement.save()
            messages.success(request, "Étape complétée avec succès.")
            return redirect("investissement_form", uid=investissement.uid)
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = InvestissementForm(instance=investissement)

    return render(
        request,
        "investors/investement_form.html",
        {
            "form": form,
            "investissement": investissement,
            "step": step,
        },
    )
