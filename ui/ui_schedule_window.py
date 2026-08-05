# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'schedule_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDateTimeEdit,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(484, 221)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(130, 180, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 0, 461, 51))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 5, 1, 1)

        self.spHoras = QSpinBox(self.gridLayoutWidget)
        self.spHoras.setObjectName(u"spHoras")

        self.gridLayout.addWidget(self.spHoras, 0, 2, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.spMin = QSpinBox(self.gridLayoutWidget)
        self.spMin.setObjectName(u"spMin")

        self.gridLayout.addWidget(self.spMin, 0, 4, 1, 1)

        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 50, 461, 71))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.grBoxDias = QGroupBox(self.verticalLayoutWidget)
        self.grBoxDias.setObjectName(u"grBoxDias")
        self.horizontalLayoutWidget = QWidget(self.grBoxDias)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(-1, 20, 488, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 0, 0, 0)
        self.chkLun = QCheckBox(self.horizontalLayoutWidget)
        self.chkLun.setObjectName(u"chkLun")

        self.horizontalLayout.addWidget(self.chkLun)

        self.chkMar = QCheckBox(self.horizontalLayoutWidget)
        self.chkMar.setObjectName(u"chkMar")

        self.horizontalLayout.addWidget(self.chkMar)

        self.chkMie = QCheckBox(self.horizontalLayoutWidget)
        self.chkMie.setObjectName(u"chkMie")

        self.horizontalLayout.addWidget(self.chkMie)

        self.chkJue = QCheckBox(self.horizontalLayoutWidget)
        self.chkJue.setObjectName(u"chkJue")

        self.horizontalLayout.addWidget(self.chkJue)

        self.chkVie = QCheckBox(self.horizontalLayoutWidget)
        self.chkVie.setObjectName(u"chkVie")

        self.horizontalLayout.addWidget(self.chkVie)

        self.chkSab = QCheckBox(self.horizontalLayoutWidget)
        self.chkSab.setObjectName(u"chkSab")

        self.horizontalLayout.addWidget(self.chkSab)

        self.chkDom = QCheckBox(self.horizontalLayoutWidget)
        self.chkDom.setObjectName(u"chkDom")

        self.horizontalLayout.addWidget(self.chkDom)


        self.verticalLayout.addWidget(self.grBoxDias)

        self.verticalLayoutWidget_2 = QWidget(Dialog)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 120, 461, 51))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.dtInicia = QDateTimeEdit(self.verticalLayoutWidget_2)
        self.dtInicia.setObjectName(u"dtInicia")
        self.dtInicia.setDateTime(QDateTime(QDate(2000, 1, 1), QTime(0, 0, 0)))
        self.dtInicia.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.dtInicia)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Hrs", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Min", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Cada", None))
        self.grBoxDias.setTitle(QCoreApplication.translate("Dialog", u"D\u00edas", None))
        self.chkLun.setText(QCoreApplication.translate("Dialog", u"L", None))
        self.chkMar.setText(QCoreApplication.translate("Dialog", u"M", None))
        self.chkMie.setText(QCoreApplication.translate("Dialog", u"M", None))
        self.chkJue.setText(QCoreApplication.translate("Dialog", u"J", None))
        self.chkVie.setText(QCoreApplication.translate("Dialog", u"V", None))
        self.chkSab.setText(QCoreApplication.translate("Dialog", u"S", None))
        self.chkDom.setText(QCoreApplication.translate("Dialog", u"D", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Iniciar el d\u00eda:", None))
    # retranslateUi

