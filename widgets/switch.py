from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import (
    Qt,
    QRectF,
    QSize,
    Property,
    QPropertyAnimation
)
from PySide6.QtGui import(
    QPainter,
    QColor,
    QBrush
)

class Switch(QCheckBox):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setCursor(Qt.PointingHandCursor)

        self._offset = 2

        self._animation = QPropertyAnimation(self, b"offset")
        self._animation.setDuration(180)

        self.toggled.connect(self.animate)

    def sizeHint(self):
        return QSize(48, 24)

    def getOffset(self):
        return self._offset

    def setOffset(self, value):
        self._offset = value
        self.update()

    offset = Property(float, getOffset, setOffset)

    def animate(self, checked):

        if checked:
            self._animation.setStartValue(2)
            self._animation.setEndValue(26)
        else:
            self._animation.setStartValue(26)
            self._animation.setEndValue(2)

        self._animation.start()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(0, 0, self.width(), self.height())

        if self.isChecked():
            painter.setBrush(QColor("#4CAF50"))
        else:
            painter.setBrush(QColor("#BDBDBD"))

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 12, 12)

        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(self._offset, 2, 20, 20)