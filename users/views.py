from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, View
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout
from .forms import CustomAuthenticationForm
from .forms import CustomUserCreationForm
from users.models import User, PhysicalPerson, MoralPerson
from .utils.mailing import send_activation_email, send_password_reset_mail
from django.contrib.auth.decorators import login_required
from .forms import (
    PhysicalPersonForm,
    MoralPersonForm,
    PhysicalPersonForm,
    MoralPersonForm,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

User = get_user_model()
# class CustomLoginView(LoginView):
#     authentication_form = CustomAuthenticationForm


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(
                request, email=clean_data["email"], password=clean_data["password"]
            )
            if user:
                login(request, user)

                messages.success(
                    request, f"Bienvenu, Vous êtes connecté en tant que {user.email}"
                )
                return redirect("home")
            else:
                messages.error(request, "Email ou mot de passe incorrecte")

        else:
            messages.error(request, "Veuillez à saisir les informations valides.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


class LogoutView(View):
    login_url = reverse_lazy("home")

    def get(self, request):
        logout(request)
        messages.success(
            self.request, "Vous êtes maintenant deconnecté de la Prices Capital"
        )
        return redirect(self.login_url)


class CustomUserCreationView(CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("auth:register")

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            context ={}
            send_activation_email(user)

            messages.success(
                self.request,
                (
                    "Un lien vous a été envoyé dans votre boite mail, veuillez le consulter pour continuer l'inscription"
                ),
            )
            return redirect(self.success_url)


class ActivationUserView(View):
    def get(self, request, uid, token):
        try:
            id = urlsafe_base64_decode(uid).decode()  # Décoder correctement l'UID
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValueError):
            return render(request, "registration/activation_invalid.html")

        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(
                    request,
                    "Votre adresse email a été vérifiée. Veuillez compléter votre profil.",
                )
            else:
                messages.error(
                    request,
                    "Ce compte est déjà vérifié, si vous n'aviez pas terminé l'inscription avant de sortir, vous pouvez vous connecté avec vos information pour continuer l'inscription dans votre profile",
                )
                return redirect("home")

            # Créer l'URL de redirection avec l'uid en paramètre
            complete_profile_url = reverse("auth:complete_profile", kwargs={"uid": uid})
            return redirect(complete_profile_url)

        return render(request, "registration/activation_invalid.html")


def profile_view(request):
    user = request.user

    # Déterminez si l'utilisateur est une personne physique ou morale
    if hasattr(user, "physical_person"):
        form = PhysicalPersonForm(
            request.POST or None, request.FILES or None, instance=user.physical_person
        )
    elif hasattr(user, "moral_person"):
        form = MoralPersonForm(
            request.POST or None, request.FILES or None, instance=user.moral_person
        )
    else:
        messages.error(request, "Aucun profil associé à cet utilisateur.")
        return redirect("home")

    # Si le formulaire est soumis et valide
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Votre profil a été mis à jour avec succès.")
        return redirect("auth:profile_user")

    context = {"form": form, "user": user}
    return render(request, "registration/user_profile.html", context)


def complete_profile(request, uid):
    try:
        # Décoder l'UID et récupérer l'utilisateur
        decoded_uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(id=decoded_uid)
    except (ValueError, User.DoesNotExist):
        messages.error(request, "Utilisateur invalide ou introuvable.")
        return redirect("home")

    if PhysicalPerson.objects.filter(user=user).exists():
        messages.info(
            request,
            "Vous avez deja un profile en tant que Personne physique, si vous voulez le modifier, allez dans votre profile",
        )
        return redirect("home")

    if MoralPerson.objects.filter(user=user).exists():
        messages.info(
            request,
            "Vous avez deja un profile en tant que Personne Morale, si vous voulez le modifier, allez dans votre profile",
        )
        return redirect("home")

    # Initialisation des formulaires

    physical_form, moral_form = None, None
    if request.method == "POST":
        role = request.POST.get("role")  # Récupérer le rôle choisi
        if role == "PHYSICAL":
            physical_form = PhysicalPersonForm(request.POST, request.FILES)
            if physical_form.is_valid():
                physical_person = physical_form.save(commit=False)
                physical_person.user = user
                physical_person.save()
                messages.success(
                    request,
                    "Votre profil a été complété avec succès, vous pouvez maintenant vous connecter.",
                )
                return redirect("auth:login")
            else:
                messages.error(request, "Veuillez corriger les erreurs du formulaire.")
        elif role == "MORAL":
            moral_form = MoralPersonForm(request.POST, request.FILES)
            if moral_form.is_valid():
                moral_person = moral_form.save(commit=False)
                moral_person.user = user
                moral_person.save()
                messages.success(
                    request,
                    "Votre profil a été complété avec succès, vous pouvez maintenant vous connecter.",
                )
                return redirect("auth:login")
            else:
                messages.error(request, "Veuillez corriger les erreurs du formulaire.")
        else:
            messages.error(request, "Veuillez sélectionner un type de personne valide.")

    # Réinitialisation des formulaires pour GET ou en cas d'erreur POST
    if physical_form is None:
        physical_form = PhysicalPersonForm()
    if moral_form is None:
        moral_form = MoralPersonForm()

    # Passer les données au contexte
    context = {
        "physical_form": physical_form,
        "moral_form": moral_form,
        "uid": uid,  # Passer l'UID pour l'action des formulaires
    }
    return render(request, "registration/complete_profile.html", context)


def check_reset_passord(request):
    if request.method == "POST":
        user_email = request.POST.get("email")
        if not User.objects.filter(email=user_email).exists():
            messages.error(request, "Aucun n'est associé à cette adresse email")
        else:
            user = get_object_or_404(User, email=user_email)
            send_password_reset_mail(user)
            messages.info(
                request,
                "Un mail vous a été envoyé avec un lien de reinitialisation de votre mot de passe,"
                "veuillez le consulter pour continuer l'oppération",
            )


def reset_password(request):
    pass
