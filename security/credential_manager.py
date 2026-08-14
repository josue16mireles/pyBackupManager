import keyring

SQL_SERVICE = "SQLBackupManager"
NAS_SERVICE = "SQLBackupManagerNAS"
EMAIL_SERVICE = "SQLBackupManagerEmail"


def save_password(service: str, username: str, password: str):
    keyring.set_password(service, username, password)


def get_password(service: str, username: str):
    return keyring.get_password(service, username)


def delete_password(service: str, username: str):
    keyring.delete_password(service, username)
