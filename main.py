"""
Briques 1 et 2 — affichage des horaires puis aperçu des messages.
Aucun email n'est envoyé.
Lancer : python main.py
"""
from datetime import date
from nour.horaires import obtenir_horaires, heures_de_rappel
from nour.messages import composer_rappel
from nour.config import DEFAULT_CITY, REMINDER_DELAY


def main():
    aujourd_hui = date.today()

    print()
    print("as-salamu alaykum")
    print(f"Date : {aujourd_hui.strftime('%d/%m/%Y')}   Lieu : {DEFAULT_CITY}")

    # --- Brique 1 : horaires ---
    print()
    print("BRIQUE 1 — Horaires du jour")
    print("-" * 56)

    try:
        donnees = obtenir_horaires()
    except FileNotFoundError as e:
        print(f"\nErreur : {e}")
        return
    except Exception as e:
        print(f"\nImpossible de récupérer les horaires : {e}")
        return

    source = "depuis le cache" if donnees['_source'] == 'cache' else "récupéré de l'API"
    rappels = heures_de_rappel(donnees)

    print(f"({source})\n")
    for priere, heure in donnees['timings'].items():
        print(f"  {priere:8}  {heure}   rappel à {rappels[priere]}  (-{REMINDER_DELAY} min)")

    # --- Brique 2 : aperçu des messages ---
    print()
    print("BRIQUE 2 — Aperçu des messages (tel qu'envoyé à l'heure du rappel)")
    print("=" * 56)

    for priere, heure in donnees['timings'].items():
        message = composer_rappel(
            priere=priere,
            heure_priere=heure,
            minutes_restantes=REMINDER_DELAY,
        )
        print(f"\n  Prière  : {priere}  (rappel à {rappels[priere]})")
        print(f"  Sujet   : {message['sujet']}")
        print(f"  ---")
        for ligne in message['corps'].splitlines():
            print(f"  {ligne}")
        print(f"  ---")

    print()
    print("Note : l'arabe peut s'afficher a l'envers dans ce terminal (probleme RTL/Windows).")
    print("Le contenu envoye par email sera correct. Valider en recevant un vrai email.")
    print()


if __name__ == '__main__':
    main()
