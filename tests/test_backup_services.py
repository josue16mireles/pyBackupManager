from pathlib import Path
from unittest.mock import MagicMock

import pytest

from services.backup_service import BackupService


@pytest.fixture
def config():
    config = MagicMock()
    config.connection_string.return_value = "CONNECTION_STRING"
    config.selected_databases = ["ventas", "inventario"]
    config.selected_path = "C:/backups"
    return config


@pytest.fixture
def service(config):
    return BackupService(config)


def test_quote_identifier_escapes_closing_brackets():
    assert BackupService._quote_identifier("base]datos") == "[base]]datos]"


def test_create_backup_path_creates_temp_directory_and_uses_database_name(
    service, mocker, tmp_path
):
    service.Temp_Backup_Directory = tmp_path / "temp"
    mocker.patch(
        "services.backup_service.datetime"
    ).now.return_value.astimezone.return_value.strftime.return_value = "20260817_123456"

    result = service._create_backup_path("ventas")

    assert result == tmp_path / "temp" / "ventas_20260817_123456.bak"
    assert service.Temp_Backup_Directory.is_dir()


def test_wait_for_file_release_returns_when_file_can_be_opened(service, tmp_path):
    backup_path = tmp_path / "backup.bak"
    backup_path.write_bytes(b"backup")

    service._wait_for_file_release(backup_path, timeout_seconds=1, retry_delay=0)


def test_wait_for_file_release_retries_after_permission_error(
    service, mocker, tmp_path
):
    backup_path = tmp_path / "backup.bak"
    open_mock = mocker.patch.object(
        Path, "open", side_effect=[PermissionError, MagicMock()]
    )
    mocker.patch("services.backup_service.time.monotonic", side_effect=[0, 0.2])
    sleep_mock = mocker.patch("services.backup_service.time.sleep")

    service._wait_for_file_release(backup_path, timeout_seconds=1, retry_delay=0.5)

    assert open_mock.call_count == 2
    sleep_mock.assert_called_once_with(0.5)


def test_wait_for_file_release_raises_timeout_when_file_remains_locked(
    service, mocker, tmp_path
):
    backup_path = tmp_path / "backup.bak"
    mocker.patch.object(Path, "open", side_effect=PermissionError)
    mocker.patch("services.backup_service.time.monotonic", side_effect=[0, 60])
    sleep_mock = mocker.patch("services.backup_service.time.sleep")

    with pytest.raises(TimeoutError, match="permanecio bloqueado"):
        service._wait_for_file_release(backup_path, timeout_seconds=60)

    sleep_mock.assert_not_called()


def test_copy_to_destination_creates_directory_and_copies_file(
    service, mocker, tmp_path
):
    source = tmp_path / "temp" / "ventas.bak"
    source.parent.mkdir()
    source.write_bytes(b"backup")
    destination = tmp_path / "destination"
    destination.mkdir()
    service.config.selected_path = str(destination)
    copy_mock = mocker.patch("services.backup_service.copy2")

    result = service._copy_to_destination(source)

    assert result == destination / "ventas.bak"
    copy_mock.assert_called_once_with(source, destination / "ventas.bak")


def test_copy_to_destination_raises_when_local_destination_is_unavailable(
    service, mocker, tmp_path
):
    source = tmp_path / "ventas.bak"
    service.config.selected_path = str(tmp_path / "missing")
    copy_mock = mocker.patch("services.backup_service.copy2")

    with pytest.raises(FileNotFoundError, match="No se puede acceder"):
        service._copy_to_destination(source)

    copy_mock.assert_not_called()


def test_copy_to_destination_connects_and_disconnects_nas(service, mocker, tmp_path):
    source = tmp_path / "ventas.bak"
    destination = tmp_path / "destination"
    destination.mkdir()
    service.config.selected_path = r"\\server\share\backups"
    mocker.patch("services.backup_service.Path", return_value=destination)
    connect_mock = mocker.patch.object(service, "_connect_to_nas")
    disconnect_mock = mocker.patch.object(service, "_disconnect_from_nas")
    copy_mock = mocker.patch("services.backup_service.copy2")

    result = service._copy_to_destination(source)

    assert result == destination / source.name
    connect_mock.assert_called_once_with()
    disconnect_mock.assert_called_once_with()
    copy_mock.assert_called_once_with(source, destination / source.name)


def test_copy_to_destination_disconnects_nas_when_copy_fails(service, mocker, tmp_path):
    source = tmp_path / "ventas.bak"
    destination = tmp_path / "destination"
    destination.mkdir()
    service.config.selected_path = r"\\server\share\backups"
    mocker.patch("services.backup_service.Path", return_value=destination)
    mocker.patch.object(service, "_connect_to_nas")
    disconnect_mock = mocker.patch.object(service, "_disconnect_from_nas")
    mocker.patch("services.backup_service.copy2", side_effect=OSError("copy failed"))

    with pytest.raises(OSError, match="copy failed"):
        service._copy_to_destination(source)

    disconnect_mock.assert_called_once_with()


def test_connect_to_nas_requires_credentials(service):
    service.config.nas_user = ""
    service.config.nas_pass = ""

    with pytest.raises(ValueError, match="no est"):
        service._connect_to_nas()


