# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'History.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(477, 550)
        self.tabl = QtWidgets.QTableView(Form)
        self.tabl.setGeometry(QtCore.QRect(10, 50, 451, 251))
        self.tabl.setObjectName("tabl")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(120, 10, 251, 31))
        self.label.setObjectName("label")
        self.Exit = QtWidgets.QPushButton(Form)
        self.Exit.setGeometry(QtCore.QRect(150, 500, 181, 31))
        self.Exit.setObjectName("Exit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 320, 471, 61))
        self.label_2.setObjectName("label_2")
        self.dela = QtWidgets.QPushButton(Form)
        self.dela.setGeometry(QtCore.QRect(10, 400, 181, 31))
        self.dela.setObjectName("dela")
        self.redac = QtWidgets.QPushButton(Form)
        self.redac.setGeometry(QtCore.QRect(250, 400, 201, 31))
        self.redac.setObjectName("redac")
        self.linetxt = QtWidgets.QLineEdit(Form)
        self.linetxt.setGeometry(QtCore.QRect(250, 440, 201, 31))
        self.linetxt.setObjectName("linetxt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">История дирректорий</span></p></body></html>"))
        self.Exit.setText(_translate("Form", "Назад"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">В 2 графе -  файл который был изменём</span></p><p><span style=\" font-size:14pt;\">В 3 графе - директория в которую он был сохранён</span></p></body></html>"))
        self.dela.setText(_translate("Form", "Удалить выбранный элемент"))
        self.redac.setText(_translate("Form", "Изменить выбранный элемент"))
        self.linetxt.setText(_translate("Form", "Введите новое название элементу:"))
