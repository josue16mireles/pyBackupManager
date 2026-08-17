import time
from datetime import datetime
from pathlib import Path
from shutil import copy2

import pyodbc

from models.connection_config import ConnectionConfig


class BackupService:
    Temp_Backup_Directory = Path(r"C:\SQLBackupManager\temp")

    def __init__(self, config: ConnectionConfig):
        self.config = config

    def backup_database(self, database: str) -> str:
        """
        Realiza el backup de una base de datos
        Retorna la ruta del archivo .bak generado
        """

        backup_path = self._create_backup_path(database)
        connection_string = self.config.connection_string()

        with pyodbc.connect(connection_string, autocommit=True) as connection:
            cursor = connection.cursor()
            try:
                sql = f"""
                    BACKUP DATABASE {self._quote_identifier(database)} 
                    TO DISK = N'{backup_path}'
                    WITH INIT, STATS = 10
                """
                cursor.execute(sql)

                while cursor.nextset():
                    pass  # Esperamos a que termine el backup
            finally:
                cursor.close()

        self._wait_for_file_release(backup_path)
        # Verificamos que SQL Server realmente generó el archivo.
        destination_path = self._copy_to_destination(backup_path)

        # Verificamos que la copia existe.
        if not destination_path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo en el destino final: {destination_path}"
            )
        try:
            # Solo eliminamos el temporal cuando la copia fue exitosa.
            backup_path.unlink()
        except OSError as error:
            print(
                f"No se pudo eliminar el archivo temporal: {backup_path}. Error: {error}"
            )

        return str(destination_path)

    def _wait_for_file_release(
        self,
        backup_path: Path,
        timeout_seconds: int = 60,
        retry_delay: float = 1,
    ) -> None:  # Espera hasta que el archivo temporal pueda abrirse

        start_time = time.monotonic()

        while True:
            try:
                with backup_path.open("rb"):
                    return  # El archivo se puede abrir, salir del bucle
            except PermissionError:
                elapsed = time.monotonic() - start_time

                if elapsed >= timeout_seconds:
                    raise TimeoutError(
                        f"El archivo permanecio bloqueado durante "
                        f"{timeout_seconds} segundos: {backup_path}"
                    )
                print(
                    f"Esperando que SQLServer libere el archivo "
                    f"{elapsed:.1f}/{timeout_seconds}s)..."
                )
                time.sleep(retry_delay)

    def _create_backup_path(self, database: str) -> Path:
        """
        Crea la ruta del archivo .bak para el backup
        """

        self.Temp_Backup_Directory.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
        filename = f"{database}_{timestamp}.bak"

        return self.Temp_Backup_Directory / filename

    @staticmethod
    def _quote_identifier(value: str) -> str:
        """
        Escapa un identificador de SQL Server (como nombres de bases de datos o tablas)
        """
        return "[" + value.replace("]", "]]") + "]"

    def backup_all(self) -> list[str]:
        backup_files = []

        for database in self.config.selected_databases:
            backup_file = self.backup_database(database)
            backup_files.append(backup_file)

        return backup_files

    def _copy_to_destination(self, backup_path: Path) -> Path:
        """Copia el backup temporal al destino configurado"""
        destination_directory = Path(self.config.selected_path)
        destination_directory.mkdir(parents=True, exist_ok=True)

        destination_path = destination_directory / backup_path.name

        print(f"Copiando backup a: {destination_path}")

        copy2(backup_path, destination_path)

        return destination_path
