from models.connection_config import ConnectionConfig
from PySide6.QtWidgets import QDialog

from ui.ui_email_config_window import Ui_Dialog


class EmailWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Configuración de Email")

        # Conectar eventos
        self.ui.buttonBox.accepted.connect(self.save)
        self.ui.buttonBox.rejected.connect(self.reject)

        # cargar configuracion previa
        config = ConnectionConfig.load()
        self.ui.txtUserEmail.setText(config.smtp_user)
        self.ui.txtPassEmail.setText(config.smtp_pass)

    def save(self):
        config = ConnectionConfig.load()
        config.smtp_user = self.ui.txtUserEmail.text().strip()
        config.smtp_pass = self.ui.txtPassEmail.text()
        config.save()
        self.accept()
