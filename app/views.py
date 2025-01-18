from django.shortcuts import render, redirect, get_object_or_404
from app.forms import ProjectSubmissionForm, ProductInfoForm
from app.forms import PorteurProjectForm
from .forms import ContactForm
from django.contrib import messages
from app.models import PorteurProject, Project, ValidatedProject, ProjectCategory, ProjectType
from django.contrib.auth.decorators import login_required
from app.utils.mailing import send_success_submision_project_mail,send_report_mail_to_superusers
from django.core.paginator import Paginator
# Create your views here.
from django.http import Http404


def index(request):
    # Filtrer uniquement les projets approuvés
    projects = ValidatedProject.objects.filter(is_approved=True).order_by("-updated_at")
    
    # Récupérer les catégories et les régions depuis la base de données
    categories = ProjectCategory.objects.all()
    regions = projects.values_list('location', flat=True).distinct()
    project_types = ProjectType.objects.all().order_by('-name')
    # Pagination
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "regions": regions,
        'project_types':project_types
    }
    return render(request, "app/home/index.html", context)

@login_required(login_url="auth:login")
def project_submision(request):
    # Initialisation des informations du porteur de projet par le profile de celui qui est connecté
    initial_data = {}

    if hasattr(request.user, 'physical_person') and request.user.physical_person:
        initial_data = {
            "first_name": request.user.physical_person.first_name,
            "last_name": request.user.physical_person.last_name,
            "phone": request.user.physical_person.telephone,
            "adress": request.user.physical_person.adresse,
            "birthday": request.user.physical_person.birthday,
            "photo": request.user.physical_person.photo,
        }
    elif hasattr(request.user, 'moral_person') and request.user.moral_person:
        initial_data = {
            "first_name": request.user.moral_person.company_name,
            "phone": request.user.moral_person.telephone,
            "adress": request.user.moral_person.adresse,
            "photo": request.user.moral_person.logo,
            "birthday": request.user.moral_person.rccm,
        }
    else:
        messages.info(request, "Vous êtes probablement un simple super admin, alors votre espace personnel c'est votre administration")

    if request.method == "POST":
        # Récupération des données soumises par l'utilisateur
        form_project = ProjectSubmissionForm(request.POST, request.FILES)
        form_owner = PorteurProjectForm(request.POST, initial=initial_data)
        form_product = ProductInfoForm(request.POST, request.FILES)

        # Validation des formulaires
        if form_project.is_valid() and form_owner.is_valid():
            # Enregistrement du porteur de projet
            if PorteurProject.objects.filter(**form_owner.cleaned_data).exists():
                owner = PorteurProject.objects.filter(**form_owner.cleaned_data)[0]
            else:
                owner = form_owner.save()

            # Enregistrement du projet
            project = form_project.save(commit=False)
            project.owner = owner
            project.user = request.user
            project.save()

            # Si le type de projet est "ACHAT ANTICIPE", enregistrer les informations du produit
            if project.project_type.name == "ACHAT ANTICIPE" and form_product.is_valid():
                
                print(f"ENREGISTREMENT DU PRODUIT")
                product_info = form_product.save(commit=False)
                product_info.project = project
                product_info.save()
            else:
                 messages.error(
                request,
                f"Erreur lors de l'enregistrement du projet {form_product.errors}",
            )
            messages.success(
                request,
                "Votre soumission du projet a bien été effectuée, veuillez consulter votre mail pour plus de détails",
            )
            con = {
                "Nom": owner.first_name,
                "titre_du_projet": project.title
            }
            send_success_submision_project_mail(request.user, context=con)
            return redirect("home")
        else:
            messages.error(
                request,
                f"Il y a une erreur lors de la soumission de votre projet, veuillez respecter les normes des champs\n {form_owner.errors}\n {form_project.errors}\n {form_product.errors if form_product else ''}",
            )
    else:
        # Affichage des formulaires pour la première fois
        form_project = ProjectSubmissionForm()
        form_owner = PorteurProjectForm(initial=initial_data)
        form_product = ProductInfoForm()

    context = {
        "form_project": form_project,
        "form_owner": form_owner,
        "form_product": form_product,
    }
    return render(request, "app/project/submision.html", context)

def cabinet_home(request):
    context = {}
    return render(request,"app/project/salon.html",context)


def incoming(request):
    # Filtrer les projets soumis ou en cours de validation
    projets = Project.objects.filter(status__in=["submited","accepted","rejected"]).order_by("-updated_at")
    # projets = Project.objects.filter(status="submited")
    context = {
        'projets': projets,
    }
    return render(request, 'app/project/incoming.html', context)


def validated(request):
    # Filtrer les projets dont le status n'est ni "submited" ni "rejected"
    projets = Project.objects.exclude(status__in=["submited", "rejected","accepted"]).order_by("-updated_at")

    context = {
        "projets": projets,
    }
    return render(request,'app/project/validated.html', context)


def detail_project(request,uid):
    project = get_object_or_404(ValidatedProject,uid=uid)
    context = {
        'validate_project':project
    }
    
    return render(request,"app/home/details_project.html",context)

#Espace soumetteur de projet

@login_required
def user_space(request):
    projects = Project.objects.filter(user=request.user).select_related("owner", "category").order_by("-updated_at")

    # Calculs des statistiques
    completed_projects = projects.filter(status="completed").count()
    ongoing_projects = projects.filter(status="published").count()
    total_investors = sum(project.investors_count for project in projects)  # À adapter selon votre modèle.

    context = {
        "projects": projects,
        "completed_projects": completed_projects,
        "ongoing_projects": ongoing_projects,
        "total_investors": total_investors,
    }
    return render(request, "app/space/user_space_1.html", context)


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    # Récupérer les autres projets de l'utilisateur
    other_projects = Project.objects.filter(user=request.user).exclude(id=project_id).order_by("-updated_at")

    context = {
        'project': project,
        'other_projects': other_projects,
    }
    return render(request, 'app/space/project_detail.html', context)


@login_required
def cabinet_project_detail(request, project_id):
    # Récupérer le projet correspondant à l'ID
    project = get_object_or_404(Project, id=project_id)
    
    # Vérifier si le projet est publié
    if project.status != "published":
        raise Http404("Les détails du cabinet ne sont disponibles que pour les projets publiés.")
    
    # Récupérer les informations du projet validé
    validated_project = ValidatedProject.objects.filter(project=project).first()
    
    # Passer les données au contexte
    context = {
        "project": validated_project,
        "validated_project": validated_project,
    }

    return render(request, "app/space/cabinet_project_detail.html", context)


#Nous contacter

def contact_us(request):
    
    return render(request,"app/contact/contact.html")




def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Envoyer un email aux super utilisateurs
            html_path = "app/mailing/contact_notification.html"
            subject = "Nouveau message de contact soumis"
            context = {
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone,
                'subject': contact.subject,
                'message': contact.message,
            }
            send_report_mail_to_superusers(subject, html_path, context)

            messages.success(request, "Votre message a été envoyé avec succès !")
            return redirect('contact')
    
    form = ContactForm()
    print(f"=========={form}============")
    return render(request, 'app/contact/contact.html', {'form': form})