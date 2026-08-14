import pytest

from services import backup_notifications, email_service


def test_send_email_sends_message_using_configured_smtp(mocker):
    config = mocker.Mock(smtp_user="sender@example.com", smtp_pass="secret")
    mocker.patch("services.email_service.ConnectionConfig.load", return_value=config)
    create_context = mocker.patch("services.email_service.ssl.create_default_context")
    smtp = mocker.patch("services.email_service.smtplib.SMTP")
    server = smtp.return_value.__enter__.return_value

    email_service.send_email(
        "Asunto", "Contenido", ["one@example.com", "two@example.com"]
    )

    smtp.assert_called_once_with(email_service.smtp_server, email_service.smtp_port)
    server.ehlo.assert_called()
    server.starttls.assert_called_once_with(context=create_context.return_value)
    server.login.assert_called_once_with("sender@example.com", "secret")
    message = server.send_message.call_args.args[0]
    assert message["Subject"] == "Asunto"
    assert message["From"] == "sender@example.com"
    assert message["To"] == "one@example.com, two@example.com"
    assert message.get_content().strip() == "Contenido"


def test_send_email_returns_without_recipients(mocker):
    load_config = mocker.patch("services.email_service.ConnectionConfig.load")
    smtp = mocker.patch("services.email_service.smtplib.SMTP")

    result = email_service.send_email("Asunto", "Contenido", [])

    assert result is None
    load_config.assert_not_called()
    smtp.assert_not_called()


def test_send_email_requires_smtp_credentials(mocker):
    config = mocker.Mock(smtp_user="", smtp_pass="")
    mocker.patch("services.email_service.ConnectionConfig.load", return_value=config)
    smtp = mocker.patch("services.email_service.smtplib.SMTP")

    with pytest.raises(ValueError, match="credenciales SMTP"):
        email_service.send_email("Asunto", "Contenido", ["to@example.com"])

    smtp.assert_not_called()


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, []),
        (["one@example.com"], ["one@example.com"]),
        (
            ("one@example.com", "two@example.com"),
            ["one@example.com", "two@example.com"],
        ),
        (" one@example.com, two@example.com ", ["one@example.com", "two@example.com"]),
    ],
)
def test_ensure_list_normalizes_recipient_values(value, expected):
    assert backup_notifications._ensure_list(value) == expected


def test_send_backup_notification_does_nothing_when_email_is_disabled(mocker):
    config = mocker.Mock(email_enabled=False)
    mocker.patch(
        "services.backup_notifications.ConnectionConfig.load", return_value=config
    )
    send_email = mocker.patch("services.backup_notifications.send_email")

    backup_notifications.send_backup_notification("Ventas")

    send_email.assert_not_called()


def test_send_backup_notification_sends_success_message(mocker):
    config = mocker.Mock(email_enabled=True, email_ok="ok@example.com, ops@example.com")
    mocker.patch(
        "services.backup_notifications.ConnectionConfig.load", return_value=config
    )
    send_email = mocker.patch("services.backup_notifications.send_email")

    backup_notifications.send_backup_notification(
        "Ventas", backup_path="C:/backups/ventas.bak"
    )

    send_email.assert_called_once_with(
        "Backup completado correctamente",
        "El backup de la base de datos 'Ventas' se ha completado correctamente."
        "\n\nRuta del backup: C:/backups/ventas.bak",
        ["ok@example.com", "ops@example.com"],
    )


def test_send_backup_notification_sends_error_message(mocker):
    config = mocker.Mock(email_enabled=True, email_err=["alerts@example.com"])
    mocker.patch(
        "services.backup_notifications.ConnectionConfig.load", return_value=config
    )
    send_email = mocker.patch("services.backup_notifications.send_email")

    backup_notifications.send_backup_notification(
        "Ventas", success=False, error_message="Espacio insuficiente"
    )

    send_email.assert_called_once_with(
        "Error en el backup",
        "Se ha producido un error durante el backup de la base de datos 'Ventas'."
        "\n\nMensaje de error: Espacio insuficiente",
        ["alerts@example.com"],
    )
