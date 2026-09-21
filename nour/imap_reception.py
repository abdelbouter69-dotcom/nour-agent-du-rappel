"""Lecture des réponses IMAP et traitement des changements de ville."""
import imaplib
import email
import json
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from nour import config
from nour.envoi import envoyer_email
from nour.horaires import obtenir_horaires, PRIERES

_VILLES_PATH   = Path(__file__).parent / 'villes.json'
_POSITION_PATH = Path(__file__).parent.parent / 'etat' / 'position.json'


def _charger_villes() -> dict:
    with open(_VILLES_PATH, encoding='utf-8') as f:
        return json.load(f)


def _normaliser(texte: str) -> str:
    return unicodedata.normalize('NFD', texte).encode('ascii', 'ignore').decode().lower()


def _detecter_ville(corps: str, villes: dict) -> str | None:
    """Retourne le nom exact de la première ville trouvée dans le corps, ou None."""
    corps_norm = _normaliser(corps)
    for nom in villes:
        if _normaliser(nom) in corps_norm:
            return nom
    return None


def _extraire_corps(msg) -> str:
    """Extrait le texte brut du message (première partie text/plain)."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='replace')
        return ''
    payload = msg.get_payload(decode=True)
    return payload.decode('utf-8', errors='replace') if payload else ''


def _mettre_a_jour_position(nom: str, infos: dict) -> None:
    """Écrit etat/position.json et met à jour les variables config en mémoire."""
    _POSITION_PATH.parent.mkdir(exist_ok=True)
    with open(_POSITION_PATH, 'w', encoding='utf-8') as f:
        json.dump(
            {
                'ville':       nom,
                'lat':         infos['lat'],
                'lon':         infos['lon'],
                'pays':        infos['pays'],
                'fuseau':      infos['fuseau'],
                'mise_a_jour': datetime.now().isoformat(timespec='seconds'),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    # Propagation immédiate pour le run en cours
    config.DEFAULT_CITY      = nom
    config.DEFAULT_COUNTRY   = infos['pays']
    config.DEFAULT_LATITUDE  = float(infos['lat'])
    config.DEFAULT_LONGITUDE = float(infos['lon'])
    config.DEFAULT_TIMEZONE  = infos['fuseau']


def _prochain_rappel_non_envoye(infos: dict) -> tuple[str, str] | None:
    """
    Retourne (nom_priere, heure) du prochain rappel non encore parti aujourd'hui,
    calculé sur la nouvelle ville. None si toutes les prières sont passées.
    """
    from nour.etat import charger_etat_du_jour

    tz = ZoneInfo(infos['fuseau'])
    maintenant = datetime.now(tz)
    horaires = obtenir_horaires(lat=infos['lat'], lon=infos['lon'])
    etat = charger_etat_du_jour(maintenant.date().isoformat())

    for priere in PRIERES:
        if priere in etat['envoyes']:
            continue
        heure_str = horaires['timings'].get(priere)
        if not heure_str:
            continue
        h, m = map(int, heure_str.split(':'))
        heure_priere = maintenant.replace(hour=h, minute=m, second=0, microsecond=0)
        if heure_priere > maintenant:
            return priere, heure_str
    return None


def traiter_reponses() -> None:
    """
    Se connecte à Gmail IMAP, traite les réponses non lues venant du destinataire.
    Doit être appelée avant verifier_et_envoyer() pour que la nouvelle ville
    s'applique dès le rappel suivant du même run.
    """
    if not config.GMAIL_USER or not config.GMAIL_APP_PASSWORD or not config.RECIPIENT_EMAIL:
        return

    villes = _charger_villes()

    try:
        with imaplib.IMAP4_SSL('imap.gmail.com') as imap:
            imap.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
            print(f"[IMAP] Connecté en tant que {config.GMAIL_USER}")
            imap.select('INBOX')

            # Emails non lus envoyés par Abdelkader (= ses réponses)
            critere = f'(UNSEEN FROM "{config.RECIPIENT_EMAIL}")'
            _, nums = imap.search(None, critere)
            uids = nums[0].split()

            print(f"[IMAP] Emails non lus de {config.RECIPIENT_EMAIL} : {len(uids)}")

            for uid in uids:
                _, data = imap.fetch(uid, '(RFC822)')
                if not data or not data[0]:
                    continue

                msg = email.message_from_bytes(data[0][1])
                corps = _extraire_corps(msg)
                apercu = corps.strip()[:80].replace('\n', ' ')
                print(f"[IMAP] Email trouvé — début du corps : « {apercu} »")

                ville_trouvee = _detecter_ville(corps, villes)
                print(f"[IMAP] Ville détectée : {ville_trouvee!r}")

                if ville_trouvee:
                    infos = villes[ville_trouvee]
                    _mettre_a_jour_position(ville_trouvee, infos)

                    prochain = _prochain_rappel_non_envoye(infos)
                    if prochain:
                        nom_p, heure_p = prochain
                        ligne_rappel = f"Prochain rappel : {nom_p} à {heure_p}."
                    else:
                        ligne_rappel = "Toutes les prières du jour ont été rappelées."

                    envoyer_email(
                        sujet=f"Position mise à jour — {ville_trouvee}",
                        corps=(
                            "as-salāmu ʿalaykum wa raḥmatu Llāhi wa barakātuh\n\n"
                            f"Horaires calés sur {ville_trouvee}.\n"
                            f"{ligne_rappel}"
                        ),
                    )
                    print(f"[OK] Ville mise à jour : {ville_trouvee}")

                # Si aucune ville reconnue : ignore silencieusement (Phase 1)

                # Marque comme lu pour ne pas retraiter au prochain run
                imap.store(uid, '+FLAGS', '\\Seen')

    except imaplib.IMAP4.error as e:
        print(f"[ERREUR IMAP] {e}")
    except OSError as e:
        print(f"[ERREUR RÉSEAU IMAP] {e}")
