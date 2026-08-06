from models.connection_config import ConnectionConfig
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from widgets.switch import Switch

from ui.connection_window import ConnectionWindow
from ui.databases_window import DatabasesWindow
from ui.location_window import LocationWindow
from ui.schedule_window import ScheduleWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SQL Backup Manager")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        self._create_server_section()
        self._create_database_section()
        self._create_backup_location_section()
        self._create_schedule_section()
        self._create_email_section()

        # se añaden los qframe a toplayout
        layout.addWidget(self.server_frame)
        layout.addWidget(self.database_frame)
        layout.addWidget(self.NAS_frame)
        layout.addWidget(self.schedule_frame)
        layout.addWidget(self.email_frame)

        central.setLayout(layout)

    def _create_server_section(self):
        # LAYOUT SERVER
        self.server_frame = QFrame()
        self.server_frame.setFrameShape(QFrame.StyledPanel)

        mainServerLayout = QVBoxLayout(self.server_frame)

        topLayout = QHBoxLayout()

        # Layout configuracion servidor
        serverIcon = QLabel()
        serverIcon.setPixmap(
            QPixmap("resources/icons/server.png").scaled(
                72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        topLayout.addWidget(serverIcon)

        self.connectionLabel = QLabel("Conectado al servidor: Sin configurar")
        self.connectionLabel.setStyleSheet("""
                    font-size: 14px;
                    font-weight: bold;
                """)
        topLayout.addWidget(self.connectionLabel)
        topLayout.addStretch()

        # boton configurar server
        self.connectionButton = self._create_icon_button_settings(
            "resources/icons/settings.png", self.openConnection
        )

        topLayout.addWidget(self.connectionButton)

        config = ConnectionConfig.load()
        if config.server:
            self.connectionLabel.setText(f"Conectado al servidor: {config.server}")
        else:
            self.connectionLabel.setText("Conectado al servidor: Sin configurar")

        mainServerLayout.addLayout(topLayout)

    # abre la ventana de configuracion de server
    def openConnection(self):
        dialog = ConnectionWindow(self)
        if dialog.exec():
            config = ConnectionConfig.load()

            self.connectionLabel.setText(f"Conectado al servidor: {config.server}")

    # SECCION SELECCION BASE DE DATOS
    def _create_database_section(self):
        # LAYOUT BASE DE DATOS
        self.database_frame = QFrame()
        self.database_frame.setFrameShape(QFrame.StyledPanel)

        mainDatabaseLayout = QVBoxLayout(self.database_frame)

        # primer fila
        headerLayout = QHBoxLayout()

        # icono base de datos
        database_icon = QLabel()
        database_icon.setPixmap(
            QPixmap("resources/icons/database.png").scaled(
                72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        headerLayout.addWidget(database_icon)

        self.database_label = QLabel("Bases de datos seleccionadas")
        self.database_label.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
            """)

        headerLayout.addWidget(self.database_label)

        headerLayout.addStretch()

        # boton seleccionar bases de datos
        self.database_config_button = self._create_icon_button_settings(
            "resources/icons/settings.png", self.open_database_config
        )

        headerLayout.addWidget(self.database_config_button)

        mainDatabaseLayout.addLayout(headerLayout)

        # segunda fila
        self.selected_databases_label = QLabel()
        self.selected_databases_label.setWordWrap(True)
        self.selected_databases_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.selected_databases_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.selected_databases_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        mainDatabaseLayout.addWidget(self.selected_databases_label)

        # cargar bases de datos previamente seleccionadas
        self.load_selected_databases()

    # abre la ventana para seleccionar bases de datos
    def open_database_config(self):
        dialog = DatabasesWindow(self)
        if dialog.exec():
            self.load_selected_databases()

    # actualiza la lista de las bases de datos seleccionadas
    def load_selected_databases(self):
        config = ConnectionConfig.load()

        if not config.selected_databases:
            self.selected_databases_label.clear()
            return
        self.selected_databases_label.setText(", ".join(config.selected_databases))

    # SECCION SELECCIONA LA UBICACION PARA GUARDAR BACKUPS
    def _create_backup_location_section(self):
        # LAYOUT UBICACION DONDE SE GUARDAN LOS BACKUPS
        self.NAS_frame = QFrame()
        self.NAS_frame.setFrameShape(QFrame.StyledPanel)

        mainNASLayout = QVBoxLayout(self.NAS_frame)

        # primer fila
        NASheaderLayout = QHBoxLayout()

        # icono base de datos
        NAS_icon = QLabel()
        NAS_icon.setPixmap(
            QPixmap("resources/icons/path.png").scaled(
                72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        NASheaderLayout.addWidget(NAS_icon)

        self.NAS_label = QLabel("Seleccione la ubicación donde desea guardar sus backups")
        self.NAS_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
        """)

        NASheaderLayout.addWidget(self.NAS_label)

        NASheaderLayout.addStretch()

        # boton seleccionar la ubicacion para guardar los backups
        self.NAS_config_button = self._create_icon_button_settings(
            "resources/icons/settings.png", self.open_NAS_config
        )

        NASheaderLayout.addWidget(self.NAS_config_button)

        mainNASLayout.addLayout(NASheaderLayout)

        # segunda fila
        self.selected_NAS_label = QLabel()
        self.selected_NAS_label.setWordWrap(False)

        self.selected_NAS_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        mainNASLayout.addWidget(self.selected_NAS_label)

        self.load_selected_NAS()

    # abre la ventana para seleccionar la ubicacion para guardar los backups
    def open_NAS_config(self):
        dialog = LocationWindow(self)
        if dialog.exec():
            self.load_selected_NAS()

    # actualiza la lista de las bases de datos seleccionadas
    def load_selected_NAS(self):
        config = ConnectionConfig.load()

        if not config.selected_path:
            self.selected_NAS_label.clear()
            return
        self.selected_NAS_label.setText(config.selected_path)

    # CREA SECCION SCHEDULE
    def _create_schedule_section(self):
        # LAYOUT PROGRAMACIÓN DE LOS BACKUPS
        self.schedule_frame = QFrame()
        self.schedule_frame.setFrameShape(QFrame.StyledPanel)

        mainScheduleLayout = QVBoxLayout(self.schedule_frame)

        # primer fila
        ScheduleheaderLayout = QHBoxLayout()

        # icono schedule
        Schedule_icon = QLabel()
        Schedule_icon.setPixmap(
            QPixmap("resources/icons/schedule.png").scaled(
                72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        ScheduleheaderLayout.addWidget(Schedule_icon)

        self.Schedule_label = QLabel("Programe un horario para sus backups")
        self.Schedule_label.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
            """)

        ScheduleheaderLayout.addWidget(self.Schedule_label)

        ScheduleheaderLayout.addStretch()

        # boton configurar schedule
        self.Schedule_config_button = self._create_icon_button_settings(
            "resources/icons/settings.png", self.open_Schedule_config
        )

        self.Schedule_config_button.setEnabled(False)

        ScheduleheaderLayout.addWidget(self.Schedule_config_button)

        mainScheduleLayout.addLayout(ScheduleheaderLayout)

        # Chk habilitar shcedule
        switchLayout = QHBoxLayout()

        self.schedule_switch = Switch()
        config = ConnectionConfig.load()
        self.schedule_switch.setChecked(config.schedule_enabled)

        switchLayout.addWidget(self.schedule_switch)
        switchLayout.addStretch()

        self.schedule_switch.toggled.connect(self.toggle_schedule)

        # Label de estado
        self.set_schedule_label = QLabel()
        self.set_schedule_label.setWordWrap(False)
        self.set_schedule_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        mainScheduleLayout.addLayout(switchLayout)

        # Actualiza la interfaz según el estado inicial
        self.toggle_schedule(self.schedule_switch.isChecked())

    def open_Schedule_config(self):
        dialog = ScheduleWindow(self)
        if dialog.exec():
            self.open_Schedule_window()

    def toggle_schedule(self, enabled):
        config = ConnectionConfig.load()
        config.schedule_enabled = enabled
        config.save()

        self.Schedule_config_button.setEnabled(enabled)

    def _create_icon_button_settings(self, icon_path, callback):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(64, 64))
        button.setFixedSize(64, 64)
        button.setFlat(True)
        button.setCursor(Qt.PointingHandCursor)

        button.clicked.connect(callback)
        return button

    # CREA SECCION email NOTIFICACIONES
    def _create_email_section(self):
        # LAYOUT email
        self.email_frame = QFrame()
        self.email_frame.setFrameShape(QFrame.StyledPanel)

        mainemailLayout = QVBoxLayout(self.email_frame)

        # primer fila
        emailheaderLayout = QHBoxLayout()

        # icono email
        email_icon = QLabel()
        email_icon.setPixmap(
            QPixmap("resources/icons/email.png").scaled(
                72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        emailheaderLayout.addWidget(email_icon)

        self.email_label = QLabel("Enviar notificaciones")
        self.email_label.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
            """)

        emailheaderLayout.addWidget(self.email_label)
        emailheaderLayout.addStretch()

        mainemailLayout.addLayout(emailheaderLayout)

        # Chk habilitar email
        switchLayout = QHBoxLayout()

        self.email_switch = Switch()
        config = ConnectionConfig.load()
        self.email_switch.setChecked(config.email_enabled)

        switchLayout.addWidget(self.email_switch)
        switchLayout.addStretch()

        self.email_switch.toggled.connect(self.toggle_email)

        # Label de estado
        self.set_email_label = QLabel()
        self.set_email_label.setWordWrap(False)
        self.set_email_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        mainemailLayout.addLayout(switchLayout)

        # notificaciones email
        self.email_fields = QWidget()
        emailfrm = QFormLayout(self.email_fields)

        # notificar si backup correcto
        self.BkpOk = QLineEdit()
        # notificar si backup fallo
        self.BkpErr = QLineEdit()

        emailfrm.addRow("Backup correcto notificar a:", self.BkpOk)
        emailfrm.addRow("Backup incorrecto notificar a:", self.BkpErr)
        self.btnsaveBkpOk_button = self._create_icon_button_settings(
            "resources/icons/save.png", lambda: self.save_email()
        )
        emailfrm.addWidget(self.btnsaveBkpOk_button)

        mainemailLayout.addWidget(self.email_fields)

        # Actualiza la interfaz según el estado inicial
        self.toggle_email(self.email_switch.isChecked())

    def toggle_email(self, enabled):
        config = ConnectionConfig.load()
        config.email_enabled = enabled
        config.email_ok = self.BkpOk.text().strip()
        config.email_err = self.BkpErr.text().strip()
        config.save()
        if hasattr(self, "email_fields"):
            self.email_fields.setEnabled(enabled)

    def save_email(self):
        config = ConnectionConfig.load()
        config.email_ok = self.BkpOk.text().strip()
        config.email_err = self.BkpErr.text().strip()
        config.save()
