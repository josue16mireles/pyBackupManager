import logging
import smtplib
import ssl
from email.message import EmailMessage

from models.connection_config import ConnectionConfig

logger = logging.getLogger(__name__)

smtp_server = "smtp.mailgun.org"
smtp_port = 587


def send_email(subject, body, to_emails):
    if not to_emails:
        return

    config = ConnectionConfig.load()
    if not config.smtp_user or not config.smtp_pass:
        raise ValueError("Las credenciales SMTP no están configuradas.")

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = config.smtp_user
    msg["To"] = ", ".join(to_emails)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(config.smtp_user, config.smtp_pass)
            server.send_message(msg)
    except (smtplib.SMTPException, ssl.SSLError, OSError):
        logger.exception("Fallo el envío de correo")
