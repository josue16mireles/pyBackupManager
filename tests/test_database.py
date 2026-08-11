import pyodbc

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


# PROBAR LA CONFIGURACION CARGADA Y LLAMA A pyodbc.connect
def test_get_connection(mocker):
    mocker.patch("database.ConnectionConfig.load", return_value=config)

    mock_connect = mocker.patch("database.pyodbc.connect")

    get_connection()

    mock_connect.assert_called_once_with(config.connection_string())


# DEVUELVE LA CONEXION QUE OBTUVO DE pyodbc.connect
def test_get_connection_returns_connection(mocker):
    mocker.patch("database.ConnectionConfig.load", return_value=config)
    fake_connection = mocker.Mock()
    mocker.patch("database.pyodbc.connect", return_value=fake_connection)
    result = get_connection()
    assert result is fake_connection
