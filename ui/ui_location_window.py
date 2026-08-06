# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'location_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(483, 338)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(130, 300, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 461, 281))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblRuta = QLabel(self.verticalLayoutWidget)
        self.lblRuta.setObjectName("lblRuta")

        self.horizontalLayout.addWidget(self.lblRuta)

        self.txtRuta = QLineEdit(self.verticalLayoutWidget)
        self.txtRuta.setObjectName("txtRuta")

        self.horizontalLayout.addWidget(self.txtRuta)

        self.btnExaminar = QPushButton(self.verticalLayoutWidget)
        self.btnExaminar.setObjectName("btnExaminar")

        self.horizontalLayout.addWidget(self.btnExaminar)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblConservar = QLabel(self.verticalLayoutWidget)
        self.lblConservar.setObjectName("lblConservar")

        self.horizontalLayout_2.addWidget(self.lblConservar)

        self.spBoxMeses = QSpinBox(self.verticalLayoutWidget)
        self.spBoxMeses.setObjectName("spBoxMeses")

        self.horizontalLayout_2.addWidget(self.spBoxMeses)

        self.lblMes = QLabel(self.verticalLayoutWidget)
        self.lblMes.setObjectName("lblMes")

        self.horizontalLayout_2.addWidget(self.lblMes)

        self.spBoxDias = QSpinBox(self.verticalLayoutWidget)
        self.spBoxDias.setObjectName("spBoxDias")

        self.horizontalLayout_2.addWidget(self.spBoxDias)

        self.lblDias = QLabel(self.verticalLayoutWidget)
        self.lblDias.setObjectName("lblDias")

        self.horizontalLayout_2.addWidget(self.lblDias)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.groupBox = QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QWidget(self.groupBox)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 10, 461, 80))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.txtUsuario = QLineEdit(self.gridLayoutWidget)
        self.txtUsuario.setObjectName("txtUsuario")

        self.gridLayout.addWidget(self.txtUsuario, 0, 1, 1, 1)

        self.txtPass = QLineEdit(self.gridLayoutWidget)
        self.txtPass.setObjectName("txtPass")

        self.gridLayout.addWidget(self.txtPass, 1, 1, 1, 1)

        self.lblUser = QLabel(self.gridLayoutWidget)
        self.lblUser.setObjectName("lblUser")

        self.gridLayout.addWidget(self.lblUser, 0, 0, 1, 1)

        self.lblPass = QLabel(self.gridLayoutWidget)
        self.lblPass.setObjectName("lblPass")

        self.gridLayout.addWidget(self.lblPass, 1, 0, 1, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.lblRuta.setText(QCoreApplication.translate("Dialog", "Ruta/NAS", None))
        self.btnExaminar.setText(QCoreApplication.translate("Dialog", "Examinar", None))
        self.lblConservar.setText(
            QCoreApplication.translate(
                "Dialog", "Eliminar backups anteriores despu\u00e9s de:", None
            )
        )
        self.lblMes.setText(QCoreApplication.translate("Dialog", "Meses", None))
        self.lblDias.setText(QCoreApplication.translate("Dialog", "D\u00edas", None))
        self.groupBox.setTitle(
            QCoreApplication.translate(
                "Dialog", "Configuraci\u00f3n avanzada NAS/Carpeta en red", None
            )
        )
        self.txtUsuario.setInputMask("")
        self.txtUsuario.setPlaceholderText("")
        self.txtPass.setInputMask("")
        self.txtPass.setPlaceholderText("")
        self.lblUser.setText(QCoreApplication.translate("Dialog", "Usuario", None))
        self.lblPass.setText(QCoreApplication.translate("Dialog", "Contrase\u00f1a", None))

    # retranslateUi
