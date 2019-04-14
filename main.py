#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
import git
from PyQt5.QtWidgets import QApplication
import Init, GitNote

userName = ""
password = ""
gitUrl = ""

gitExist = True

myGitNote = ""

def setGitEnv():
    os.environ['GIT_ASKPASS'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'askpass.py')
    os.environ['GIT_USERNAME'] = userName
    os.environ['GIT_PASSWORD'] = password

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myInit = Init.Init()
    sys.exit(app.exec_())