# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GitNote.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_note(object):
    def setupUi(self, Form_note):
        Form_note.setObjectName("Form_note")
        Form_note.resize(1105, 789)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form_note.sizePolicy().hasHeightForWidth())
        Form_note.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../.designer/backup/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form_note.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form_note)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_update = QtWidgets.QPushButton(Form_note)
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout.addWidget(self.pushButton_update)
        self.pushButton_create = QtWidgets.QPushButton(Form_note)
        self.pushButton_create.setObjectName("pushButton_create")
        self.horizontalLayout.addWidget(self.pushButton_create)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.splitter_2 = QtWidgets.QSplitter(Form_note)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.treeWidget_tree = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget_tree.setMinimumSize(QtCore.QSize(100, 0))
        self.treeWidget_tree.setMaximumSize(QtCore.QSize(200, 16777215))
        self.treeWidget_tree.setSizeIncrement(QtCore.QSize(250, 0))
        self.treeWidget_tree.setBaseSize(QtCore.QSize(250, 0))
        self.treeWidget_tree.setObjectName("treeWidget_tree")
        self.treeWidget_tree.headerItem().setText(0, "1")
        self.treeWidget_tree.header().setVisible(False)
        self.listWidget_list = QtWidgets.QListWidget(self.splitter)
        self.listWidget_list.setMinimumSize(QtCore.QSize(100, 0))
        self.listWidget_list.setMaximumSize(QtCore.QSize(150, 16777215))
        self.listWidget_list.setProperty("isWrapping", True)
        self.listWidget_list.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget_list.setObjectName("listWidget_list")
        self.widget = QtWidgets.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_save = QtWidgets.QPushButton(self.widget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_3.addWidget(self.pushButton_save)
        self.lineEdit_title = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_title.setReadOnly(True)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.horizontalLayout_3.addWidget(self.lineEdit_title)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.plainTextEdit_markdown = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit_markdown.setEnabled(True)
        self.plainTextEdit_markdown.setObjectName("plainTextEdit_markdown")
        self.horizontalLayout_2.addWidget(self.plainTextEdit_markdown)
        self.textEdit_show = QtWidgets.QTextEdit(self.widget)
        self.textEdit_show.setReadOnly(True)
        self.textEdit_show.setObjectName("textEdit_show")
        self.horizontalLayout_2.addWidget(self.textEdit_show)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.splitter_2)

        self.retranslateUi(Form_note)
        QtCore.QMetaObject.connectSlotsByName(Form_note)

    def retranslateUi(self, Form_note):
        _translate = QtCore.QCoreApplication.translate
        Form_note.setWindowTitle(_translate("Form_note", "笔记"))
        self.pushButton_update.setText(_translate("Form_note", "更新"))
        self.pushButton_create.setText(_translate("Form_note", "新建"))
        self.pushButton_save.setText(_translate("Form_note", "编辑"))


