import pyodbc

from security.credential_manager import get_password
from models.connection_config import ConnectionConfig


def test_connection(config: ConnectionConfig):

    try:

        connection = pyodbc.connect(
            config.connection_string(),
            timeout=5
        )

        connection.close()

        return True, "Conexión exitosa."

    except Exception as ex:

        return False, str(ex)

def get_connection():
    config = ConnectionConfig.load()

    return pyodbc.connect(
        config.connection_string()
    )

#obtener las bases de datos
def get_databases():
    query = """SELECT name FROM sys.databases WHERE database_id > 4 AND state = 0 ORDER BY name;"""

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        return[row.name for row in cursor.fetchall()]
    finally:
        connection.close()