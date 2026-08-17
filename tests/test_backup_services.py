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
    mocker.patch("services.backup_service.datetime").now.return_value.astimezone.return_value.strftime.return_value = "20260817_123456"

    result = service._create_backup_path("ventas")

    assert result == tmp_path / "temp" / "ventas_20260817_123456.bak"
    assert service.Temp_Backup_Directory.is_dir()


def test_wait_for_file_release_returns_when_file_can_be_opened(service, tmp_path):
    backup_path = tmp_path / "backup.bak"
    backup_path.write_bytes(b"backup")

    service._wait_for_file_release(backup_path, timeout_seconds=1, retry_delay=0)


def test_wait_for_file_release_retries_after_permission_error(service, mocker, tmp_path):
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


def test_copy_to_destination_creates_directory_and_copies_file(service, mocker, tmp_path):
    source = tmp_path / "temp" / "ventas.bak"
    source.parent.mkdir()
    source.write_bytes(b"backup")
    destination = tmp_path / "destination"
    service.config.selected_path = str(destination)
    copy_mock = mocker.patch("services.backup_service.copy2")

    result = service._copy_to_destination(source)

    assert result == destination / "ventas.bak"
    assert destination.is_dir()
    copy_mock.assert_called_once_with(source, destination / "ventas.bak")


def test_backup_database_executes_backup_copies_file_and_removes_temp(service, mocker, tmp_path):
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
    copy_mock = mocker.patch.object(service, "_copy_to_destination", return_value=destination_path)
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


def test_backup_database_raises_when_destination_copy_does_not_exist(service, mocker, tmp_path):
    backup_path = tmp_path / "ventas.bak"
    destination_path = tmp_path / "missing.bak"
    cursor = MagicMock()
    cursor.nextset.return_value = False
    connection = MagicMock()
    connection.cursor.return_value = cursor
    mocker.patch("services.backup_service.pyodbc.connect").return_value.__enter__.return_value = connection
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
    mocker.patch("services.backup_service.pyodbc.connect").return_value.__enter__.return_value = connection
    mocker.patch.object(service, "_create_backup_path", return_value=tmp_path / "ventas.bak")

    with pytest.raises(RuntimeError, match="SQL error"):
        service.backup_database("ventas")

    cursor.close.assert_called_once()


def test_backup_all_returns_one_result_per_selected_database(service, mocker):
    backup_database = mocker.patch.object(
        service, "backup_database", side_effect=["ventas.bak", "inventario.bak"]
    )

    assert service.backup_all() == ["ventas.bak", "inventario.bak"]
    assert backup_database.call_args_list == [mocker.call("ventas"), mocker.call("inventario")]
