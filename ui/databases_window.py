from database import get_databases
from models.connection_config import ConnectionConfig
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

# from PySide6.QtGui import QIcon


class DatabasesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Selección Base de Datos")
        # self.setWindowIcon(QIcon("resources/icons/BkpIco.ico"))
        self.resize(420, 220)

        # layout principal
        layout = QVBoxLayout()

        label = QLabel("Seleccione las bases de datos que desea reslpaldar")
        layout.addWidget(label)

        # checkbox seleccionar todas
        self.chkAll = QCheckBox("Seleccionar todas")
        layout.addWidget(self.chkAll)

        # area scroll lista de DB
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.dbLayout = QVBoxLayout(container)
        self.dbLayout.setAlignment(Qt.AlignTop)

        scroll.setWidget(container)

        layout.addWidget(scroll)

        # botones
        btnLayout = QHBoxLayout()
        btnLayout.addStretch()

        self.savebtn = QPushButton("Guardar")
        self.cancelbtn = QPushButton("Cancelar")

        btnLayout.addWidget(self.savebtn)
        btnLayout.addWidget(self.cancelbtn)

        layout.addLayout(btnLayout)

        # lista para los chkBox
        self.databaseCheckboxes = []

        # carga bases de datos
        try:
            self.config = ConnectionConfig.load()
            databases = get_databases()
            self.load_databases(databases)
        except Exception as ex:
            print(ex)

        # eventos
        self.chkAll.toggled.connect(self.toggle_all)
        self.savebtn.clicked.connect(self.save)
        self.cancelbtn.clicked.connect(self.close)

        self.setLayout(layout)

    def load_databases(self, databases):
        """Carga la lista de bases de datos."""

        # Eliminar checkboxes existentes
        while self.dbLayout.count():
            item = self.dbLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.databaseCheckboxes.clear()

        # Crear un checkbox por cada BD
        for database in databases:
            checkbox = QCheckBox(database)
            if database in self.config.selected_databases:
                checkbox.setChecked(True)

            checkbox.stateChanged.connect(self.update_select_all)
            self.dbLayout.addWidget(checkbox)
            self.databaseCheckboxes.append(checkbox)

        self.update_select_all()

        self.dbLayout.addStretch()

    def toggle_all(self, checked):
        """Marca o desmarca todas las bases."""
        for checkbox in self.databaseCheckboxes:
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)

    def update_select_all(self):
        """Actualiza el estado del checkbox Seleccionar todas."""
        if not self.databaseCheckboxes:
            return

        all_checked = all(cb.isChecked() for cb in self.databaseCheckboxes)

        self.chkAll.blockSignals(True)
        self.chkAll.setChecked(all_checked)
        self.chkAll.blockSignals(False)

    def get_selected_databases(self):
        """Devuelve una lista con las bases seleccionadas."""
        return [cb.text() for cb in self.databaseCheckboxes if cb.isChecked()]

    # guarda la lista de las bases de datos seleccionadas
    def save(self):
        config = ConnectionConfig.load()
        config.selected_databases = self.get_selected_databases()
        config.save()
        self.accept()
