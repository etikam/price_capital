from django.shortcuts import render, redirect
from app.forms import ProjectSubmissionForm
from app.forms import PorteurProjectForm
from django.contrib import messages
from app.models import PorteurProject
from django.contrib.auth.decorators import login_required
from app.utils.mailing import send_success_submision_project_mail

# Create your views here.


def index(request):

    return render(request, "app/home/index.html")


@login_required(login_url="auth:login")
def project_submision(request):
    # Initionalisation des informations du porteur de projet par le profile de celui qui est connecté
    initial_data = {}

    if request.user.physical_person:
        initial_data = {
            "first_name": request.user.physical_person.first_name,
            "last_name": request.user.physical_person.last_name,
            "phone": request.user.physical_person.telephone,
            "adress": request.user.physical_person.adresse,
            "birthday": request.user.physical_person.birthday,
            "photo": request.user.physical_person.photo,
        }
    elif request.user.moral_person:
        initial_data = {
            "first_name": request.user.moral_person.company_name,
            "phone": request.user.moral_person.telephone,
            "adress": request.user.moral_person.adresse,
            "photo": request.user.moral_person.photo,
        }

    if request.method == "POST":
        # Récupération des données soumises par l'utilisateur
        form_project = ProjectSubmissionForm(request.POST, request.FILES)
        form_owner = PorteurProjectForm(request.POST, initial=initial_data)

        # Validation des deux formulaires
        if form_project.is_valid() and form_owner.is_valid():

            if PorteurProject.objects.filter(**form_owner.cleaned_data).exists():
                owner = PorteurProject.objects.filter(**form_owner.cleaned_data)[0]
            else:
                owner = form_owner.save()
                
            project = form_project.save(commit=False)
            project.owner = owner  # Lier le projet au porteur de projet
            project.user = (
                request.user
            )  # Associer l'utilisateur connecté à l'instance du projet
            project.save()

            messages.success(
                request,
                "Votre soumission du projet a bien été effectué, veuillez consulter votre mail pour plus de détails",
            )
            send_success_submision_project_mail(request.user)
            # ici je dois encore implementer l'envoie de mail de succès pour la soumission du projet
            # Redirection ou message de succès après la soumission
            return redirect("home")
        else:
            messages.error(
                request,
                f"Il y'a une erreur lors de la soumission de votre projet, veuillez respecter les normes des champs\n {form_owner.errors}\n ",
            )
    else:
        # Affichage des formulaires pour la première fois
        form_project = ProjectSubmissionForm()
        form_owner = PorteurProjectForm(initial=initial_data)

    context = {
        "form_project": form_project,
        "form_owner": form_owner,
    }
    return render(request, "app/project/submision.html", context)
