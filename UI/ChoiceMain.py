# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChoiceMain.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChoiceMain(object):
    def setupUi(self, ChoiceMain):
        ChoiceMain.setObjectName("ChoiceMain")
        ChoiceMain.resize(480, 289)
        self.ViborTxt = QtWidgets.QLabel(ChoiceMain)
        self.ViborTxt.setGeometry(QtCore.QRect(20, 0, 191, 31))
        self.ViborTxt.setObjectName("ViborTxt")
        self.Met3 = QtWidgets.QPushButton(ChoiceMain)
        self.Met3.setGeometry(QtCore.QRect(10, 90, 221, 31))
        self.Met3.setObjectName("Met3")
        self.Met4 = QtWidgets.QPushButton(ChoiceMain)
        self.Met4.setGeometry(QtCore.QRect(250, 90, 221, 31))
        self.Met4.setObjectName("Met4")
        self.Met2 = QtWidgets.QPushButton(ChoiceMain)
        self.Met2.setGeometry(QtCore.QRect(250, 50, 221, 31))
        self.Met2.setObjectName("Met2")
        self.Met1 = QtWidgets.QPushButton(ChoiceMain)
        self.Met1.setGeometry(QtCore.QRect(10, 50, 221, 31))
        self.Met1.setObjectName("Met1")
        self.Met6 = QtWidgets.QPushButton(ChoiceMain)
        self.Met6.setGeometry(QtCore.QRect(250, 130, 221, 31))
        self.Met6.setObjectName("Met6")
        self.Met5 = QtWidgets.QPushButton(ChoiceMain)
        self.Met5.setGeometry(QtCore.QRect(10, 130, 221, 31))
        self.Met5.setObjectName("Met5")
        self.Met7 = QtWidgets.QPushButton(ChoiceMain)
        self.Met7.setGeometry(QtCore.QRect(70, 180, 351, 41))
        self.Met7.setObjectName("Met7")
        self.Exit = QtWidgets.QPushButton(ChoiceMain)
        self.Exit.setGeometry(QtCore.QRect(190, 240, 101, 41))
        self.Exit.setObjectName("Exit")

        self.retranslateUi(ChoiceMain)
        QtCore.QMetaObject.connectSlotsByName(ChoiceMain)

    def retranslateUi(self, ChoiceMain):
        _translate = QtCore.QCoreApplication.translate
        ChoiceMain.setWindowTitle(_translate("ChoiceMain", "Form"))
        self.ViborTxt.setText(_translate("ChoiceMain", "<html><head/><body><p><span style=\" font-size:14pt;\">Выберете Действие:</span></p></body></html>"))
        self.Met3.setText(_translate("ChoiceMain", "3. Нахождение границ и их тиснение"))
        self.Met4.setText(_translate("ChoiceMain", "4. Скругление изображения"))
        self.Met2.setText(_translate("ChoiceMain", "2.    Общая настройка изображения"))
        self.Met1.setText(_translate("ChoiceMain", "1. Переворот изображения"))
        self.Met6.setText(_translate("ChoiceMain", "6. Наложение водяного знака"))
        self.Met5.setText(_translate("ChoiceMain", "5. Наложение текста на изображение"))
        self.Met7.setText(_translate("ChoiceMain", "7. Извлечение RGB каналов и изменение их последовательности"))
        self.Exit.setText(_translate("ChoiceMain", "Назад"))
