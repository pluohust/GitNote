#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTreeWidgetItem, QListWidgetItem, QMenu, QInputDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QColor, QBrush, QPalette, QColor, QFontMetricsF, QPixmap, QMovie, QTextCursor
from PyQt5.QtCore import Qt, QByteArray
import GitNoteUi
import main
import git
import os, getpass, threading, time, datetime, operator, shutil
import pathlib
import markdown2

def runClone():
    main.setGitEnv()
    git.Repo.clone_from(url=main.gitUrl, to_path="/home/"+getpass.getuser()+"/.GitNote/Notes")
    #git.Git("/home/"+getpass.getuser()+"/.GitNote/Notes").clone(main.gitUrl)
    main.myGitNote.setUpdateBack()

def updateGit():
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
        self.treeWidget_tree.customContextMenuRequested.connect(self.menuTreeContextClicked)
        self.listWidget_list.setStyleSheet(
        "QListWidget::item { border-bottom: 0.5px dotted blue; margin-bottom:10px;}"
        "QListWidget::item:!selected{}"  
        "QListWidget::item:selected:active{background:#FFFFFF;color:#19649F;border-width:-1;}"  
        "QListWidget::item:selected{background:#FFFFFF;color:#19649F;}")
        self.listWidget_list.clicked.connect(self.clickedListView)
        self.listWidget_list.customContextMenuRequested.connect(self.menuListContextClicked)
        #self.treeWidget_tree.addTopLevelItem(root)
        # set window background color
        self.setAutoFillBackground(True)
        pBack = self.palette()
        pBack.setColor(self.backgroundRole(), QColor(79, 79, 79))
        self.setPalette(pBack)
        self.listfileDir = main.gitNoteNoteHome
        self.viewfileName = ""
        self.plainTextEdit_markdown.hide()
        self.plainTextEdit_markdown.setTabStopDistance(QFontMetricsF(self.plainTextEdit_markdown.font()).width(' ')*4)
        self.saveStatus = False
        self.createStatus = False
        self.pushButton_save.clicked.connect(self.clickedButtonSave)
        self.plainTextEdit_markdown.textChanged.connect(self.textChangedEdit)
        self.pushButton_save.setEnabled(False)
        self.updateListView(self.listfileDir)
        self.newDirName = ""
        self.pushButton_addpicture.setEnabled(False)
        self.pushButton_addpicture.clicked.connect(self.choosePictures)
        self.insertPictures = []
        # 设置更新图标
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "loading.png")), QIcon.Normal, QIcon.Off)
        self.pushButton_update.setIcon(icon)
        saveicon = QIcon()
        saveicon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "edit.ico")), QIcon.Normal, QIcon.Off)
        self.pushButton_save.setIcon(saveicon)
        addpicturicon = QIcon()
        addpicturicon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "addpicture.png")), QIcon.Normal, QIcon.Off)
        self.pushButton_addpicture.setIcon(addpicturicon)
        # 保存打开时的文本
        self.oldTexts = ""

    def closeEvent(self, event):
        if self.saveStatus:
            unsavereturn = self.saveNote(False)
            if not unsavereturn:
                replay = QMessageBox.question(self, "未保存警告", "有未保存的未命名笔记，确定退出？", QMessageBox.Yes, QMessageBox.No)
                if replay == QMessageBox.Yes:
                    event.accept()
                    return
                elif replay == QMessageBox.No:
                    event.ignore()
                    return
        event.accept()
    
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_O):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.pushButton_save.clicked.emit()
    
    def choosePictures(self):
        pictures, ok = QFileDialog.getOpenFileNames(self, "选取图片", str(pathlib.Path.home()), "Picture Files (*.png | *.jpg | *.jpeg | *.gif | *.ico")
        for eachfile in pictures:
            basenamewith = os.path.basename(eachfile)
            basename, suffix = os.path.splitext(basenamewith)
            i = 0
            while os.path.exists(os.path.join(self.showTextDir, basename+"-"+str(i)+suffix)):
                i = i + 1
            lastbasename =basename + "-" + str(i) + suffix
            self.insertPictures.append(lastbasename)
            self.plainTextEdit_markdown.insertPlainText("\n![](" + lastbasename + ")\n")
            lastname = os.path.join(self.showTextDir, lastbasename)
            shutil.copyfile(eachfile, lastname)
            time.sleep(0.01)
    
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
            self.pushButton_save.setEnabled(False)
    
    def deleteNote(self):
        if not os.path.exists(self.viewfileName):
            return
        basename = os.path.basename(self.viewfileName)
        realname = os.path.splitext(basename)[0]
        replay = QMessageBox.warning(self, "警告", "您确定要删除笔记 "+realname+" 吗？", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            # 先删除里面的图片
            tmpf = open(self.viewfileName, "r")
            tmpviewTexts = tmpf.read()
            tmpf.close()
            multilines = tmpviewTexts.split("\n")
            for eachline in multilines:
                if "![](" in eachline and ")" in eachline.split("![](")[1]:
                    shotfile = (eachline.split("![](")[1]).split(")")[0]
                    realfile = os.path.join(self.listfileDir, shotfile)
                    if os.path.exists(realfile):
                        os.remove(realfile)
            # 然后删除markdown文件和更新控件显示
            os.remove(self.viewfileName)
            self.viewfileName = ""
            self.addTopDirs()
            if os.path.exists(self.listfileDir):
                self.updateListView(self.listfileDir)
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
    
    def menuListContextClicked(self, pos):
        item = self.listWidget_list.itemAt(pos)
        if item:
            itemCount = item.text()
            filename = (itemCount.split("\n"))[0]
            self.viewfileName = os.path.join(self.listfileDir, filename)
            if self.viewfileName[-3:] != ".md":
                self.viewfileName = self.viewfileName + ".md"
            self.listmenu = QMenu()
            self.listmenu.addAction("删除笔记", self.deleteNote)
            self.listmenu.exec_(self.listWidget_list.mapToGlobal(pos))

    def menuTreeContextClicked(self, pos):
        item = self.treeWidget_tree.itemAt(pos)
        if item:
            self.listfileDir = item.text(1)
            self.updateListView(self.listfileDir)
            self.treemenu = QMenu()
            self.treemenu.addAction("新建笔记", self.createNote)
            self.treemenu.addAction("新建文件夹", self.createDir)
            self.treemenu.addAction("删除文件夹", self.deleteDir)
            self.treemenu.exec_(self.treeWidget_tree.mapToGlobal(pos))
        else:
            self.listfileDir = main.gitNoteNoteHome
            self.treerootmenu = QMenu()
            self.treerootmenu.addAction("新建Root文件夹", self.createRootDir)
            self.treerootmenu.exec_(self.treeWidget_tree.mapToGlobal(pos))

    def createNote(self):
        self.insertPictures = []
        if self.saveStatus:
            self.saveNote(True)
        self.saveStatus = True
        saveicon = QIcon()
        saveicon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "save.ico")), QIcon.Normal, QIcon.Off)
        self.pushButton_save.setIcon(saveicon)
        self.pushButton_save.setEnabled(True)
        self.pushButton_addpicture.setEnabled(True)
        self.createStatus = True
        self.lineEdit_title.setReadOnly(False)
        self.lineEdit_title.clear()
        self.plainTextEdit_markdown.clear()
        self.plainTextEdit_markdown.show()
        self.textEdit_show.clear()
        self.lineEdit_title.setFocus()
        self.oldTexts = ""
        self.showTextDir = self.listfileDir
    
    def clickedListView(self, qmodelindex):
        item = self.listWidget_list.currentItem()
        if not item:
            return
        if self.saveStatus or self.createStatus:
            self.saveNote(True)
        itemCount = item.text()
        filename = (itemCount.split("\n"))[0]
        self.pushButton_save.setEnabled(True)
        self.viewfileName = os.path.join(self.listfileDir, filename)
        if self.viewfileName[-3:] != ".md":
            self.viewfileName = self.viewfileName + ".md"
        self.lineEdit_title.setText(os.path.splitext(filename)[0])
        tmpf = open(self.viewfileName, "r")
        self.viewTexts = tmpf.read()
        tmpf.close()
        self.showTextDir = self.listfileDir
        self.textEdit_show.setText(markdown2.markdown(self.showRealPictures(self.viewTexts)))
        self.textEdit_show.moveCursor(QTextCursor.Start)
    
    def showRealPictures(self, inputtext):
        multilines = inputtext.split("\n")
        realtext = ""
        for eachline in multilines:
            if "![](" in eachline and ")" in eachline.split("![](")[1]:
                shotfile = (eachline.split("![](")[1]).split(")")[0]
                realfile = os.path.join(self.showTextDir, shotfile)
                realtext = realtext + "![](" + realfile + ")\n"
            else:
                realtext = realtext + eachline + "\n"
        return realtext
        
    def textChangedEdit(self):
        self.viewTexts = self.plainTextEdit_markdown.toPlainText()
        therealmd = self.showRealPictures(self.viewTexts)
        #self.textEdit_show.clear()
        self.textEdit_show.setText(markdown2.markdown(therealmd))
        self.textEdit_show.moveCursor(QTextCursor.End)

    
    def clickedButtonSave(self):
        if not self.saveStatus: # 编辑
            if len(self.viewfileName) > 1:
                # 更新已有的图片
                self.insertPictures = []
                multilines = self.viewTexts.split("\n")
                for eachline in multilines:
                    if "![](" in eachline and ")" in eachline.split("![](")[1]:
                        shotfile = (eachline.split("![](")[1]).split(")")[0]
                        self.insertPictures.append(shotfile)

                self.saveStatus = True
                self.plainTextEdit_markdown.setPlainText(self.viewTexts)
                self.plainTextEdit_markdown.show()
                saveicon = QIcon()
                saveicon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "save.ico")), QIcon.Normal, QIcon.Off)
                self.pushButton_save.setIcon(saveicon)
                self.pushButton_addpicture.setEnabled(True)
                self.oldTexts = self.viewTexts
        else: #保存
            self.pushButton_addpicture.setEnabled(False)
            self.saveNote(True)
            self.textEdit_show.moveCursor(QTextCursor.Start)

    def saveNote(self, checkwarning):
        if len(self.lineEdit_title.text()) < 1:
            if checkwarning:
                QMessageBox.information(self, "警告", "请输入记录名！", QMessageBox.Yes)
            return False
        if self.createStatus:
            self.viewfileName = os.path.join(self.showTextDir, self.lineEdit_title.text().strip())
            self.lineEdit_title.setReadOnly(True)
            if self.viewfileName[-3:] != ".md":
                self.viewfileName = self.viewfileName + ".md"
        self.saveStatus = False
        self.plainTextEdit_markdown.hide()
        saveicon = QIcon()
        saveicon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "edit.ico")), QIcon.Normal, QIcon.Off)
        self.pushButton_save.setIcon(saveicon)
        self.lineEdit_title.setReadOnly(True)
        if len(self.viewfileName) > 1:
            if not self.createStatus and self.oldTexts == self.viewTexts:
                return
            tmpf = open(self.viewfileName, "w")
            tmpf.write(self.viewTexts)
            tmpf.close()
            self.updateListView(self.listfileDir)
            #pictures
            for eachpicture in self.insertPictures:
                if eachpicture not in self.viewTexts and os.path.exists(os.path.join(self.listfileDir, eachpicture)):
                    os.remove(os.path.join(self.listfileDir, eachpicture))
            #self.treeWidget_tree.clear()
            #self.updateTreeItemName()
        if self.createStatus:
            self.createStatus = False
            self.addTopDirs()
        return True
    
    def updateUiAfterShow(self):
        self.treeWidget_tree.setColumnWidth(0,100)
    
    def mycloneGit(self):
        if not main.gitExist:
            self.movie = QMovie(os.path.join(os.path.dirname(__file__), "loading.gif"), QByteArray(), self)
            self.movie.frameChanged.connect(self.setButtonIcon)
            self.movie.start()
            cloneThread = threading.Thread(target=runClone, name="cloneThread")
            cloneThread.start()
    
    def myupdateGit(self):
        self.setUpdateStatus()
        updateThread = threading.Thread(target=updateGit, name="updateThread")
        updateThread.start()
    
    def setUpdateBack(self):
        self.movie = None
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "loading.png")), QIcon.Normal, QIcon.Off)
        self.pushButton_update.setIcon(icon)
    
    def setButtonIcon(self):
        if self.movie:
            self.pushButton_update.setIcon(QIcon(self.movie.currentPixmap()))
    
    def setUpdateStatus(self):
        self.movie = QMovie(os.path.join(os.path.dirname(__file__), "loading.gif"), QByteArray(), self)
        self.movie.frameChanged.connect(self.setButtonIcon)
        self.movie.start()

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
        returnStr = returnStr + "\n" + self.timeStampToTime(os.path.getmtime(filepath))
        return returnStr
    
    def timeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)