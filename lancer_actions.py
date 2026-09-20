"""
Point d'entrée pour GitHub Actions.
Lancer : python lancer_actions.py
"""
import sys
from nour.superviseur import verifier_et_envoyer


def main():
    envoyes = verifier_et_envoyer()
    if envoyes:
        print(f"Rappels envoyés : {', '.join(envoyes)}")
    else:
        print("Aucun rappel à envoyer pour ce créneau.")
    sys.exit(0)


if __name__ == '__main__':
    main()
