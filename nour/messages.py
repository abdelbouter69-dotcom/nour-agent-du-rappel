"""
Composition des messages de rappel selon la recette skills/rappel_priere.md.
Langue principale : arabe vocalisé.

IMPORTANT : les textes arabes vivent dans nour/textes_ar.json.
Ne jamais les copier-coller depuis le terminal — l'affichage RTL y est inversé.
Éditer le fichier JSON directement et valider en envoyant un vrai email.
"""
import json
from pathlib import Path

_TEXTES_AR = json.loads(
    (Path(__file__).parent / 'textes_ar.json').read_text(encoding='utf-8')
)

# Textes français — maintenus ici, pas de problème d'affichage RTL
_TEXTES_FR = {
    'salutation': 'as-salāmu ʿalaykum wa raḥmatu Llāhi wa barakātuh',
    'corps':      'La prière de %(priere)s est à %(heure)s — dans %(minutes)s minutes.',
    'siwak':      'Pense au siwak et au parfum avant de prier.',
    'sujet':      '%(priere)s %(heure)s — dans %(minutes)s minutes',
}


def composer_rappel(
    priere: str,
    heure_priere: str,
    minutes_restantes: int,
    langue: str = 'ar',
) -> dict:
    """
    Compose un message de rappel selon la recette.

    Args:
        priere:            nom interne ('Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha')
        heure_priere:      heure au format 'HH:MM'
        minutes_restantes: minutes avant la prière au moment de l'envoi
        langue:            'ar' (défaut) ou 'fr'

    Returns:
        {'sujet': str, 'corps': str}
    """
    if langue == 'ar':
        t = _TEXTES_AR
        nom_priere = t['prieres'].get(priere, priere)
        # Repli : si le delai n'est pas dans textes_ar.json, on compose au moins
        # une phrase valide (nombre + daqiqatan) plutot qu'un chiffre nu.
        minutes_ar = t['minutes'].get(
            str(minutes_restantes),
            '%s \u062f\u064e\u0642\u0650\u064a\u0642\u064e\u0629\u064b' % minutes_restantes,
        )
        vals = {'nom_priere': nom_priere, 'heure': heure_priere, 'minutes_ar': minutes_ar}
        corps = '\n'.join([
            t['salutation'],
            '',
            t['corps'] % vals,
            '',
            t['siwak'],
        ])
        sujet = t['sujet'] % vals

    else:  # fr
        t = _TEXTES_FR
        heure_fr = heure_priere.replace(':', 'h')
        vals = {'priere': priere, 'heure': heure_fr, 'minutes': minutes_restantes}
        corps = '\n'.join([
            t['salutation'],
            '',
            t['corps'] % vals,
            '',
            t['siwak'],
        ])
        sujet = t['sujet'] % vals

    return {'sujet': sujet, 'corps': corps}
