#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTreeWidgetItem, QListWidgetItem
from PyQt5.QtGui import QIcon, QColor, QBrush, QPalette, QColor
from PyQt5.QtCore import Qt
import GitNoteUi
import main
import git
import os, getpass, threading, time, operator
import markdown2

def runClone():
    main.setGitEnv()
    git.Repo.clone_from(url=main.gitUrl, to_path="/home/"+getpass.getuser()+"/.GitNote/Notes")
    #git.Git("/home/"+getpass.getuser()+"/.GitNote/Notes").clone(main.gitUrl)
    main.myGitNote.setUpdateBack()

def updateGit():
    main.myGitNote.setUpdateStatus()
    main.setGitEnv()
    repo = git.Repo("/home/"+getpass.getuser()+"/.GitNote/Notes")
    remote = repo.remote()
    #index = repo.index
    #index.add(u=True) # 
    #index.commit('note')
    repo.git.add('--all')
    repo.index.commit('note')
    remote.push()
    remote.pull()
    main.myGitNote.setUpdateBack()

class GitNote(QWidget, GitNoteUi.Ui_Form_note):
    def __init__(self, parent=None):
        super(GitNote, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.show()
        self.updateUiAfterShow()
        
    def initUi(self):
        if not main.gitExist:
            self.mycloneGit()
        self.pushButton_update.clicked.connect(self.myupdateGit)
        self.dirIcon = QIcon("dir.ico")
        self.addTopDirs()
        self.treeWidget_tree.expandAll()
        self.treeWidget_tree.clicked.connect(self.onTreeClicked)
        self.listWidget_list.setStyleSheet(
        "QListWidget::item { border-bottom: 0.5px dotted blue; margin-bottom:10px;}"
        "QListWidget::item:!selected{}"  
        "QListWidget::item:selected:active{background:#FFFFFF;color:#19649F;border-width:-1;}"  
        "QListWidget::item:selected{background:#FFFFFF;color:#19649F;}")
        self.listWidget_list.clicked.connect(self.clickedListView)
        #self.treeWidget_tree.addTopLevelItem(root)
        # set window background color
        self.setAutoFillBackground(True)
        pBack = self.palette()
        pBack.setColor(self.backgroundRole(), QColor(79, 79, 79))
        self.setPalette(pBack)
        self.listfileDir = ""
        self.plainTextEdit_markdown.hide()
        self.saveStatus = False
        self.pushButton_save.clicked.connect(self.clickedButtonSave)
    
    def clickedListView(self, qmodelindex):
        item = self.listWidget_list.currentItem()
        itemCount = item.text()
        filename = (itemCount.split("\n"))[0]
        filepath = os.path.join(self.listfileDir, filename)
        tmpf = open(filepath, "r")
        tmplines = tmpf.read()
        tmpf.close()
        self.textEdit_show.setText(markdown2.markdown(tmplines))
    
    def clickedButtonSave(self):
        if not self.saveStatus:
            self.saveStatus = True
            self.plainTextEdit_markdown.show()
            self.pushButton_save.setText("保存")
        else:
            self.saveStatus = False
            self.plainTextEdit_markdown.hide()
            self.pushButton_save.setText("编辑")
    
    def updateUiAfterShow(self):
        self.treeWidget_tree.setColumnWidth(0,100)
    
    def mycloneGit(self):
        if not main.gitExist:
            self.pushButton_update.setText("克隆中")
            cloneThread = threading.Thread(target=runClone, name="cloneThread")
            cloneThread.start()
    
    def myupdateGit(self):
        updateThread = threading.Thread(target=updateGit, name="updateThread")
        updateThread.start()
    
    def setUpdateBack(self):
        self.pushButton_update.setText("更新")
    
    def setUpdateStatus(self):
        self.pushButton_update.setText("更新中")

    def addTopDirs(self):
        files = os.listdir(main.gitNoteNoteHome)
        for eachone in files:
            eachone_d = os.path.join(main.gitNoteNoteHome, eachone)
            if os.path.isdir(eachone_d) and eachone[0] != '.':
                item = QTreeWidgetItem(self.treeWidget_tree)
                item.setText(0, eachone)
                item.setText(1, eachone_d)
                item.setIcon(0, self.dirIcon)
                self.showDirs(eachone_d, item)

    def showDirs(self, filepath, item):
        files = os.listdir(filepath)
        for eachone in files:
            eachone_d = os.path.join(filepath, eachone)
            if os.path.isdir(eachone_d) and eachone[0] != '.':
                childitem = QTreeWidgetItem(item)
                countMd = self.countMdFiles(eachone_d)
                dirName = eachone
                if countMd > 0:
                    dirName = eachone + " (" + str(countMd) + ")"
                childitem.setText(0, dirName)
                childitem.setText(1, eachone_d)
                childitem.setIcon(0, self.dirIcon)
                self.showDirs(eachone_d, childitem)
    
    def countMdFiles(self, filepath):
        files = os.listdir(filepath)
        number = 0
        for eachone in files:
            eachone_d = os.path.join(filepath, eachone)
            if not os.path.isdir(eachone_d) and eachone_d[-3:] == ".md":
                number = number + 1
        return number
    
    def onTreeClicked(self, qmodelindex):
        item = self.treeWidget_tree.currentItem()
        if item.text(1) != self.listfileDir:
            self.listfileDir = item.text(1)
            self.listWidget_list.clear()
            self.fileList = self.traverseDir(item.text(1))
            for eachone in self.fileList:
                self.listWidget_list.addItem(eachone[0])
    
    def traverseDir(self, filepath):
        files = os.listdir(filepath)
        fileList = []
        for eachone in files:
            eachone_d = os.path.join(filepath, eachone)
            if not os.path.isdir(eachone_d) and eachone_d[-3:] == ".md":
                tmpfileinfo = []
                tmpfileinfo.append(eachone + "\n" + self.read20words(eachone_d))
                tmpfileinfo.append(os.path.getmtime(eachone_d))
                fileList.append(tmpfileinfo)
        if len(fileList) > 1:
            fileList.sort(key=operator.itemgetter(1), reverse=True)
        return fileList
    
    def read20words(self, filepath):
        returnStr = ""
        readHandle = open(filepath, "r")
        while True:
            oneline = readHandle.readline()
            returnStr = returnStr + oneline.strip()
            if oneline and len(returnStr) <20:
                oneline = readHandle.readline()
                returnStr = returnStr + oneline.strip()
            else:
                break
        readHandle.close()
        if len(returnStr) > 10:
            returnStr = returnStr[:10] + "\n" + returnStr[10:]
        return returnStr