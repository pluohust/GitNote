#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, getpass
import LogOn
import main, FileAll, GitNote

class Init:
    def __init__(self):
        self.exist = True
        main.gitNoteHome = "/home/"+getpass.getuser()+"/.GitNote"
        main.gitNoteNoteHome = "/home/"+getpass.getuser()+"/.GitNote/Notes"
        if not os.path.exists(main.gitNoteHome):
            self.exist = False
            os.makedirs(main.gitNoteHome)
            os.makedirs(main.gitNoteNoteHome)
            print("No .GitNOte")
        if not os.path.exists(main.gitNoteNoteHome):
            main.gitExist = False
            os.makedirs(main.gitNoteNoteHome)
            print("No Notes")
        if not os.path.exists(os.path.join(main.gitNoteHome, "config")):
            self.exist = False
            print("NO config:" + os.path.join(main.gitNoteHome, "config"))
        if not os.path.exists(os.path.join(main.gitNoteNoteHome, ".git")):
            main.gitExist = False
        if not self.exist:
            self.logWin = LogOn.LogOn()
        else:
            FileAll.readConfig()
            main.setGitEnv()
            main.myGitNote = GitNote.GitNote()