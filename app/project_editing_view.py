from django.shortcuts import render, redirect, get_object_or_404
from app.models import Project, ValidatedProject

from django.utils import timezone
from django.contrib import messages
from .forms import ValidatedProjectForm
from django.views.decorators.http import require_POST
from app.utils.mailing import send_report_mail_on_project


def detail_project(request,uid):
    project = get_object_or_404(Project, uid=uid)
    return render(request,"app/project/detail.html", {'project':project})


def reformulate_project(request, uid):
    project = get_object_or_404(Project, uid=uid)
    validated_project, created = ValidatedProject.objects.get_or_create(project=project)

    if request.method == "POST":
        form = ValidatedProjectForm(request.POST, request.FILES, instance=validated_project)
        if form.is_valid():
            validated_project = form.save(commit=False)
            validated_project.reformulated_by = request.user
            validated_project.approved_at = timezone.now() if validated_project.is_approved else None
            validated_project.save()
            project.status = "reformulated"
            project.save()
            
            html_path = "app/mailing/reformulated_project_mail.html"
            subject = f"Reformulatiion du projet {project.title}"
            user = project.user
            #envoie du mail
            send_report_mail_on_project(user,subject,html_path)
            messages.success(request,f"le projet {project.title} a été reformulé avec succès")
            messages.success(request, "Un mail de retour a été envoyé au soumetteur de projet pour l'informé de l'état actuel de son projet")
            return redirect("cabinet-incoming")
        else:
            messages.error(request, f"Veuillez corriger les erreurs du formulaire. {form.errors}")
    else:
        form = ValidatedProjectForm(instance=validated_project)

    context = {"form": form, "project": project}
    return render(request, "app/project/reformulate.html", context)



# def reject_project(request):
#     pass


def accepte_project(request, uid):
    project = get_object_or_404(Project, uid=uid)
    project.status = "accepted"
    project.save()
    
    html_path = "app/mailing/accept_project_mail.html"
    subject = f"Acceptation du projet {project.title}"
    user = project.user
    #envoie du mail
    send_report_mail_on_project(user,subject,html_path)
    messages.success(request,f"le projet {project.title} a été accepté avec succès")
    messages.success(request, "Un mail de retour a été envoyé au soumetteur de projet pour l'informé de l'état actuel de son projet")
    return redirect('cabinet-incoming')

@require_POST
def publish_project(request, uid):
    # Récupérer le projet et sa validation associée
    project = get_object_or_404(Project, uid=uid)
    validated_project = get_object_or_404(ValidatedProject, project=project)
    # Vérifier si la case "is_published" a été cochée
    is_published = request.POST.get("is_published") == "on"

    if validated_project.is_approved != is_published:  # Vérifier si un changement est nécessaire
        validated_project.is_approved = is_published
        if is_published:
            project.status = "published"  # Mettre à jour le statut du projet
            #envoie du mail
            html_path = "app/mailing/published_project_mail.html"
            subject = f"Publication du projet {project.title}"
            user = project.user
            send_report_mail_on_project(user,subject,html_path)
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
    project.status = "rejected"
    project.save()
    
    html_path = "app/mailing/rejected_project_mail.html"
    subject = f"Rejet du projet {project.title}"
    user = project.user
    send_report_mail_on_project(user,subject,html_path)
    messages.success(request, f"Le projet '{project.title}' a été rejeté avec succès.")
    messages.success(request, "Un mail de retour a été envoyé au soumetteur de projet pour l'informé de l'état actuel de son projet")
            
    return redirect('cabinet-incoming')