# helpers.py

from django.core.mail import send_mail

def informer_gagnant(gagnant):
    sujet = "Félicitations, vous avez gagné l'enchère !"
    message = f"Bonjour {gagnant.nom},\n\nVous avez gagné l'enchère pour l'article {gagnant.article.nom}.\n\nFélicitations !"
    expediteur = Customer.objects.get(pk=gagnant_id)
    destinataire = Customer.objects.get(pk=gagnant_id)
    send_mail(sujet, message, expediteur.email, destinataire.email, fail_silently=False)


