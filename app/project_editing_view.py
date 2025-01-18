from django.shortcuts import render, redirect, get_object_or_404
from app.models import Project, ValidatedProject

from django.utils import timezone
from django.contrib import messages
from .forms import ValidatedProjectForm
from django.views.decorators.http import require_POST
from app.utils.mailing import send_report_mail_on_project
from .models import ProjectCategory
from .models import ValidatedProductInfo
from .forms import  ValidatedProductInfoForm

def detail_project(request,uid):
    project = get_object_or_404(Project, uid=uid)
    return render(request,"app/project/detail.html", {'project':project})

def detail_product(request,id):
    product= get_object_or_404(ValidatedProductInfo, uid=id)
    return render(request,"app/project/detail.html", {'product':product})




def reformulate_project(request, uid):
    project = get_object_or_404(Project, uid=uid)
    
    # Vérifier si un ValidatedProductInfo existe pour ce projet
    try:
        validated_product_info = ValidatedProductInfo.objects.get(Project=project)
    except ValidatedProductInfo.DoesNotExist:
        validated_product_info = None

    # Si le type de projet est "ACHAT ANTICIPE", utiliser un template spécifique
    if project.project_type.name == "ACHAT ANTICIPE":
        # Préremplir les formulaires
        form = ValidatedProjectForm(instance=project)
        product_form = ValidatedProductInfoForm(instance=validated_product_info)

        if request.method == "POST":
            if validated_product_info:
                product_form = ValidatedProductInfoForm(request.POST, request.FILES, instance=validated_product_info)
            else:
                product_form = ValidatedProductInfoForm(request.POST, request.FILES)

            if product_form.is_valid():
                product_info = product_form.save(commit=False)
                product_info.Project = project  # Lier au projet
                product_info.save()

                # Mettre à jour le statut du projet
                project.status = "reformulated"
                project.save()

                # Préparer et envoyer un mail au propriétaire du projet
                html_path = "app/mailing/reformulated_project_mail.html"
                subject = "Recommandation – Reformulation de votre projet"
                user = project.user
                context = {
                    "Nom": project.owner.first_name,
                    "titre_du_projet": project.title
                }
                messages.success(request, f"Le projet {project.title} a été reformulé avec succès.")
                try:
                    send_report_mail_on_project(user, subject, html_path, context)
                    messages.success(request, "Un mail de retour a été envoyé au soumetteur de projet pour l'informer de l'état actuel de son projet.")
                except Exception as e:
                    messages.warning(request, f"Le projet a été reformulé, mais l'envoi du mail a échoué. {str(e)}")
                
                return redirect("cabinet-incoming")
            else:
                messages.error(request, f"Erreur lors de l'enregistrement des informations du produit. {product_form.errors}")

        context = {
            "form": form,
            "product_form": product_form,
            "project": project,
            "validated_product_info": validated_product_info,
        }
        return render(request, "app/project/reformulate_achat_anticipe.html", context)

    # Pour les autres types de projet, utiliser le template de reformulation standard
    else:
        form = ValidatedProjectForm(instance=project)

        if request.method == "POST":
            form = ValidatedProjectForm(request.POST, instance=project)

            if form.is_valid():
                form.save()

                # Mettre à jour le statut du projet
                project.status = "reformulated"
                project.save()

                # Préparer et envoyer un mail au propriétaire du projet
                html_path = "app/mailing/reformulated_project_mail.html"
                subject = "Recommandation – Reformulation de votre projet"
                user = project.user
                context = {
                    "Nom": project.owner.first_name,
                    "titre_du_projet": project.title
                }
                messages.success(request, f"Le projet {project.title} a été reformulé avec succès.")
                try:
                    send_report_mail_on_project(user, subject, html_path, context)
                    messages.success(request, "Un mail de retour a été envoyé au soumetteur de projet pour l'informer de l'état actuel de son projet.")
                except Exception as e:
                    messages.warning(request, f"Le projet a été reformulé, mais l'envoi du mail a échoué. {str(e)}")
                
                return redirect("cabinet-incoming")
            else:
                messages.error(request, f"Veuillez corriger les erreurs du formulaire. {form.errors}")

        context = {
            "form": form,
            "project": project,
        }
        return render(request, "app/project/reformulate.html", context)


