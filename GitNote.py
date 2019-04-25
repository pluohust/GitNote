#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTreeWidgetItem, QListWidgetItem, QMenu, QInputDialog, QMessageBox, QFileDialog, QToolButton, QFontDialog, QColorDialog
from PyQt5.QtGui import QIcon, QColor, QBrush, QPalette, QColor, QFontMetricsF, QPixmap, QMovie, QTextCursor, QFont
from PyQt5.QtCore import Qt, QByteArray, QThread, QTimer, QSize
import GitNoteUi
import main
import git
import os, getpass, threading, time, datetime, operator, shutil
import pathlib
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
import json, pdfkit

movieStatus = False

class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

class CloneThread(QThread):
    def __init__(self):
        super(CloneThread, self).__init__()
    
    def run(self):
        global movieStatus
        main.setGitEnv()
        git.Repo.clone_from(url=main.gitUrl, to_path=main.gitNoteNoteHome)
        movieStatus = True
        #main.myGitNote.setUpdateBack()

class UpdateThread(QThread):
    def __init__(self):
        super(UpdateThread, self).__init__()
    
    def run(self):
        global movieStatus
        main.setGitEnv()
        repo = git.Repo(main.gitNoteNoteHome)
        remote = repo.remote()
        repo.git.add('--all')
        repo.index.commit('note')
        remote.push()
        remote.pull()
        movieStatus = True
        #main.myGitNote.setUpdateBack()

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
        # 界面配置
        self.configfile = os.path.join(main.gitNoteHome, "config.json")
        self.initInterface()
        self.pushButton_update.clicked.connect(self.myupdateGit)
        self.treeWidget_tree.clicked.connect(self.onTreeClicked)
        self.treeWidget_tree.customContextMenuRequested.connect(self.menuTreeContextClicked)
        self.listWidget_list.clicked.connect(self.clickedListView)
        self.listWidget_list.customContextMenuRequested.connect(self.menuListContextClicked)
        #self.treeWidget_tree.addTopLevelItem(root)
        # set window background color
        self.setAutoFillBackground(True)
        self.listfileDir = main.gitNoteNoteHome
        self.viewfileName = ""
        self.viewTexts = ""
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
        # 更新恢复
        self.movietimer = QTimer(self)
        self.movietimer.start(500)
        self.movietimer.timeout.connect(self.movieTimeout)
        # 配置
        configicon = QIcon()
        configicon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "config.ico")), QIcon.Normal, QIcon.Off)
        self.toolButton_config.setIcon(configicon)
        toolmenu = QMenu()
        toolmenu.addAction("设置字体", self.setFont)
        toolmenu.addAction("默认主题", self.whiteTheme)
        toolmenu.addAction("暗黑主题", self.blackTheme)
        self.toolButton_config.setMenu(toolmenu)
        self.toolButton_config.setPopupMode(QToolButton.MenuButtonPopup)
        # 转换
        convertico = QIcon(os.path.join(os.path.dirname(__file__), "convert.ico"))
        self.toolButton_functions.setIcon(convertico)
        convertmenu = QMenu()
        convertmenu.addAction("另存为pdf文件", self.viewToPdf)
        self.toolButton_functions.setMenu(convertmenu)
    
    def viewToPdf(self):
        if not self.pushButton_save.isEnabled() and not self.pushButton_addpicture.isEnabled():
            return
        filename, filetype = QFileDialog.getSaveFileName(self, "文件保存", str(pathlib.Path.home()), "PdfFiles (*.pdf)")
        if filename != "":
            if filename[-4:] != '.pdf':
                oldfilename = filename
                filename = filename + '.pdf'
                if os.path.exists(filename) and not os.path.exists(oldfilename):
                    replay = QMessageBox.question(self, "文件覆盖警告", "文件"+os.path.basename(filename)+"已存在，确定覆盖？", QMessageBox.Yes, QMessageBox.No)
                    if replay == QMessageBox.No:
                        return
            markdown = mistune.Markdown()
            pdfkit.from_string('<head><meta charset="UTF-8"></head>' + markdown(self.showRealPictures(self.viewTexts)), filename)
            #print(markdown(self.showRealPictures(self.viewTexts)))

    def initInterface(self):
        self.interfacedata = {'theme': 'white'}
        if not os.path.exists(self.configfile):
            self.whiteTheme()
            return
        with open(self.configfile, 'r') as f:
            self.interfacedata = json.load(f)
        if 'theme' in self.interfacedata and self.interfacedata['theme'] == 'black':
            self.blackTheme()
        else:
            self.whiteTheme()
        if 'font' in self.interfacedata:
            font = QFont()
            font.fromString(self.interfacedata['font'])
            self.plainTextEdit_markdown.setFont(font)
            self.textEdit_show.setFont(font)

    def whiteTheme(self):
        self.dirIcon = QIcon(os.path.join(os.path.dirname(__file__),"dir.ico"))
        self.addTopDirs()
        pBack = self.palette()
        pBack.setColor(self.backgroundRole(), QColor(239, 235, 231))
        self.setPalette(pBack)
        self.treeWidget_tree.setStyleSheet('background-color: rgb(255, 255, 255);color: rgb(0, 0, 0)')
        self.listWidget_list.setStyleSheet("QListWidget{background-color: rgb(255, 255, 255);color: rgb(0, 0, 0);}"
        "QListWidget::item { border-bottom: 0.5px dotted black; margin-bottom:10px;}"
        "QListWidget::item:!selected{}"  
        "QListWidget::item:selected:active{background:#FFFFFF;color:#19649F;border-width:-1;}"  
        "QListWidget::item:selected{background:#FFFFFF;color:#19649F;}")
        self.lineEdit_title.setStyleSheet('background-color: rgb(255, 255, 255);color: rgb(0, 0, 0)')
        self.plainTextEdit_markdown.setStyleSheet('background-color: rgb(255, 255, 255);color: rgb(0, 0, 0)')
        self.textEdit_show.setStyleSheet('background-color: rgb(255, 255, 255);color: rgb(0, 0, 0)')
        if self.interfacedata['theme'] != 'white':
            self.interfacedata['theme'] = 'white'
            with open(self.configfile, 'w') as f:
                json.dump(self.interfacedata, f)
    
    def blackTheme(self):
        self.dirIcon = QIcon(os.path.join(os.path.dirname(__file__),"blackdir.ico"))
        self.addTopDirs()
        pBack = self.palette()
        pBack.setColor(self.backgroundRole(), QColor(51, 51, 51))
        self.setPalette(pBack)
        self.treeWidget_tree.setStyleSheet('background-color: rgb(51, 51, 51);color: rgb(200, 200, 200);')
        self.listWidget_list.setStyleSheet("QListWidget{background-color: rgb(37, 37, 38);color: rgb(200, 200, 200);}"
        "QListWidget::item { border-bottom: 0.5px dotted white; margin-bottom:10px;}")
        self.lineEdit_title.setStyleSheet('background-color: rgb(30, 30, 30);color: rgb(200, 200, 200)')
        self.plainTextEdit_markdown.setStyleSheet('background-color: rgb(30, 30, 30);color: rgb(200, 200, 200)')
        self.textEdit_show.setStyleSheet('background-color: rgb(30, 30, 30);color: rgb(200, 200, 200)')
        if self.interfacedata['theme'] != 'black':
            self.interfacedata['theme'] = 'black'
            with open(self.configfile, 'w') as f:
                json.dump(self.interfacedata, f)

    def setFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.plainTextEdit_markdown.setFont(font)
            self.textEdit_show.setFont(font)
            self.interfacedata['font'] = font.toString()
            with open(self.configfile, 'w') as f:
                json.dump(self.interfacedata, f)

    def movieTimeout(self):
        global movieStatus
        if movieStatus:
            movieStatus = False
            self.setUpdateBack()

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
        #self.saveNote(True)
        event.accept()
    
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_O):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.pushButton_save.clicked.emit()
    
    def choosePictures(self):
        pictures, ok = QFileDialog.getOpenFileNames(self, "选取图片", str(pathlib.Path.home()), "Picture Files (*.png | *.jpg | *.jpeg | *.gif | *.ico | *.svg)")
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
    
    def moveDirToDir(self):
        dir_choose = QFileDialog.getExistingDirectory(self, "选择目标文件夹", main.gitNoteNoteHome)
        if self.listfileDir in dir_choose:
            QMessageBox.information(self, "警告", "文件夹不能移动到当前目录和子目录！", QMessageBox.Yes)
            return
        targetDir = self.getTargetName(dir_choose, os.path.basename(self.listfileDir))
        if os.path.exists(self.listfileDir):
            shutil.move(self.listfileDir, targetDir)
        if self.listfileDir in self.viewfileName:
            self.lineEdit_title.clear()
            self.plainTextEdit_markdown.clear()
            self.textEdit_show.clear()
        self.listfileDir = main.gitNoteNoteHome
        self.addTopDirs()
        self.listWidget_list.clear()
        self.pushButton_save.setEnabled(False)
    
    def deleteDir(self):
        countNotes = 0
        for dirpath, dirnames, filenames in os.walk(self.listfileDir):
            for eachone in filenames:
                if os.path.splitext(eachone)[1] == ".md":
                    countNotes = countNotes + 1
        replay = QMessageBox.warning(self, "警告", "文件夹 " + os.path.basename(os.path.normpath(self.listfileDir)) + "下有" + str(countNotes) + "篇笔记，您确定要删除吗？", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes and os.path.exists(self.listfileDir):
            shutil.rmtree(self.listfileDir)
            if self.listfileDir in self.viewfileName:
                self.lineEdit_title.clear()
                self.plainTextEdit_markdown.clear()
                self.textEdit_show.clear()
            self.listfileDir = main.gitNoteNoteHome
            self.addTopDirs()
            self.listWidget_list.clear()
            self.pushButton_save.setEnabled(False)

    def getPicturesInOneNote(self, filename):
        pictures = []
        tmpf = open(filename, "r", encoding='UTF-8')
        tmpviewTexts = tmpf.read()
        tmpf.close()
        multilines = tmpviewTexts.split("\n")
        for eachline in multilines:
            if "![](" in eachline and ")" in eachline.split("![](")[1]:
                shotfile = (eachline.split("![](")[1]).split(")")[0]
                realfile = os.path.join(self.listfileDir, shotfile)
                if os.path.exists(realfile):
                    pictures.append(realfile)
        return pictures
    
    def deleteNote(self):
        if not os.path.exists(self.listmenufilename):
            return
        basename = os.path.basename(self.listmenufilename)
        realname = os.path.splitext(basename)[0]
        replay = QMessageBox.warning(self, "警告", "您确定要删除笔记 "+realname+" 吗？", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            # 先删除里面的图片
            pictures = self.getPicturesInOneNote(self.listmenufilename)
            for eachpicture in pictures:
                os.remove(eachpicture)
            # 然后删除markdown文件和更新控件显示
            os.remove(self.listmenufilename)
            self.addTopDirs()
            if os.path.exists(self.listfileDir):
                self.updateListView(self.listfileDir)
            if self.listmenufilename.strip() == self.viewfileName.strip():
                self.clearNoteShow()
            self.listmenufilename = ""
    
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
            #self.viewfileName = os.path.join(self.listfileDir, filename)
            #if self.viewfileName[-3:] != ".md":
            #    self.viewfileName = self.viewfileName + ".md"
            self.listmenufilename = os.path.join(self.listfileDir, filename)
            if self.listmenufilename[-3:] != ".md":
                self.listmenufilename = self.listmenufilename + ".md"
            self.listmenu = QMenu()
            self.listmenu.addAction("删除笔记", self.deleteNote)
            self.listmenu.addAction("移动笔记", self.moveNoteToDir)
            self.listmenu.addAction("重命名笔记", self.renameNote)
            self.listmenu.exec_(self.listWidget_list.mapToGlobal(pos))
    
    def clearNoteShow(self):
        self.pushButton_save.setEnabled(False)
        self.lineEdit_title.clear()
        self.lineEdit_title.setReadOnly(True)
        self.pushButton_addpicture.setEnabled(False)
        self.plainTextEdit_markdown.clear()
        self.plainTextEdit_markdown.hide()
        self.textEdit_show.clear()
        self.viewfileName = ""

    def renameNote(self):
        newname, ok = QInputDialog.getText(self, "笔记重命名", "请输入新名：")
        newname = newname + ".md"
        if ok:
            newfilepath = os.path.join(self.listfileDir, newname)
            if os.path.exists(newfilepath):
                QMessageBox.warning(self, "警告", "笔记已存在，请重新命名", QMessageBox.Yes, QMessageBox.Yes)
                return
            if os.path.exists(self.listmenufilename):
                shutil.move(self.listmenufilename, newfilepath)
                if self.viewfileName.strip() == self.listmenufilename.strip():
                    realname = os.path.splitext(newname)[0]
                    self.lineEdit_title.setText(realname)
                    self.viewfileName = newfilepath
                if os.path.exists(self.listfileDir):
                    self.updateListView(self.listfileDir)

    def getTargetName(self, targetDir, basenamewith):
        if os.path.exists(os.path.join(targetDir, basenamewith)):
            basename, suffix = os.path.splitext(basenamewith)
            i = 0
            while os.path.exists(os.path.join(targetDir, basename+"-"+str(i)+suffix)):
                i = i + 1
            basenamewith = basename + "-" + str(i) + suffix
        return os.path.join(targetDir, basenamewith)
    
    def replacePictureName(self, viewTexts, basename, newbasename):
        multilines = viewTexts.split("\n")
        newViewTexts = ""
        for eachline in multilines:
            if "![](" in eachline and ")" in eachline.split("![](")[1] and (eachline.split("![](")[1]).split(")")[0] == basename:
                newViewTexts = newViewTexts + "![]("+newbasename+")\n"
            else:
                newViewTexts = newViewTexts + eachline+"\n"
        return newViewTexts
    
    def moveNoteToDir(self):
        dir_choose = QFileDialog.getExistingDirectory(self, "选择目标文件夹", main.gitNoteNoteHome)
        if main.gitNoteNoteHome in dir_choose and os.path.dirname(self.listmenufilename) != dir_choose:
            # 移动图片
            tmpf = open(self.listmenufilename, "r", encoding='UTF-8')
            tmpviewTexts = tmpf.read()
            tmpf.close()
            pictures = self.getPicturesInOneNote(self.listmenufilename)
            for eachpicture in pictures:
                basename = os.path.basename(eachpicture)
                targetfilename = self.getTargetName(dir_choose, basename)
                if os.path.exists(eachpicture):
                    shutil.move(eachpicture, targetfilename)
                newbasename = os.path.basename(targetfilename)
                tmpviewTexts= self.replacePictureName(tmpviewTexts, basename, newbasename)
            tmpf = open(self.listmenufilename, "w", encoding='UTF-8')
            tmpf.write(tmpviewTexts)
            tmpf.close()
            # 移动日记文件
            basename = os.path.basename(self.listmenufilename)
            targetfilename = self.getTargetName(dir_choose, basename)
            if os.path.exists(self.listmenufilename):
                shutil.move(self.listmenufilename, targetfilename)
            if self.viewfileName.strip() == self.listmenufilename.strip():
                self.viewfileName = ""
                self.clearNoteShow()
            self.addTopDirs()
            if os.path.exists(self.listfileDir):
                self.updateListView(self.listfileDir)
    
    def renameDir(self):
        newname, ok = QInputDialog.getText(self, "笔记重命名", "请输入新名：")
        if ok:
            if self.listfileDir[-1] == '/' or self.listfileDir[-1] == '\\':
                self.listfileDir = self.listfileDir[:-1]
            newDir = os.path.join(os.path.dirname(self.listfileDir), newname)
            if os.path.exists(newDir):
                QMessageBox.warning(self, "警告", "文件夹已存在，请重新命名", QMessageBox.Yes, QMessageBox.Yes)
                return
            else:
                shutil.move(self.listfileDir, newDir)
                self.listfileDir = newDir
                self.addTopDirs()
                self.updateListView(self.listfileDir)
                self.clearNoteShow()

    def menuTreeContextClicked(self, pos):
        item = self.treeWidget_tree.itemAt(pos)
        if item:
            self.listfileDir = item.text(1)
            self.updateListView(self.listfileDir)
            self.treemenu = QMenu()
            self.treemenu.addAction("新建笔记", self.createNote)
            self.treemenu.addAction("新建日记", self.createDiaryNote)
            self.treemenu.addAction("新建文件夹", self.createDir)
            self.treemenu.addAction("删除文件夹", self.deleteDir)
            self.treemenu.addAction("移动文件夹", self.moveDirToDir)
            self.treemenu.addAction("重命名文件夹", self.renameDir)
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

    def createDiaryNote(self):
        today = str(time.strftime("%Y-%m-%d", time.localtime()))
        self.createNote()
        self.lineEdit_title.setText(today)
        self.plainTextEdit_markdown.setFocus()
    
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
        self.lineEdit_title.setText(filename)
        tmpf = open(self.viewfileName, "r", encoding='UTF-8')
        self.viewTexts = tmpf.read()
        tmpf.close()
        self.showTextDir = self.listfileDir
        #self.textEdit_show.setText(markdown2.markdown(self.showRealPictures(self.viewTexts)))
        #self.textEdit_show.setHtml(markdown2.markdown(self.showRealPictures(self.viewTexts)))
        #renderer = HighlightRenderer()
        markdown = mistune.Markdown()
        markdownTxt = markdown(self.showRealPictures(self.viewTexts))
        markdownTxt = markdownTxt.replace("\n<", "$&$&$&").strip()
        markdownTxt = markdownTxt.replace("\n", r"<br>")
        markdownTxt = markdownTxt.replace("$&$&$&", "\n<")
        self.textEdit_show.setHtml(markdownTxt)
        #print(markdown(self.showRealPictures(self.viewTexts)))
        self.textEdit_show.moveCursor(QTextCursor.Start)
    
    def showRealPictures(self, inputtext):
        multilines = inputtext.split("\n")
        realtext = ""
        for eachline in multilines:
            if "![](" in eachline and ")" in eachline.split("![](")[1]:
                shotfile = (eachline.split("![](")[1]).split(")")[0]
                realfile = os.path.join(self.showTextDir, shotfile)
                #realtext = realtext + "![](" + realfile + ")\n"
                realtext = realtext + '<img src="' + realfile + '" />\n'
            else:
                realtext = realtext + eachline + "\n"
        return realtext
        
    def textChangedEdit(self):
        self.viewTexts = self.plainTextEdit_markdown.toPlainText()
        #therealmd = self.showRealPictures(self.viewTexts)
        #self.textEdit_show.clear()
        #self.textEdit_show.setText(markdown2.markdown(therealmd))
        #self.textEdit_show.setHtml(markdown2.markdown(therealmd))
        #renderer = HighlightRenderer()
        #markdown = mistune.Markdown(renderer=renderer)
        markdown = mistune.Markdown()
        markdownTxt = markdown(self.showRealPictures(self.viewTexts))
        markdownTxt = markdownTxt.replace("\n<", "$&$&$&").strip()
        markdownTxt = markdownTxt.replace("\n", r"<br>")
        markdownTxt = markdownTxt.replace("$&$&$&", "\n<")
        self.textEdit_show.setHtml(markdownTxt)
        #markdown = mistune.Markdown()
        #self.textEdit_show.setHtml(markdown(self.showRealPictures(self.viewTexts)))
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
                return True
            tmpf = open(self.viewfileName, "w", encoding='UTF-8')
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
            main.updateStatus = True
            self.cloneThread = CloneThread()
            self.cloneThread.start()
    
    def myupdateGit(self):
        if main.updateStatus:
            return
        else:
            main.updateStatus = True
        self.setUpdateStatus()
        self.updateThread = UpdateThread()
        self.updateThread.start()
    
    def setUpdateBack(self):
        self.movie = None
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "loading.png")), QIcon.Normal, QIcon.Off)
        self.pushButton_update.setIcon(icon)
        self.addTopDirs()
        self.treeWidget_tree.expandAll()
        main.updateStatus = False
        #self.pushButton_update.setText("更新")
    
    def setButtonIcon(self):
        if self.movie:
            self.pushButton_update.setIcon(QIcon(self.movie.currentPixmap()))
    
    def setUpdateStatus(self):
        self.movie = QMovie(os.path.join(os.path.dirname(__file__), "loading.gif"), QByteArray(), self)
        self.movie.frameChanged.connect(self.setButtonIcon)
        self.movie.start()
        #self.pushButton_update.setText("更新中")

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
            tmpitem = QListWidgetItem(eachone[0])
            #if len(eachone[2]) > 1:
            #    tmpitem.setIcon(QIcon(eachone[2]))
            #tmpitem.setTextAlignment(Qt.AlignLeft)
            #tmpitem.setSizeHint(QSize(150, 100))
            self.listWidget_list.addItem(tmpitem)
    
    def traverseDir(self, filepath):
        files = os.listdir(filepath)
        fileList = []
        for eachone in files:
            eachone_d = os.path.join(filepath, eachone)
            if not os.path.isdir(eachone_d) and eachone_d[-3:] == ".md":
                tmpfileinfo = []
                tmpfileinfo.append(eachone[:-3] + "\n" + self.read20words(eachone_d))
                tmpfileinfo.append(os.path.getmtime(eachone_d))
                #tmpfileinfo.append(self.addPictureToList(eachone_d))
                fileList.append(tmpfileinfo)
        if len(fileList) > 1:
            fileList.sort(key=operator.itemgetter(1), reverse=True)
        return fileList
    
    def addPictureToList(self, filepath):
        returnStr = " "
        readHandle = open(filepath, "r", encoding='UTF-8')
        while True:
            oneline = readHandle.readline()
            if oneline:
                if "![](" in oneline and ")" in oneline.split("![](")[1]:
                    shotfile = (oneline.split("![](")[1]).split(")")[0]
                    realfile = os.path.join(self.listfileDir, shotfile)
                    if os.path.exists(realfile):
                        returnStr = realfile
            else:
                break
        readHandle.close()
        return returnStr
    
    def read20words(self, filepath):
        returnStr = ""
        readHandle = open(filepath, "r", encoding='UTF-8')
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
