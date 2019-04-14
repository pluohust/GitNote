# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GitNote.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitNoteUi(object):
    def setupUi(self, GitNoteUi):
        GitNoteUi.setObjectName("GitNoteUi")
        GitNoteUi.resize(1028, 873)
        self.centralwidget = QtWidgets.QWidget(GitNoteUi)
        self.centralwidget.setObjectName("centralwidget")
        self.treeView_Notes = QtWidgets.QTreeView(self.centralwidget)
        self.treeView_Notes.setGeometry(QtCore.QRect(0, 0, 250, 1020))
        self.treeView_Notes.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeView_Notes.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeView_Notes.setObjectName("treeView_Notes")
        self.textEdit_Note = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_Note.setGeometry(QtCore.QRect(253, 0, 1660, 1020))
        self.textEdit_Note.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_Note.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_Note.setObjectName("textEdit_Note")
        GitNoteUi.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GitNoteUi)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1028, 28))
        self.menubar.setObjectName("menubar")
        self.menu_update = QtWidgets.QMenu(self.menubar)
        self.menu_update.setObjectName("menu_update")
        GitNoteUi.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu_update.menuAction())

        self.retranslateUi(GitNoteUi)
        QtCore.QMetaObject.connectSlotsByName(GitNoteUi)

    def retranslateUi(self, GitNoteUi):
        _translate = QtCore.QCoreApplication.translate
        GitNoteUi.setWindowTitle(_translate("GitNoteUi", "MainWindow"))
        self.menu_update.setTitle(_translate("GitNoteUi", "更新"))