# def reject_project(request):
#     pass



def accepte_project(request, uid):
    project = get_object_or_404(Project, uid=uid)
    project.status = "accepted"
    project.save()
    
    # Création du contexte à passer au template
    context = {
        'Nom': project.owner.first_name,  # Le nom de l'utilisateur (si vous avez un champ first_name dans User)
        'Titre': project.title,  # Le titre du projet
    }
    
    html_path = "app/mailing/accept_project_mail.html"
    subject = f"Acceptation du projet {project.title}"
    user = project.user

    # Envoi du mail avec le contexte
    send_report_mail_on_project(user, subject, html_path, context)

    messages.success(request, f"Le projet {project.title} a été accepté avec succès.")
    messages.success(request, "Un mail de retour a été envoyé au soumetteur de projet pour l'informer de l'état actuel de son projet.")
    
    return redirect('cabinet-incoming')


@require_POST
def publish_project(request, uid):
    # Récupérer le projet et sa validation associée
    is_published = request.POST.get("is_published") == "on"
    project = get_object_or_404(Project, uid=uid)
    validated_project = None
    if project.project_type.name == "ACHAT ANTICIPE":
        validated_project = project.validated_product_info
    else:
        validated_project = get_object_or_404(ValidatedProject, project=project)
    # Vérifier si la case "is_published" a été cochée

    if validated_project.is_approved != is_published:  # Vérifier si un changement est nécessaire
        validated_project.is_approved = is_published
        if is_published:
            project.status = "published"  # Mettre à jour le statut du projet
            project.approved_at = timezone.now()
            #envoie du mail
            html_path = "app/mailing/published_project_mail.html"
            subject = "Votre projet est publié"
            user = project.user
            context = {
                "Nom":project.owner.first_name,
                "titre_du_projet":project.title
            }
            send_report_mail_on_project(user,subject,html_path,context)
            messages.success(request, f"Le projet '{project.title}' a été publié avec succès.")
            messages.success(request, "Un mail de retour a été envoyé au soumetteur de projet pour l'informé de l'état actuel de son projet")
        else:
            project.status = "reformulated"  # Rétablir un statut neutre
            messages.warning(request, f"La publication du projet '{project.title}' a été annulée.")
        
        # Sauvegarder les modifications
        validated_project.save()
        project.save()
    else:
        messages.info(request, "Aucune modification n'a été effectuée.")

    # Redirection vers la page des projets validés
    return redirect("cabinet-validated")



def reject_project(request, uid):
    project = get_object_or_404(Project, uid=uid)

    # Si la requête est en POST, récupérer la raison
    if request.method == 'POST':
        raison = request.POST.get('reason', '')
        
        # Mettre à jour le statut du projet à "rejeté"
        project.status = "rejected"
        project.save()

        # Créer le contexte pour l'email
        context = {
            'Nom': project.owner.first_name,
            'Titre_du_projet': project.title,
            'raison': raison,  # Passer la raison du rejet
        }

        # Envoi du mail
        html_path = "app/mailing/rejected_project_mail.html"
        subject = f"Rejet du projet {project.title}"
        user = project.user
        
        send_report_mail_on_project(user, subject, html_path, context)

        # Message de succès pour l'interface utilisateur
        messages.success(request, f"Le projet '{project.title}' a été rejeté avec succès.")
        messages.success(request, "Un mail de retour a été envoyé au soumetteur de projet.")

        return redirect('cabinet-incoming')
    
    # Si ce n'est pas une requête POST, on redirige
    return redirect('cabinet-incoming')


def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get("name")
        if category_name:
            category, created = ProjectCategory.objects.get_or_create(name=category_name)
            if created:
                messages.success(request, f"La catégorie '{category_name}' a été ajoutée avec succès.")
            else:
                messages.info(request, f"La catégorie '{category_name}' existe déjà.")
        else:
            messages.error(request, "Veuillez entrer un nom valide pour la catégorie.")

        # Retourner à la page précédente avec les données du formulaire précédemment saisies
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)
    else:
        return redirect("reformulate_project")
