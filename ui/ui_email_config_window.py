# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'email_config_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QLabel,
    QLineEdit,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(333, 248)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(30, 200, 291, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        self.label = QLabel(Dialog)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(10, 100, 49, 16))
        self.txtUserEmail = QLineEdit(Dialog)
        self.txtUserEmail.setObjectName("txtUserEmail")
        self.txtUserEmail.setGeometry(QRect(10, 120, 311, 22))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(10, 150, 91, 16))
        self.txtPassEmail = QLineEdit(Dialog)
        self.txtPassEmail.setObjectName("txtPassEmail")
        self.txtPassEmail.setGeometry(QRect(10, 170, 311, 22))
        self.txtPassEmail.setEchoMode(QLineEdit.EchoMode.Password)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", "Usuario:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "Contrase\u00f1a:", None))
        self.txtPassEmail.setInputMask("")

    # retranslateUi
