"""
Brique 3 — test d'envoi réel.
Envoie UN email de rappel (Maghrib du jour) depuis l'adresse de Nour.
Lancer : python tester_envoi.py
"""
from datetime import date
from nour.horaires import obtenir_horaires, heures_de_rappel
from nour.messages import composer_rappel
from nour.envoi import envoyer_email
from nour.config import RECIPIENT_EMAIL, GMAIL_USER, REMINDER_DELAY


def main():
    print()
    print("Brique 3 — test d'envoi réel")
    print("-" * 45)

    try:
        donnees = obtenir_horaires()
    except Exception as e:
        print(f"Impossible de récupérer les horaires : {e}")
        return

    priere = 'Maghrib'
    heure  = donnees['timings'][priere]
    rappel = heures_de_rappel(donnees)[priere]

    message = composer_rappel(priere, heure, REMINDER_DELAY)

    print(f"Expéditeur   : {GMAIL_USER}")
    print(f"Destinataire : {RECIPIENT_EMAIL}")
    print(f"Prière test  : {priere} à {heure} — rappel prévu à {rappel}")
    print(f"(L'objet et le corps sont en arabe — vérifier le rendu dans la boîte)")
    print()
    print("Envoi en cours...")

    resultat = envoyer_email(message['sujet'], message['corps'])

    if resultat['succes']:
        print()
        print(f"Envoyé. Vérifie ta boîte {RECIPIENT_EMAIL}.")
        print("Si le message est dans les spams, marque-le comme 'Pas un spam'")
        print("pour que les suivants arrivent directement.")
    else:
        print()
        print(f"Echec : {resultat['erreur']}")

    print()


if __name__ == '__main__':
    main()
