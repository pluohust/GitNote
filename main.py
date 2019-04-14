#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
import git
from PyQt5.QtWidgets import QApplication
import Init

userName = ""
password = ""
gitUrl = ""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myInit = Init.Init()
    sys.exit(app.exec_())