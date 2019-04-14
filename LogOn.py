#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit
from LogOnUi import *
import main
import git

class LogOn(QWidget, Ui_LogOn):
    def __init__(self, parent=None):
        super(LogOn, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.show()
        
    def initUi(self):
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.pushButton_logOn.clicked.connect(self.logOn)

    def logOn(self):
        if len(self.lineEdit_userName.text()) < 2:
            QMessageBox.information(self, "警告", "请输入有效的用户名", QMessageBox.Ok)
            return
        if len(self.lineEdit_password.text()) < 2:
            QMessageBox.information(self, "警告", "请输入有效的密码", QMessageBox.Ok)
            return
        if (self.lineEdit_gitUrl.text())[-3:] != "git":
            QMessageBox.information(self, "警告", "请输入有效的Git地址", QMessageBox.Ok)
            return
        main.userName = self.lineEdit_userName.text()
        main.password = self.lineEdit_password.text()
        main.gitUrl = self.lineEdit_gitUrl.text()
        self.close()