from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QDateTime, QTime
from ui.ui_schedule_window import Ui_Dialog
from models.connection_config import ConnectionConfig
#from PySide6.QtGui import QIcon

class ScheduleWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Progamación de Backups")
        #self.setWindowIcon(QIcon("resources/icons/BkpIco.ico"))

        #conectar eventos
        self.ui.buttonBox.accepted.connect(self.save)
        self.ui.buttonBox.rejected.connect(self.reject)

        config = ConnectionConfig.load()
        self.ui.spHoras.setValue(config.schedule_hours)
        self.ui.spMin.setValue(config.schedule_minutes)
        self.ui.chkLun.setChecked(0 in config.schedule_days)
        self.ui.chkMar.setChecked(1 in config.schedule_days)
        self.ui.chkMie.setChecked(2 in config.schedule_days)
        self.ui.chkJue.setChecked(3 in config.schedule_days)
        self.ui.chkVie.setChecked(4 in config.schedule_days)
        self.ui.chkSab.setChecked(5 in config.schedule_days)
        self.ui.chkDom.setChecked(6 in config.schedule_days)

        if config.schedule_start:
            self.ui.dtInicia.setDateTime(
                QDateTime.fromString(
                    config.schedule_start,
                    Qt.ISODate
                )
            )
        else:
            tomorrow = QDateTime.currentDateTime().addDays(1)
            tomorrow.setTime(QTime(0,0))
            self.ui.dtInicia.setDateTime(tomorrow)

    def save(self):
        config = ConnectionConfig.load()
        config.schedule_hours = self.ui.spHoras.value()
        config.schedule_minutes = self.ui.spMin.value()
        dias = []
        if self.ui.chkLun.isChecked():
            dias.append(0)
        if self.ui.chkMar.isChecked():
            dias.append(1)
        if self.ui.chkMie.isChecked():
            dias.append(2) 
        if self.ui.chkJue.isChecked():
            dias.append(3)
        if self.ui.chkVie.isChecked():
            dias.append(4)
        if self.ui.chkSab.isChecked():
            dias.append(5) 
        if self.ui.chkDom.isChecked():
            dias.append(6)
        config.schedule_days = dias          
        config.schedule_start = (
            self.ui.dtInicia.dateTime().toPython().isoformat()
        )
        config.save()
        self.accept()