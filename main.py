
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui.main_window import MainWindow


app = QApplication(sys.argv)

app.setWindowIcon(QIcon("resources/icons/BkpIco.ico"))
window = MainWindow()
window.show()

sys.exit(app.exec())