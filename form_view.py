# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(560, 569)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icon.fw.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("")
        self.isGameLocated = QtWidgets.QLabel(Form)
        self.isGameLocated.setGeometry(QtCore.QRect(10, 181, 261, 16))
        self.isGameLocated.setObjectName("isGameLocated")
        self.display = QtWidgets.QLabel(Form)
        self.display.setGeometry(QtCore.QRect(10, 200, 251, 251))
        self.display.setText("")
        self.display.setPixmap(QtGui.QPixmap("resources/gridTemplate.png"))
        self.display.setScaledContents(True)
        self.display.setWordWrap(False)
        self.display.setObjectName("display")
        self.commandsBox = QtWidgets.QGroupBox(Form)
        self.commandsBox.setGeometry(QtCore.QRect(270, 190, 281, 261))
        self.commandsBox.setObjectName("commandsBox")
        self.inputWord = QtWidgets.QPushButton(self.commandsBox)
        self.inputWord.setGeometry(QtCore.QRect(10, 30, 261, 23))
        self.inputWord.setObjectName("inputWord")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 541, 168))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.logoLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.logoLayout.setContentsMargins(0, 0, 0, 0)
        self.logoLayout.setObjectName("logoLayout")
        self.logo = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setAutoFillBackground(False)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("resources/logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.logoLayout.addWidget(self.logo)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyLex"))
        self.isGameLocated.setText(_translate("Form", "Bookworm Adventures is not located!"))
        self.commandsBox.setTitle(_translate("Form", "Commands"))
        self.inputWord.setText(_translate("Form", "Input Word"))


