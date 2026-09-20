"""Envoi des emails de rappel via Gmail SMTP."""
import smtplib
from email.message import EmailMessage
from nour import config


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
