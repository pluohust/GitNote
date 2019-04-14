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
    main.myGitNote.setMenuClone()

class GitNote(QMainWindow, GitNoteUi.Ui_GitNoteUi):
    def __init__(self, parent=None):
        super(GitNote, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.show()
        
    def initUi(self):
        if not main.gitExist:
            self.cloneGit()
    
    def cloneGit(self):
        if not main.gitExist:
            self.menu_update.setTitle("克隆中")
            cloneThread = threading.Thread(target=runClone, name="cloneThread")
            cloneThread.start()
    
    def setMenuClone(self):
        self.menu_update.setTitle("更新")