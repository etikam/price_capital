from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


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

#mail de rejet de projet
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
