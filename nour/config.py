"""Lecture du fichier .env et exposition des réglages de Nour."""
import os
from pathlib import Path

_ROOT = Path(__file__).parent.parent


def _charger_env():
    env = _ROOT / '.env'
    if not env.exists():
        # Sur GitHub Actions, les variables viennent des secrets — pas d'erreur
        return
    with open(env, encoding='utf-8') as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne and not ligne.startswith('#') and '=' in ligne:
                cle, _, valeur = ligne.partition('=')
                os.environ.setdefault(cle.strip(), valeur.strip())


_charger_env()

# Gmail
GMAIL_USER         = os.environ.get('GMAIL_USER', '')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')
RECIPIENT_EMAIL    = os.environ.get('RECIPIENT_EMAIL', '')
SENDER_NAME        = os.environ.get('SENDER_NAME', 'Nour')
LANGUAGE           = os.environ.get('LANGUAGE', 'ar')

# Réglages API prière
PRAYER_CALC_METHOD      = os.environ.get('PRAYER_CALC_METHOD', '99')
PRAYER_METHOD_SETTINGS  = os.environ.get('PRAYER_METHOD_SETTINGS', '12,null,90 min')
PRAYER_SCHOOL           = os.environ.get('PRAYER_SCHOOL', '0')
PRAYER_TUNE             = os.environ.get('PRAYER_TUNE', '0,-3,0,4,-4,0,0,0,0')
REMINDER_DELAY          = int(os.environ.get('REMINDER_DELAY_MINUTES', '20'))

# Position par défaut
DEFAULT_LATITUDE    = float(os.environ.get('DEFAULT_LATITUDE', '45.9894'))
DEFAULT_LONGITUDE   = float(os.environ.get('DEFAULT_LONGITUDE', '4.7186'))
DEFAULT_CITY        = os.environ.get('DEFAULT_CITY', 'Villefranche-sur-Saone')
DEFAULT_COUNTRY     = os.environ.get('DEFAULT_COUNTRY', 'France')
DEFAULT_TIMEZONE    = os.environ.get('DEFAULT_TIMEZONE', 'Europe/Paris')

# Répertoire du cache
CACHE_DIR = _ROOT / 'cache'
CACHE_DIR.mkdir(exist_ok=True)
