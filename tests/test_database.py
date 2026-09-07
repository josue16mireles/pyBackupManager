import pyodbc

import database
from database import check_connection, get_connection
from models.connection_config import ConnectionConfig

config = ConnectionConfig(server="192.168.1.100", user="sa", password="123456")


# LA PRUEBA COMPRUEBA LA LLAMADA A PYODBC.CONNECT
def test_connection_calls_pyodbc(mocker):
    connect_mock = mocker.patch("database.pyodbc.connect")

    check_connection(config)

    connect_mock.assert_called_once()


# LA PRUEBA VERIFICA LA CADENA DE CONEXION
def test_connection_string_used(mocker):
    connect_mock = mocker.patch("database.pyodbc.connect")

    expected = config.connection_string()
    check_connection(config)

    connect_mock.assert_called_once_with(expected, timeout=5)


# LA PRUEBA SIMULA UN ERROR, SE COMPORTA COMO SI SQL ESTUVIERA APAGADO
def test_connection_error(mocker):
    mocker.patch(
        "database.pyodbc.connect", side_effect=pyodbc.Error("No se pudo conectar")
    )
    result = check_connection(config)

    assert result == (False, "No se pudo conectar")


# CARGA LA CONFIGURACION Y USA SU CADENA AL CREAR LA CONEXION
def test_get_connection(mocker):
    load_mock = mocker.patch("database.ConnectionConfig.load", return_value=config)
    fake_connection = mocker.Mock()
    connect_mock = mocker.patch("database.pyodbc.connect", return_value=fake_connection)

    result = get_connection()

    load_mock.assert_called_once_with()
    connect_mock.assert_called_once_with(config.connection_string())
    assert result is fake_connection


def test_get_databases_executes_query_returns_names_and_closes_connection(mocker):
    connection = mocker.Mock()
    cursor = connection.cursor.return_value
    database_1 = mocker.Mock()
    database_1.name = "Database1"
    database_2 = mocker.Mock()
    database_2.name = "Database2"
    cursor.fetchall.return_value = [database_1, database_2]
    get_connection_mock = mocker.patch(
        "database.get_connection", return_value=connection
    )
    expected_query = (
        "SELECT name FROM sys.databases WHERE database_id > 4 AND state = 0 "
        "ORDER BY name;"
    )

    result = database.get_databases()

    get_connection_mock.assert_called_once_with()
    cursor.execute.assert_called_once_with(expected_query)
    assert result == ["Database1", "Database2"]
    connection.close.assert_called_once_with()
