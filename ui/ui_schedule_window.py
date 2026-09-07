# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'schedule_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QDate, QDateTime, QMetaObject, QRect, Qt, QTime
from PySide6.QtWidgets import (
    QCheckBox,
    QDateTimeEdit,
    QDialogButtonBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(484, 221)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(130, 180, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 0, 461, 51))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 0, 5, 1, 1)

        self.spHoras = QSpinBox(self.gridLayoutWidget)
        self.spHoras.setObjectName("spHoras")

        self.gridLayout.addWidget(self.spHoras, 0, 2, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.spMin = QSpinBox(self.gridLayoutWidget)
        self.spMin.setObjectName("spMin")

        self.gridLayout.addWidget(self.spMin, 0, 4, 1, 1)

        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 50, 461, 71))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.grBoxDias = QGroupBox(self.verticalLayoutWidget)
        self.grBoxDias.setObjectName("grBoxDias")
        self.horizontalLayoutWidget = QWidget(self.grBoxDias)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(-1, 20, 488, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 0, 0, 0)
        self.chkLun = QCheckBox(self.horizontalLayoutWidget)
        self.chkLun.setObjectName("chkLun")

        self.horizontalLayout.addWidget(self.chkLun)

        self.chkMar = QCheckBox(self.horizontalLayoutWidget)
        self.chkMar.setObjectName("chkMar")

        self.horizontalLayout.addWidget(self.chkMar)

        self.chkMie = QCheckBox(self.horizontalLayoutWidget)
        self.chkMie.setObjectName("chkMie")

        self.horizontalLayout.addWidget(self.chkMie)

        self.chkJue = QCheckBox(self.horizontalLayoutWidget)
        self.chkJue.setObjectName("chkJue")

        self.horizontalLayout.addWidget(self.chkJue)

        self.chkVie = QCheckBox(self.horizontalLayoutWidget)
        self.chkVie.setObjectName("chkVie")

        self.horizontalLayout.addWidget(self.chkVie)

        self.chkSab = QCheckBox(self.horizontalLayoutWidget)
        self.chkSab.setObjectName("chkSab")

        self.horizontalLayout.addWidget(self.chkSab)

        self.chkDom = QCheckBox(self.horizontalLayoutWidget)
        self.chkDom.setObjectName("chkDom")

        self.horizontalLayout.addWidget(self.chkDom)

        self.verticalLayout.addWidget(self.grBoxDias)

        self.verticalLayoutWidget_2 = QWidget(Dialog)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 120, 461, 51))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName("label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.dtInicia = QDateTimeEdit(self.verticalLayoutWidget_2)
        self.dtInicia.setObjectName("dtInicia")
        self.dtInicia.setDateTime(QDateTime(QDate(2000, 1, 1), QTime(0, 0, 0)))
        self.dtInicia.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.dtInicia)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", "Hrs", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "Min", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "Cada", None))
        self.grBoxDias.setTitle(QCoreApplication.translate("Dialog", "D\u00edas", None))
        self.chkLun.setText(QCoreApplication.translate("Dialog", "L", None))
        self.chkMar.setText(QCoreApplication.translate("Dialog", "M", None))
        self.chkMie.setText(QCoreApplication.translate("Dialog", "M", None))
        self.chkJue.setText(QCoreApplication.translate("Dialog", "J", None))
        self.chkVie.setText(QCoreApplication.translate("Dialog", "V", None))
        self.chkSab.setText(QCoreApplication.translate("Dialog", "S", None))
        self.chkDom.setText(QCoreApplication.translate("Dialog", "D", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", "Iniciar el d\u00eda:", None))

    # retranslateUi
