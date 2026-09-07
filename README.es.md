# SQL Backup Manager

SQL Backup Manager es una aplicación de escritorio desarrollada en Python con PySide6 para facilitar la ejecución de copias de seguridad de bases de datos SQL Server. La aplicación permite configurar conexiones, seleccionar bases de datos, definir rutas de destino, programar respaldos y enviar notificaciones por correo electrónico.

> Estado actual: esta aplicación se encuentra en desarrollo activo y actualmente en estado beta. Algunas funcionalidades pueden cambiar, mejorarse o requerir ajustes según el entorno de uso.

## ✨ Características principales

- Conexión a servidores SQL Server mediante ODBC.
- Selección de una o varias bases de datos para respaldar.
- Generación de archivos `.bak` con respaldo nativo de SQL Server.
- Guardado de respaldos en rutas locales o recursos compartidos NAS.
- Soporte para programación de copias de seguridad.
- Eliminación automática de backups antiguos según días o meses configurados.
- Notificaciones por correo electrónico para respaldos exitosos o fallidos.
- Almacenamiento seguro de credenciales mediante `keyring`.
- Interfaz gráfica construida con PySide6.

## 🧩 Stack tecnológico

- Python 3.x
- PySide6
- pyodbc
- SQL Server / ODBC Driver 18 for SQL Server
- keyring
- pytest

## 🛠️ Requisitos previos

Antes de ejecutar la aplicación debes tener instalado lo siguiente:

- Python 3.10 o superior
- SQL Server accesible desde la máquina donde corre la aplicación
- ODBC Driver 18 para SQL Server
- Windows (el proyecto está orientado a entornos Windows, por ejemplo para uso de `net use` con NAS)
- Dependencias del proyecto instaladas

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/sql-backup-manager.git
cd sql-backup-manager
```

2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Activa el entorno virtual:

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

Si usas herramientas de desarrollo y pruebas:

```bash
pip install -r requirements-dev.txt
```

## ▶️ Ejecución

Inicia la aplicación con:

```bash
python main.py
```

## ⚙️ Configuración

La aplicación permite configurar:

- Servidor SQL Server
- Usuario y contraseña de conexión
- Base de datos principal o selección múltiple de bases
- Ruta de destino de backup
- Credenciales para NAS compartido
- Programación automática de respaldos
- Notificación por correo electrónico

Las credenciales sensibles se almacenan en el sistema de claves del sistema operativo mediante `keyring`, en lugar de guardarse en texto plano dentro del archivo de configuración.

## 📁 Estructura del proyecto

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

## 🔐 Seguridad

Se recomienda:

- Usar cuentas con permisos adecuados para realizar backups de bases de datos.
- Mantener actualizado el controlador ODBC de SQL Server.
- Proteger el acceso físico o remoto a la máquina que ejecuta la aplicación.
- Revisar la configuración de NAS y correo antes de usarlo en producción.

## 🧪 Pruebas

El proyecto incluye pruebas automatizadas con `pytest`. Para ejecutarlas:

```bash
pytest
```

## 🚧 Nota sobre la versión beta

Actualmente la aplicación está en etapa beta, por lo que puede presentar:

- cambios en la interfaz o flujo de configuración,
- ajustes en la lógica de programación o limpieza automática,
- mejoras pendientes en validaciones y manejo de errores,
- compatibilidad específica con ciertos entornos de red o SQL Server.

Se recomienda probarla en entornos controlados antes de usarla en producción crítica.

## 🗺️ Roadmap sugerido

- Mejorar validaciones de configuración antes de iniciar un backup.
- Añadir registro de actividad y historial de respaldos.
- Mejorar la gestión de errores y mensajes del sistema.
- Añadir backup diferencial y transaccional.
- Mejorar la experiencia de usuario en la programación automática.
- Preparar una versión estable con documentación más profunda y despliegue controlado.

## 📄 Licencia

Este proyecto es de propósito interno. Consultar con el propietario para más detalles.

## 👨‍💻 Autor

Desarrollado por: **Josue Mireles** ([@josue16mireles](https://github.com/josue16mireles))  
*Última actualización: Septiembre 2026*