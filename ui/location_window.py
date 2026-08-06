from models.connection_config import ConnectionConfig
from PySide6.QtWidgets import QDialog, QFileDialog

from ui.ui_location_window import Ui_Dialog

# from PySide6.QtGui import QIcon


class LocationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Ubicación de Backups")
        # self.setWindowIcon(QIcon("resources/icons/BkpIco.ico"))

        # Conectar eventos
        self.ui.btnExaminar.clicked.connect(self.select_folder)
        self.ui.buttonBox.accepted.connect(self.save)
        self.ui.buttonBox.rejected.connect(self.reject)

        # cargar configuracion previa
        config = ConnectionConfig.load()
        self.ui.txtRuta.setText(config.selected_path)
        self.ui.spBoxMeses.setValue(config.auto_delete_months)
        self.ui.spBoxDias.setValue(config.auto_delete_days)
        self.ui.txtUsuario.setText(config.nas_user)
        self.ui.txtPass.setText(config.nas_pass)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de backups")

        if folder:
            self.ui.txtRuta.setText(folder)

    def save(self):
        config = ConnectionConfig.load()
        config.selected_path = self.ui.txtRuta.text().strip()
        config.nas_user = self.ui.txtUsuario.text().strip()
        config.nas_pass = self.ui.txtPass.text()
        config.auto_delete_months = self.ui.spBoxMeses.value()
        config.auto_delete_days = self.ui.spBoxDias.value()
        config.save()
        self.accept()
