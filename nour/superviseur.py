"""Vérifie les horaires et envoie les rappels nécessaires."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from nour import config, etat
from nour.horaires import obtenir_horaires, PRIERES
from nour.messages import composer_rappel
from nour.envoi import envoyer_email


def verifier_et_envoyer() -> list:
    """
    Vérifie toutes les prières du jour et envoie les rappels manquants.

    Logique d'envoi : envoyer si l'heure de rappel (= prière - délai) est passée
    ET que la prière n'a pas encore eu lieu ET que le rappel n'a pas déjà été envoyé.

    Retourne la liste des prières dont le rappel vient d'être envoyé.
    """
    tz = ZoneInfo(config.DEFAULT_TIMEZONE)
    maintenant = datetime.now(tz)
    aujourd_hui = maintenant.date().isoformat()

    etat_du_jour = etat.charger_etat_du_jour(aujourd_hui)
    deja_envoyes = etat_du_jour['envoyes']
    timings = etat_du_jour['timings']

    # Premier lancement du jour : appel API unique, résultat mis en cache
    if not timings:
        donnees = obtenir_horaires(jour=maintenant.date())
        timings = donnees['timings']

    nouveaux = []

    for priere in PRIERES:
        if priere in deja_envoyes:
            continue

        heure_str = timings.get(priere)
        if not heure_str:
            continue

        h, m = map(int, heure_str.split(':'))
        heure_priere = maintenant.replace(hour=h, minute=m, second=0, microsecond=0)
        heure_rappel = heure_priere - timedelta(minutes=config.REMINDER_DELAY)

        # Fenêtre d'envoi : entre l'heure de rappel et l'heure de la prière
        if heure_rappel <= maintenant < heure_priere:
            # Minutes réellement restantes, arrondies aux 5 minutes les plus proches
            minutes_reelles = int((heure_priere - maintenant).total_seconds() / 60)
            minutes_msg = max(5, round(minutes_reelles / 5) * 5)

            message = composer_rappel(priere, heure_str, minutes_msg)
            resultat = envoyer_email(message['sujet'], message['corps'])

            if resultat['succes']:
                nouveaux.append(priere)
                print(f"[OK] Rappel {priere} ({heure_str}) — {minutes_reelles} min restantes.")
            else:
                print(f"[ERREUR] {priere} : {resultat['erreur']}")

    # Sauvegarder si les horaires viennent d'être récupérés ou si un rappel a été envoyé
    if nouveaux or not etat_du_jour['timings']:
        etat.enregistrer_etat(aujourd_hui, deja_envoyes + nouveaux, timings)

    return nouveaux
