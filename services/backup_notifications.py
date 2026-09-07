from models.connection_config import ConnectionConfig

from .email_service import send_email


def _ensure_list(value):
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [s.strip() for s in str(value).split(",") if s.strip()]


def send_backup_notification(
    database, success=True, backup_path=None, error_message=None
):
    """
    Unified notification for backup success or failure.
    - If success=True uses config.email_ok and a success subject/body.
    - If success=False uses config.email_err and an error subject/body.
    """
    config = ConnectionConfig.load()
    if not config.email_enabled:
        return

    if success:
        recipients = _ensure_list(config.email_ok)
        subject = "Backup completado correctamente"
        body = f"El backup de la base de datos '{database}' se ha completado correctamente."
        if backup_path:
            body += f"\n\nRuta del backup: {backup_path}"
    else:
        recipients = _ensure_list(config.email_err)
        subject = "Error en el backup"
        body = f"Se ha producido un error durante el backup de la base de datos '{database}'."
        if error_message:
            body += f"\n\nMensaje de error: {error_message}"

    if not recipients:
        return

    send_email(subject, body, recipients)
