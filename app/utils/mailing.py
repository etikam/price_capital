from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_success_submision_project_mail(user):
        # Charger le sujet et le message HTML
        subject = "Succes de soumission de projet"
        html_message = render_to_string("app/mailing/success_submission_mail.html")

    

        # Envoi de l'email
        send_mail(
            subject=subject,
            message="Succes de soumission de projet",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
            html_message=html_message, 
        )
        
        
        
