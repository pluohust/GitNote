#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os, getpass
import LogOn
import main, FileAll, GitNote

class Init:
    def __init__(self):
        self.exist = True
        if not os.path.exists("/home/"+getpass.getuser()+"/.GitNote"):
            self.exist = False
            os.makedirs("/home/"+getpass.getuser()+"/.GitNote")
            os.makedirs("/home/"+getpass.getuser()+"/.GitNote/Notes")
            print("No .GitNOte")
        if not os.path.exists("/home/"+getpass.getuser()+"/.GitNote/Notes"):
            main.gitExist = False
            os.makedirs("/home/"+getpass.getuser()+"/.GitNote/Notes")
            print("No Notes")
        if not os.path.exists("/home/"+getpass.getuser()+"/.GitNote/config"):
            self.exist = False
            print("NO config:" + "/home/"+getpass.getuser()+"/.GitNote/config")
        if not os.path.exists("/home/"+getpass.getuser()+"/.GitNote/Notes/.git"):
            main.gitExist = False
        if not self.exist:
            self.logWin = LogOn.LogOn()
        else:
            FileAll.readConfig()
            main.setGitEnv()
            main.myGitNote = GitNote.GitNote()