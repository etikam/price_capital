from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()



def send_success_submision_project_mail(user,context):
        # Charger le sujet et le message HTML
        subject = "Accusé de réception – Projet soumis"
        html_path = "app/mailing/success_submission_mail.html"
        html_message = render_to_string(html_path,context)

    # Envoi de l'email
        send_mail(
            subject=subject,
            message="Succes de soumission de projet",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
            html_message=html_message, 
        )


def send_report_mail_on_project(user, subject,html_path,context):
        html_message = render_to_string(html_path,context)
        # Envoi de l'email
        send_mail(
            subject=subject,
            message=subject,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
            html_message=html_message, 
        )


def send_report_mail_to_superusers(subject, html_path, context):
    super_users = User.objects.filter(is_superuser=True)
    recipient_list = [user.email for user in super_users if user.email]
    if recipient_list:
        html_message = render_to_string(html_path, context)
        send_mail(
            subject=subject,
            message=subject,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True,
            html_message=html_message,
        )