from django.shortcuts import render, redirect, get_object_or_404
from .forms import InvestorForm, AchatForm
from django.contrib.auth.decorators import login_required
from .models import Investor, GainRecord, Achat
from django.contrib import messages
from django.utils.html import strip_tags
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum, F
from django.views.decorators.http import require_POST
from app.models import ValidatedProductInfo


class MyAchats(LoginRequiredMixin, ListView):
    model = Achat
    template_name = 'investors/my_achats.html'
    context_object_name = 'achats'

    def get_queryset(self):
        return Achat.objects.filter(buyer=self.request.user.investor)


class AchatDetailView(LoginRequiredMixin, DetailView):
    model = Achat
    template_name = 'investors/investment_details_achat.html'
    context_object_name = 'achat'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        achat = self.get_object()
        
        # Ajouter des informations supplémentaires au contexte
        context.update({
            'total_amount': achat.total_amount,
            'product_info': {
                'name': achat.product.product_name,
                'description': achat.product.product_description,
                'unit_price': achat.product.unit_price,
                'currency': "GNF",
                'quantity_available': achat.product.quantity_available,
            },
            'achat_form': AchatForm(instance=achat),
        })
        
        return context


@login_required
def initiate_purchass(request, uid):
    product = get_object_or_404(ValidatedProductInfo, uid=uid)
    investor = None
    if request.user.investor:
        investor = request.user.investor

    if investor:
        if Achat.objects.filter(buyer=investor, product=product).exists():
            messages.info(request,"vous avez deja initialisé l'investissement pour ce projet, veuillez le consulter dans votre espace Investissement")
            return redirect("home")
        else:
            try:
                achat = Achat.objects.create(product=product, buyer=investor)
                messages.success(
                request,
                    f"Felicatation, Nous vous remercions de vouloir etre financier "
                        f"du projet {product.Project.title}, Veuillez continuer le processuces"
                        "d'investissement dans votre espace Investissement",
            )
            except Exception as e:
                messages.error(
                    request,
                        f"Erreur lors de l'initialisation du processus d'investissement : Si le problème persiste, Veuillez contacter les Administrateur"
                        f"Veuillez réessayer ou contacter les administrateurs. '{e}")
               
    else:
        return render(request,"investors/not_investor.html")
            
    return redirect('investor:investment-dashboard')


@login_required
def set_achat_quantity(request, uid=None):
    if uid is not None:
        achat = get_object_or_404(Achat, uid=uid)
    else:
        achat = None

    # Gérer la soumission du formulaire
    if request.method == "POST":
        form = AchatForm(request.POST, instance=achat)
        if form.is_valid():
            achat = form.save()
            achat.progress = 50
            achat.save()
            messages.success(
                request,
                "Achat enregistré avec succès. Veuillez continuer vers le paiement pour terminer le processus d'achat!",
            )
        else:
            # Supprimer les balises HTML des erreurs
            clean_errors = strip_tags(str(form.errors))
            messages.error(
                request, f"Veuillez corriger les erreurs ci-dessous : {clean_errors}"
            )
    else:
        # Initialiser le formulaire
        form = AchatForm(instance=achat)
    
    return redirect('investor:investment-dashboard')


@login_required
@require_POST
def annuler_achat(request, uid):
    """Vue pour annuler un achat"""
    try:
        # Récupérer l'achat et vérifier qu'il appartient bien à l'investisseur connecté
        achat = get_object_or_404(Achat, uid=uid, buyer=request.user.investor)
        
        # Vérifier que l'achat n'est pas déjà terminé
        if achat.progress >= 100:
            messages.error(request, "Impossible d'annuler un achat déjà terminé.")
            return redirect('investor:mes-achats')
            
        # Stocker les informations pour le message de confirmation
        product_name = achat.product.product_name
        
        # Supprimer l'achat
        achat.delete()
        
        # Message de succès avec les détails de l'achat supprimé
        messages.success(
            request, 
            f"L'achat du produit '{product_name}' a été supprimé avec succès."
        )
        
    except Achat.DoesNotExist:
        messages.error(
            request, 
            "L'achat que vous essayez d'annuler n'existe pas ou ne vous appartient pas."
        )
    except Exception as e:
        messages.error(
            request,
            f"Une erreur s'est produite lors de l'annulation de l'achat. Si le problème persiste, veuillez contacter l'administrateur. {e}"
        )
    
    return redirect('investor:mes-achats')
