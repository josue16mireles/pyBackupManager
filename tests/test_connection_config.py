import json

from models.connection_config import ConnectionConfig


def test_connection_string():
    # arranque
    config = ConnectionConfig(
        server="192.168.1.100",
        user="sa",
        password="123456",
    )

    # Act
    connection_string = config.connection_string()

    # assert
    assert "SERVER=192.168.1.100;" in connection_string
    assert "UID=sa;" in connection_string
    assert "PWD=123456" in connection_string
    assert "DATABASE=master;" in connection_string
    assert "DRIVER={ODBC Driver 18 for SQL Server};" in connection_string


def test_default_values():
    config = ConnectionConfig()

    assert config.database == "master"
    assert config.driver == "ODBC Driver 18 for SQL Server"
    assert config.selected_databases == []
    assert config.schedule_enabled is False
    assert config.email_enabled is False


def test_custom_database_and_driver():
    config = ConnectionConfig(
        server="localhost",
        user="sa",
        password="123",
        database="Ventas",
        driver="ODBC Driver 17 for SQL Server",
    )

    connection_string = config.connection_string()

    assert "DATABASE=Ventas;" in connection_string
    assert "DRIVER={ODBC Driver 17 for SQL Server};" in connection_string


def test_save_connection_config(tmp_path, monkeypatch):
    config_file = tmp_path / "settings.json"

    monkeypatch.setattr("models.connection_config.CONFIG_FILE", config_file)
    config = ConnectionConfig(server="192.168.1.100", user="sa", password="123456")

    config.save()
    assert config_file.exists()


def test_save_connection_data(tmp_path, monkeypatch):

    config_file = tmp_path / "settings.json"

    monkeypatch.setattr("models.connection_config.CONFIG_FILE", config_file)

    config = ConnectionConfig(
        server="192.168.1.100", user="sa", password="123456", database="master"
    )

    config.save()

    data = json.loads(config_file.read_text())

    assert data["server"] == "192.168.1.100"
    assert data["user"] == "sa"
    assert data["database"] == "master"


def test_save_password_called(mocker):

    mock_save = mocker.patch("models.connection_config.save_password")

    config = ConnectionConfig(server="192.168.1.100", user="sa", password="123456")

    config.save()

    mock_save.assert_any_call("SQLBackupManager", "sa", "123456")
