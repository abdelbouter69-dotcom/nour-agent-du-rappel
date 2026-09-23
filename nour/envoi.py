"""Envoi des emails de rappel via Gmail SMTP.

Chaque email part en deux versions dans le même message :
  - texte brut (repli pour les messageries qui n'affichent pas le HTML) ;
  - HTML avec le logo de Nour en haut, lisible sur téléphone.
Le logo (nour/logo_email.png) est joint dans l'email lui-même : il s'affiche
sans rien télécharger d'Internet, y compris dans l'appli Gmail du portable.
"""
import html
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

from nour import config

_LOGO = Path(__file__).parent / 'logo_email.png'


def _corps_html(corps: str, cid_logo: str | None) -> str:
    """Met le texte en page : logo centré, gros caractères, sens automatique (arabe/français)."""
    paragraphes = [p for p in corps.split('\n') if p.strip()]
    lignes = ''.join(
        f'<p dir="auto" style="margin:0 0 14px 0;">{html.escape(p)}</p>'
        for p in paragraphes
    )
    logo = (
        f'<img src="cid:{cid_logo}" width="120" height="120" alt="نُور" '
        f'style="display:block;margin:0 auto 18px auto;width:120px;height:120px;border:0;">'
        if cid_logo else ''
    )
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="margin:0;padding:0;background:#faf8f3;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#faf8f3;">
<tr><td align="center" style="padding:20px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
       style="max-width:480px;background:#fbfbfb;border-radius:14px;border-top:4px solid #c9a24e;">
<tr><td style="padding:24px 20px;text-align:center;font-family:'Amiri','Traditional Arabic','Segoe UI',Tahoma,Arial,sans-serif;
               font-size:20px;line-height:1.9;color:#1f3a5f;">
{logo}{lignes}
</td></tr></table>
</td></tr></table>
</body></html>"""


def envoyer_email(sujet: str, corps: str) -> dict:
    """
    Envoie un email depuis le compte de Nour.

    Returns:
        {'succes': True, 'erreur': None}
        {'succes': False, 'erreur': str}
    """
    if not config.GMAIL_USER or not config.GMAIL_APP_PASSWORD:
        return {
            'succes': False,
            'erreur': 'GMAIL_USER ou GMAIL_APP_PASSWORD manquant dans .env',
        }

    msg = EmailMessage()
    msg['From']    = f"{config.SENDER_NAME} <{config.GMAIL_USER}>"
    msg['To']      = config.RECIPIENT_EMAIL
    msg['Subject'] = sujet
    msg.set_content(corps, charset='utf-8')

    # Version HTML avec logo — si le logo manque, l'email part quand même, sans image
    cid = make_msgid(domain='nour')[1:-1] if _LOGO.exists() else None
    msg.add_alternative(_corps_html(corps, cid), subtype='html', charset='utf-8')
    if cid:
        msg.get_payload()[1].add_related(
            _LOGO.read_bytes(), maintype='image', subtype='png', cid=f'<{cid}>',
            filename='nour.png', disposition='inline',
        )

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        return {'succes': True, 'erreur': None}

    except smtplib.SMTPAuthenticationError:
        return {
            'succes': False,
            'erreur': (
                'Authentification refusée. '
                'Vérifier GMAIL_USER et GMAIL_APP_PASSWORD dans .env — '
                'le mot de passe doit être le mot de passe d\'application '
                '(16 caractères), pas le mot de passe du compte Gmail.'
            ),
        }
    except smtplib.SMTPException as e:
        return {'succes': False, 'erreur': f'Erreur SMTP : {e}'}
    except OSError as e:
        return {'succes': False, 'erreur': f'Erreur réseau : {e}'}
