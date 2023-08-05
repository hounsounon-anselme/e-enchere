# tasks.py

import datetime
from celery import shared_task
from zoomus import ZoomClient
from django.utils import timezone
from . import Product

@shared_task
def planifier_reunion_zoom():
    client = ZoomClient('votre_api_key', 'votre_api_secret')

    now = datetime.datetime.now()
    heure_debut = now + datetime.timedelta(minutes=1)
    heure_fin = heure_debut + datetime.timedelta(minutes=5)

    reponse = client.meeting.create(user_id='votre_user_id', start_time=heure_debut.strftime('%Y-%m-%dT%H:%M:%S'),
                                    duration=5, topic='Enchères', agenda='Nouvelle enchère en cours')

    if reponse.get('start_url'):
        url_reunion = reponse['start_url']
        nouvel_article = Product.objects.last()
        nouvel_article.url_reunion_zoom = url_reunion
        nouvel_article.save()
    else:
        # Gérer l'erreur si la réunion n'a pas été créée
        pass

@shared_task
def verifier_offres(article_id):
    article = Product.objects.get(pk=article_id)
    if article.date_fin_encheres < timezone.now() and not article.gagnant:
        # Trouver l'utilisateur avec l'offre la plus élevée
        gagnant = None
        offre_max = 0.0
        encheres = Enchere.objects.filter(article=article).order_by('-offre')
        for enchere in encheres:
            if enchere.offre > offre_max:
                offre_max = enchere.offre
                gagnant = enchere.utilisateur

        # Si un gagnant est trouvé, attribuer l'article à l'utilisateur
        if gagnant:
            article.gagnant = gagnant
            article.save()

        else:
            # Pas d'offre gagnante, redémarrer l'enchère
            demarrer_nouvelle_enchere()

        # Informer le gagnant par email ou tout autre moyen de notification
        informer_gagnant(gagnant)

@shared_task
def demarrer_nouvelle_enchere():
    nouvel_article = Product(
        nom='Article à vendre',
        description='Description de l\'article',
        prix_de_depart=10.0,
        date_debut_encheres=timezone.now(),
        date_fin_encheres=timezone.now() + datetime.timedelta(minutes=5)
    )
    nouvel_article.save()

    planifier_reunion_zoom()

