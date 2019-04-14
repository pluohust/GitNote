# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GitNote.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1041, 756)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.treeView_motes = QtWidgets.QTreeView(self.centralwidget)
        self.treeView_motes.setGeometry(QtCore.QRect(0, 0, 171, 731))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.treeView_motes.sizePolicy().hasHeightForWidth())
        self.treeView_motes.setSizePolicy(sizePolicy)
        self.treeView_motes.setAutoFillBackground(False)
        self.treeView_motes.setObjectName("treeView_motes")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1041, 28))
        self.menubar.setObjectName("menubar")
        self.menu_sync = QtWidgets.QMenu(self.menubar)
        self.menu_sync.setObjectName("menu_sync")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu_sync.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GitNote"))
        self.menu_sync.setTitle(_translate("MainWindow", "同步"))


