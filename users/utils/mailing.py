from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

#     send_mail(
#         subject, message,
#         'etiennedheleine2000@gmail.com',
#         [user.email],
#         fail_silently=True
#     )
#     return True
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# def send_activation_email(user):
#     subject = "Activation de votre compte"
#     uid = urlsafe_base64_encode(force_bytes(user.id))
#     token = default_token_generator.make_token(user)
#     message = render_to_string(
#         'registration/activation_email.html', {
#             'user': user,
#             'uid': uid,
#             'token': token,
#             'domain': settings.DOMAIN_URL
#         }
#     )


def send_activation_email(user):

    # Générer les variables nécessaires
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = (
        f"http://{settings.DOMAIN_URL}{reverse('auth:confirm_user_activation', kwargs={'uid': uid, 'token': token})}"
    )

    # Préparer le contexte pour le template
    context = {
        "user": user,
        "domain": settings.DOMAIN_URL,
        "uid": uid,
        "token": token,
        "activation_link": activation_link,
    }

    # Charger le sujet et le message HTML
    subject = "Activation de votre compte"
    html_message = render_to_string("registration/activation_email.html", context)

    # Ajouter un fallback en texte brut
    plain_message = (
        f"Bonjour {user.first_name},\n\n"
        f"Veuillez cliquer sur le lien suivant pour activer votre compte : {activation_link}\n"
    )

    # Envoi de l'email
    send_mail(
        subject,
        plain_message,  # Message texte brut pour fallback
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        html_message=html_message,  # Contenu HTML
    )


def send_password_reset_mail(user):
    # Générer les variables nécessaires
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"http://{settings.DOMAIN_URL}{reverse('auth:reset_password', kwargs={'uid': uid, 'token': token})}"

    # Préparer le contexte pour le template
    context = {
        "user": user,
        "domain": settings.DOMAIN_URL,
        "uid": uid,
        "token": token,
        "activation_link": reset_link,
    }

    # Charger le sujet et le message HTML
    subject = "Réinitialisation de mot de passe"
    html_message = render_to_string("registration/reset_password_email.html", context)

    # Envoi de l'email
    send_mail(
        subject,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=True,
        html_message=html_message,  # Contenu HTML
    )
