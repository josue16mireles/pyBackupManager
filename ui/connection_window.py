from database import check_connection
from models.connection_config import ConnectionConfig
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class ConnectionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Configación SQL Server")
        self.resize(420, 220)

        # layout principal
        mainLayout = QVBoxLayout()

        # formulario
        formLayout = QFormLayout()

        # Servidor
        self.server = QLineEdit()

        # Usuario
        self.user = QLineEdit()

        # Password
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        formLayout.addRow("Servidor/IP", self.server)
        formLayout.addRow("Usuario", self.user)
        formLayout.addRow("Contraseña", self.password)

        # Botones
        self.testButton = QPushButton("Probar conexión")
        self.saveButton = QPushButton("Aceptar")
        self.cancelButton = QPushButton("Cancelar")

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.testButton)
        buttonsLayout.addWidget(self.saveButton)
        buttonsLayout.addWidget(self.cancelButton)

        # Agregar layouts al principal
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)

        self.testButton.clicked.connect(self.check)
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.close)

        # cargar configuración previa
        self.load_config()

    def get_config(self) -> ConnectionConfig:

        return ConnectionConfig(
            server=self.server.text().strip(),
            user=self.user.text().strip(),
            password=self.password.text(),
        )

    def check(self):

        config = self.get_config()

        ok, message = check_connection(config)

        if ok:
            QMessageBox.information(self, "Conexión", message)
        else:
            QMessageBox.critical(self, "Error", message)

    def save(self):

        config = self.get_config()

        # guarda servidor y usuario
        config.save()

        QMessageBox.information(self, "Configuración", "Conexión guardada.")

        self.accept()

    def load_config(self):
        config = ConnectionConfig.load()

        self.server.setText(config.server)
        self.user.setText(config.user)
        self.password.setText(config.password)
