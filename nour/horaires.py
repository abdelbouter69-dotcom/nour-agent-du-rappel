"""Récupération et mise en cache des horaires de prière depuis AlAdhan."""
import json
import urllib.request
import urllib.parse
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from nour import config

PRIERES = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']


def _chemin_cache(jour: date, lat: float, lon: float) -> Path:
    return config.CACHE_DIR / f"horaires_{jour.isoformat()}_{lat}_{lon}.json"


def _depuis_api(jour: date, lat: float, lon: float) -> dict:
    date_str = jour.strftime('%d-%m-%Y')
    params = urllib.parse.urlencode({
        'latitude':      lat,
        'longitude':     lon,
        'method':        config.PRAYER_CALC_METHOD,
        'school':        config.PRAYER_SCHOOL,
        'methodSettings': config.PRAYER_METHOD_SETTINGS,
        'tune':          config.PRAYER_TUNE,
    })
    url = f"https://api.aladhan.com/v1/timings/{date_str}?{params}"

    with urllib.request.urlopen(url, timeout=15) as r:
        donnees = json.loads(r.read())

    if donnees.get('code') != 200:
        raise RuntimeError(
            f"L'API AlAdhan a répondu avec une erreur : {donnees.get('status', 'inconnue')}"
        )

    brut = donnees['data']['timings']
    return {p: brut[p][:5] for p in PRIERES if p in brut}


def obtenir_horaires(lat: float = None, lon: float = None, jour: date = None) -> dict:
    """
    Retourne les horaires du jour pour la position donnée.
    Lit depuis le cache si disponible, appelle l'API sinon.

    Retourne un dict :
      {
        'date':       'YYYY-MM-DD',
        'latitude':   float,
        'longitude':  float,
        'fetched_at': 'YYYY-MM-DDTHH:MM:SS',
        'timings':    {'Fajr': 'HH:MM', 'Dhuhr': ..., ...},
        '_source':    'cache' | 'api'
      }
    """
    lat  = lat  if lat  is not None else config.DEFAULT_LATITUDE
    lon  = lon  if lon  is not None else config.DEFAULT_LONGITUDE
    if jour is None:
        jour = datetime.now(ZoneInfo(config.DEFAULT_TIMEZONE)).date()

    cache = _chemin_cache(jour, lat, lon)

    if cache.exists():
        with open(cache, encoding='utf-8') as f:
            payload = json.load(f)
        payload['_source'] = 'cache'
        return payload

    horaires = _depuis_api(jour, lat, lon)
    payload = {
        'date':       jour.isoformat(),
        'latitude':   lat,
        'longitude':  lon,
        'fetched_at': datetime.now(ZoneInfo(config.DEFAULT_TIMEZONE)).isoformat(timespec='seconds'),
        'timings':    horaires,
    }
    with open(cache, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    payload['_source'] = 'api'
    return payload


def heures_de_rappel(horaires: dict, delai: int = None) -> dict:
    """
    Calcule l'heure d'envoi de chaque rappel (heure prière - délai en minutes).
    Retourne {'Fajr': 'HH:MM', ...}
    """
    delai = delai if delai is not None else config.REMINDER_DELAY
    resultat = {}
    for priere, heure in horaires['timings'].items():
        h, m = map(int, heure.split(':'))
        total = h * 60 + m - delai
        if total < 0:
            total += 24 * 60
        resultat[priere] = f"{total // 60:02d}:{total % 60:02d}"
    return resultat