def test_connect_to_nas_runs_net_use_command(service, mocker):
    service.config.selected_path = r"\\192.168.1.10\backups\sql"
    service.config.nas_user = "backup-user"
    service.config.nas_pass = "secret"
    run_mock = mocker.patch(
        "services.backup_service.subprocess.run",
        return_value=MagicMock(returncode=0),
    )

    service._connect_to_nas()

    run_mock.assert_called_once_with(
        ["net", "use", r"\\192.168.1.10\backups", "secret", "/user:backup-user"],
        capture_output=True,
        text=True,
        check=False,
    )


def test_connect_to_nas_raises_connection_error_with_command_output(service, mocker):
    service.config.selected_path = r"\\server\share\folder"
    service.config.nas_user = "user"
    service.config.nas_pass = "pass"
    mocker.patch(
        "services.backup_service.subprocess.run",
        return_value=MagicMock(returncode=1, stderr="access denied", stdout=""),
    )

    with pytest.raises(ConnectionError, match="access denied"):
        service._connect_to_nas()


def test_disconnect_from_nas_ignores_command_error_and_reports_it(
    service, mocker, capsys
):
    service.config.selected_path = r"\\server\share\folder"
    run_mock = mocker.patch(
        "services.backup_service.subprocess.run",
        return_value=MagicMock(returncode=1, stderr="network error", stdout=""),
    )

    service._disconnect_from_nas()

    run_mock.assert_called_once_with(
        ["net", "use", r"\\server\share", "/delete", "/y"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert "network error" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("configured_path", "expected"),
    [
        (r"\\server\share\folder", r"\\server\share"),
        (r"\\server\share", r"\\server\share"),
    ],
)
def test_get_nas_share_path_returns_server_and_share(
    service, configured_path, expected
):
    service.config.selected_path = configured_path

    assert service._get_nas_share_path() == expected


def test_get_nas_share_path_rejects_invalid_unc_path(service):
    service.config.selected_path = r"\\server"

    with pytest.raises(ValueError, match="formato UNC"):
        service._get_nas_share_path()


@pytest.mark.parametrize(
    ("configured_path", "expected"),
    [(r"\\server\share", True), ("C:/backups", False)],
)
def test_is_nas_path_identifies_unc_paths(service, configured_path, expected):
    service.config.selected_path = configured_path

    assert service._is_nas_path() is expected


def test_backup_database_executes_backup_copies_file_and_removes_temp(
    service, mocker, tmp_path
):
    backup_path = tmp_path / "ventas.bak"
    destination_path = tmp_path / "destination" / "ventas.bak"
    destination_path.parent.mkdir()
    destination_path.touch()
    cursor = MagicMock()
    cursor.nextset.side_effect = [True, False]
    connection = MagicMock()
    connection.cursor.return_value = cursor
    connect_mock = mocker.patch("services.backup_service.pyodbc.connect")
    connect_mock.return_value.__enter__.return_value = connection
    mocker.patch.object(service, "_create_backup_path", return_value=backup_path)
    wait_mock = mocker.patch.object(service, "_wait_for_file_release")
    copy_mock = mocker.patch.object(
        service, "_copy_to_destination", return_value=destination_path
    )
    unlink_mock = mocker.patch.object(Path, "unlink")

    result = service.backup_database("ventas]2026")

    assert result == str(destination_path)
    connect_mock.assert_called_once_with("CONNECTION_STRING", autocommit=True)
    assert "BACKUP DATABASE [ventas]]2026]" in cursor.execute.call_args.args[0]
    assert f"TO DISK = N'{backup_path}'" in cursor.execute.call_args.args[0]
    assert cursor.nextset.call_count == 2
    cursor.close.assert_called_once()
    wait_mock.assert_called_once_with(backup_path)
    copy_mock.assert_called_once_with(backup_path)
    unlink_mock.assert_called_once_with()


def test_backup_database_raises_when_destination_copy_does_not_exist(
    service, mocker, tmp_path
):
    backup_path = tmp_path / "ventas.bak"
    destination_path = tmp_path / "missing.bak"
    cursor = MagicMock()
    cursor.nextset.return_value = False
    connection = MagicMock()
    connection.cursor.return_value = cursor
    mocker.patch(
        "services.backup_service.pyodbc.connect"
    ).return_value.__enter__.return_value = connection
    mocker.patch.object(service, "_create_backup_path", return_value=backup_path)
    mocker.patch.object(service, "_wait_for_file_release")
    mocker.patch.object(service, "_copy_to_destination", return_value=destination_path)
    unlink_mock = mocker.patch.object(Path, "unlink")

    with pytest.raises(FileNotFoundError, match="destino final"):
        service.backup_database("ventas")

    cursor.close.assert_called_once()
    unlink_mock.assert_not_called()


def test_backup_database_closes_cursor_when_execution_fails(service, mocker, tmp_path):
    cursor = MagicMock()
    cursor.execute.side_effect = RuntimeError("SQL error")
    connection = MagicMock()
    connection.cursor.return_value = cursor
    mocker.patch(
        "services.backup_service.pyodbc.connect"
    ).return_value.__enter__.return_value = connection
    mocker.patch.object(
        service, "_create_backup_path", return_value=tmp_path / "ventas.bak"
    )

    with pytest.raises(RuntimeError, match="SQL error"):
        service.backup_database("ventas")

    cursor.close.assert_called_once()


def test_backup_all_returns_one_result_per_selected_database(service, mocker):
    backup_database = mocker.patch.object(
        service, "backup_database", side_effect=["ventas.bak", "inventario.bak"]
    )

    assert service.backup_all() == ["ventas.bak", "inventario.bak"]
    assert backup_database.call_args_list == [
        mocker.call("ventas"),
        mocker.call("inventario"),
    ]
