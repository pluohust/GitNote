#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
import GitNoteUi
import main
import git
import os, getpass, threading

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
        
    def initUi(self):
        if not main.gitExist:
            self.mycloneGit()
        self.pushButton_update.clicked.connect(self.myupdateGit)
    
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