import smtplib

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(1)  # Active les logs détaillés SMTP
    server.local_hostname = "localhost"  # Définir un nom d'hôte valide
    server.starttls()
    server.login("etiro2005@gmail.com", "votre_mot_de_passe_d_application")
    server.sendmail(
        "etiro2005@gmail.com",  # Expéditeur
        "etiennedheleine2000@gmail.com",  # Destinataire
        "Subject: Test Email\n\nCeci est un test direct via smtplib."
    )
    server.quit()
    print("Email envoyé avec succès via smtplib !")
except Exception as e:
    print(f"Erreur SMTP : {e}")
