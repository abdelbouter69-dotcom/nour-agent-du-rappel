"""Persistance de l'état du jour : prières envoyées et horaires mis en cache."""
import json
from pathlib import Path

_ETAT_PATH = Path(__file__).parent.parent / 'etat' / 'journal.json'


def charger_etat_du_jour(date_str: str) -> dict:
    """
    Retourne l'état du jour sous la forme :
      {'envoyes': ['Fajr', ...], 'timings': {'Fajr': '06:13', ...}}
    Si le fichier est absent ou concerne un autre jour, retourne des listes vides.
    """
    if not _ETAT_PATH.exists():
        return {'envoyes': [], 'timings': {}}
    with open(_ETAT_PATH, encoding='utf-8') as f:
        etat = json.load(f)
    if etat.get('date') != date_str:
        return {'envoyes': [], 'timings': {}}
    return {
        'envoyes':  etat.get('envoyes', []),
        'timings':  etat.get('timings', {}),
    }


def enregistrer_etat(date_str: str, envoyes: list, timings: dict) -> None:
    """Sauvegarde l'état complet du jour (prières envoyées + horaires)."""
    _ETAT_PATH.parent.mkdir(exist_ok=True)
    with open(_ETAT_PATH, 'w', encoding='utf-8') as f:
        json.dump(
            {'date': date_str, 'envoyes': envoyes, 'timings': timings},
            f,
            ensure_ascii=False,
            indent=2,
        )
