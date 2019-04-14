# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogOn.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LogOn(object):
    def setupUi(self, LogOn):
        LogOn.setObjectName("LogOn")
        LogOn.resize(388, 150)
        self.formLayout = QtWidgets.QFormLayout(LogOn)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(LogOn)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit_userName = QtWidgets.QLineEdit(LogOn)
        self.lineEdit_userName.setObjectName("lineEdit_userName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_userName)
        self.label_2 = QtWidgets.QLabel(LogOn)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_password = QtWidgets.QLineEdit(LogOn)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        self.label_3 = QtWidgets.QLabel(LogOn)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_gitUrl = QtWidgets.QLineEdit(LogOn)
        self.lineEdit_gitUrl.setObjectName("lineEdit_gitUrl")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_gitUrl)
        self.pushButton_logOn = QtWidgets.QPushButton(LogOn)
        self.pushButton_logOn.setObjectName("pushButton_logOn")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pushButton_logOn)

        self.retranslateUi(LogOn)
        QtCore.QMetaObject.connectSlotsByName(LogOn)

    def retranslateUi(self, LogOn):
        _translate = QtCore.QCoreApplication.translate
        LogOn.setWindowTitle(_translate("LogOn", "登录"))
        self.label.setText(_translate("LogOn", "用户名："))
        self.label_2.setText(_translate("LogOn", "密码："))
        self.label_3.setText(_translate("LogOn", "Git地址："))
        self.pushButton_logOn.setText(_translate("LogOn", "登录"))


