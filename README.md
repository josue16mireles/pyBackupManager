# SQL Backup Manager

SQL Backup Manager is a desktop application developed in Python with PySide6 to simplify backing up SQL Server databases. The application allows users to configure database connections, select databases, define backup destinations, schedule backups, and send email notifications.

> Current status: this application is still under active development and is currently in beta. Some features may change, improve, or require adjustments depending on the environment in which it is used.

## ✨ Key Features

- Connection to SQL Server using ODBC.
- Selection of one or multiple databases to back up.
- Generation of `.bak` files using SQL Server native backup functionality.
- Storage of backups in local folders or NAS shared resources.
- Support for scheduled backup execution.
- Automatic cleanup of old backups based on days or months configured by the user.
- Email notifications for successful and failed backups.
- Secure credential storage using `keyring`.
- Graphical user interface built with PySide6.

## 🧩 Technology Stack

- Python 3.x
- PySide6
- pyodbc
- SQL Server / ODBC Driver 18 for SQL Server
- keyring
- pytest

## 🛠️ Requirements

Before running the application, make sure you have the following installed:

- Python 3.10 or higher
- SQL Server accessible from the machine where the app runs
- ODBC Driver 18 for SQL Server
- Windows (the project is oriented toward Windows environments, including `net use` for NAS resources)
- Project dependencies installed

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-user/sql-backup-manager.git
cd sql-backup-manager
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

If you are using development and testing tools:

```bash
pip install -r requirements-dev.txt
```

## ▶️ Running the Application

Start the application with:

```bash
python main.py
```

## ⚙️ Configuration

The application allows configuration for:

- SQL Server host
- Username and password for connection
- Primary database or multiple database selection
- Backup destination path
- NAS shared credentials
- Automated backup scheduling
- Email notifications

Sensitive credentials are stored in the operating system keychain using `keyring`, instead of being saved in plain text inside the configuration file.

## 📁 Project Structure

```text
pyBackupManager/
├── main.py
├── database.py
├── settings.json
├── requirements.txt
├── requirements-dev.txt
├── models/
│   └── connection_config.py
├── services/
│   ├── backup_service.py
│   ├── backup_notifications.py
│   └── email_service.py
├── security/
│   └── credential_manager.py
├── ui/
│   ├── connection_window.py
│   ├── databases_window.py
│   ├── email_config_window.py
│   ├── location_window.py
│   ├── main_window.py
│   └── schedule_window.py
├── interfaces/
│   ├── email_config_window.ui
│   ├── location_window.ui
│   └── schedule_window.ui
├── resources/
│   └── icons/
├── tests/
│   ├── test_backup_services.py
│   ├── test_connection_config.py
│   ├── test_database.py
│   └── test_email.py
├── widgets/
│   └── switch.py
└── README.md
```

## 🔐 Security Notes

It is recommended to:

- Use accounts with the appropriate permissions to perform database backups.
- Keep the SQL Server ODBC driver updated.
- Protect physical and remote access to the machine running the application.
- Review NAS and email settings before using the app in production environments.

## 🧪 Testing

The project includes automated tests with `pytest`. To run them:

```bash
pytest
```

## 🚧 Beta Version Note

The application is currently in beta, so it may present:

- changes in the user interface or configuration flow,
- adjustments in scheduling and automatic cleanup logic,
- pending improvements in validation and error handling,
- compatibility constraints in certain network or SQL Server environments.

It is recommended to test it in controlled environments before using it in critical production scenarios.

## 🗺️ Suggested Roadmap

- Improve configuration validation before starting a backup.
- Add activity logs and backup history.
- Improve system error handling and user messaging.
- Add differential and transactional backup support.
- Improve the automatic scheduling experience.
- Prepare a stable release with deeper documentation and controlled deployment.

## 📄 License

This project is intended for internal use. Please consult the owner for more details before distribution or reuse.

## 👨‍💻 Author

Developed by: **Josue Mireles** ([@josue16mireles](https://github.com/josue16mireles))  
*Last updated: September 2026*
