#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTreeWidgetItem, QListWidgetItem, QMenu, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon, QColor, QBrush, QPalette, QColor
from PyQt5.QtCore import Qt
import GitNoteUi
import main
import git
import os, getpass, threading, time, operator, shutil
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
        self.treeWidget_tree.clicked.connect(self.onTreeClicked)
        self.treeWidget_tree.customContextMenuRequested.connect(self.menuContextClicked)
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
        self.listfileDir = main.gitNoteNoteHome
        self.viewfileName = ""
        self.plainTextEdit_markdown.hide()
        self.saveStatus = False
        self.createStatus = False
        self.pushButton_save.clicked.connect(self.clickedButtonSave)
        self.plainTextEdit_markdown.textChanged.connect(self.textChangedEdit)
        self.pushButton_create.clicked.connect(self.createNote)
        self.pushButton_create.setEnabled(False)
        self.pushButton_createdir.setEnabled(False)
        self.pushButton_delete.setEnabled(False)
        self.pushButton_deletedir.setEnabled(False)
        self.pushButton_save.setEnabled(False)
        self.updateListView(self.listfileDir)
        self.newDirName = ""
        self.pushButton_createdir.clicked.connect(self.createDir)
        self.pushButton_createroot.clicked.connect(self.createRootDir)
        self.pushButton_delete.clicked.connect(self.deleteNote)
        self.pushButton_deletedir.clicked.connect(self.deleteDir)
    
    def deleteDir(self):
        countNotes = 0
        for dirpath, dirnames, filenames in os.walk(self.listfileDir):
            for eachone in filenames:
                if os.path.splitext(eachone)[1] == ".md":
                    countNotes = countNotes + 1
        replay = QMessageBox.warning(self, "警告", "文件夹 " + os.path.basename(os.path.normpath(self.listfileDir)) + "下有" + str(countNotes) + "篇笔记，您确定要删除吗？", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes and os.path.exists(self.listfileDir):
            shutil.rmtree(self.listfileDir)
            self.listfileDir = main.gitNoteNoteHome
            self.addTopDirs()
            self.listWidget_list.clear()
            self.pushButton_create.setEnabled(False)
            self.pushButton_createdir.setEnabled(False)
            self.pushButton_delete.setEnabled(False)
            self.pushButton_deletedir.setEnabled(False)
            self.pushButton_save.setEnabled(False)
    
    def deleteNote(self):
        if not os.path.exists(self.viewfileName):
            return
        basename = os.path.basename(self.viewfileName)
        realname = os.path.splitext(basename)[0]
        replay = QMessageBox.warning(self, "警告", "您确定要删除笔记 "+realname+" 吗？", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            os.remove(self.viewfileName)
            self.viewfileName = ""
            self.addTopDirs()
            if os.path.exists(self.listfileDir):
                self.updateListView(self.listfileDir)
            self.pushButton_delete.setEnabled(False)
            self.pushButton_save.setEnabled(False)
            self.lineEdit_title.clear()
            self.plainTextEdit_markdown.clear()
            self.textEdit_show.clear()
    
    def createRootDir(self):
        newDirName, ok = QInputDialog.getText(self, "创建新文件夹", "文件夹名")
        if len(newDirName) > 0:
            newWholeDirName = os.path.join(main.gitNoteNoteHome, newDirName)
            if not os.path.exists(newWholeDirName):
                os.mkdir(newWholeDirName)
                self.addTopDirs()

    def createDir(self):
        newDirName, ok = QInputDialog.getText(self, "创建新文件夹", "文件夹名")
        if len(newDirName) > 0:
            newWholeDirName = os.path.join(self.listfileDir, newDirName)
            if not os.path.exists(newWholeDirName):
                os.mkdir(newWholeDirName)
                self.addTopDirs()
    
    def menuCreateNote(self):
        #item = self.listWidget_list.currentItem()
        #self.listfileDir = item.text(1)
        #self.createNote()
        pass

    def createNote(self):
        if self.saveStatus:
            self.saveNote()
        self.saveStatus = True
        self.pushButton_save.setText("保存")
        self.pushButton_save.setEnabled(True)
        self.createStatus = True
        self.lineEdit_title.setReadOnly(False)
        self.lineEdit_title.clear()
        self.plainTextEdit_markdown.clear()
        self.plainTextEdit_markdown.show()
        self.textEdit_show.clear()
    
    def clickedListView(self, qmodelindex):
        if self.saveStatus or self.createStatus:
            self.saveNote()
        item = self.listWidget_list.currentItem()
        itemCount = item.text()
        filename = (itemCount.split("\n"))[0]
        self.pushButton_delete.setEnabled(True)
        self.pushButton_deletedir.setEnabled(False)
        self.pushButton_save.setEnabled(True)
        self.viewfileName = os.path.join(self.listfileDir, filename)
        if self.viewfileName[-3:] != ".md":
            self.viewfileName = self.viewfileName + ".md"
        self.lineEdit_title.setText(os.path.splitext(filename)[0])
        tmpf = open(self.viewfileName, "r")
        self.viewTexts = tmpf.read()
        tmpf.close()
        self.textEdit_show.setText(markdown2.markdown(self.viewTexts))

    def menuContextClicked(self, pos):
        item = self.listWidget_list.itemAt(pos)
        if item:
            self.treemenu = QMenu()
            self.treemenu.addAction("新建笔记", self.menuCreateNote)
            self.treemenu.addAction("新建文件夹")
            self.treemenu.addAction("删除文件夹")
            self.treemenu.exec_(self.treeWidget_tree.mapToGlobal(pos))
        
    def textChangedEdit(self):
        self.viewTexts = self.plainTextEdit_markdown.toPlainText()
        self.textEdit_show.setText(markdown2.markdown(self.viewTexts))
    
    def clickedButtonSave(self):
        if not self.saveStatus:
            if len(self.viewfileName) > 1:
                self.saveStatus = True
                self.plainTextEdit_markdown.setPlainText(self.viewTexts)
                self.plainTextEdit_markdown.show()
                self.pushButton_save.setText("保存")
        else:
            self.saveNote()
    
    def saveNote(self):
        if self.createStatus:
            self.viewfileName = os.path.join(self.listfileDir, self.lineEdit_title.text().strip())
            self.lineEdit_title.setReadOnly(True)
            if self.viewfileName[-3:] != ".md":
                self.viewfileName = self.viewfileName + ".md"
        self.saveStatus = False
        self.plainTextEdit_markdown.hide()
        self.pushButton_save.setText("编辑")
        self.lineEdit_title.setReadOnly(True)
        if len(self.viewfileName) > 1:
            tmpf = open(self.viewfileName, "w")
            tmpf.write(self.viewTexts)
            tmpf.close()
            self.updateListView(self.listfileDir)
            #self.treeWidget_tree.clear()
            #self.updateTreeItemName()
        if self.createStatus:
            self.createStatus = False
            self.addTopDirs()
    
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
        self.treeWidget_tree.clear()
        files = os.listdir(main.gitNoteNoteHome)
        for eachone in files:
            eachone_d = os.path.join(main.gitNoteNoteHome, eachone)
            if os.path.isdir(eachone_d) and eachone[0] != '.':
                item = QTreeWidgetItem(self.treeWidget_tree)
                countMd = self.countMdFiles(eachone_d)
                dirName = eachone
                if countMd > 0:
                    dirName = eachone + " (" + str(countMd) + ")"
                item.setText(0, dirName)
                item.setText(1, eachone_d)
                item.setIcon(0, self.dirIcon)
                self.showDirs(eachone_d, item)
        self.treeWidget_tree.expandAll()

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
    
    def updateTreeItemName(self):
        baseName = self.treeItem.text(0).split('(')[0]
        countMd = self.countMdFiles(self.treeItem.text(1))
        dirName = baseName
        if countMd > 0:
            dirName = dirName + " (" + str(countMd) + ")"
        self.treeItem.setText(0, dirName)
    
    def countMdFiles(self, filepath):
        files = os.listdir(filepath)
        number = 0
        for eachone in files:
            eachone_d = os.path.join(filepath, eachone)
            if not os.path.isdir(eachone_d) and eachone_d[-3:] == ".md":
                number = number + 1
        return number
    
    def onTreeClicked(self, qmodelindex):
        self.pushButton_create.setEnabled(True)
        self.pushButton_createdir.setEnabled(True)
        self.pushButton_delete.setEnabled(False)
        self.pushButton_deletedir.setEnabled(True)
        self.treeItem = self.treeWidget_tree.currentItem()
        if self.treeItem.text(1) != self.listfileDir:
            self.listfileDir = self.treeItem.text(1)
            self.updateListView(self.listfileDir)
    
    def updateListView(self, fileDir):
        self.listWidget_list.clear()
        if fileDir == main.gitNoteNoteHome:
            return
        self.fileList = self.traverseDir(fileDir)
        for eachone in self.fileList:
            self.listWidget_list.addItem(eachone[0])
    
    def traverseDir(self, filepath):
        files = os.listdir(filepath)
        fileList = []
        for eachone in files:
            eachone_d = os.path.join(filepath, eachone)
            if not os.path.isdir(eachone_d) and eachone_d[-3:] == ".md":
                tmpfileinfo = []
                tmpfileinfo.append(eachone[:-3] + "\n" + self.read20words(eachone_d))
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