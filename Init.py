#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
import LogOn

class Init:
    def __init__(self):
        self.exist = True
        if not os.path.exists("~/.GitNote"):
            self.exist = False
            os.makedirs("~/.GitNote")
            os.makedirs("~/.GitNote/Notes")
        if not os.path.exists("~/.GitNote/Notes"):
            self.exist = False
            os.makedirs("~/.GitNote/Notes")
        if not os.path.exists("~/.GitNotes/config"):
            self.exist = False
        if not self.exist:
            self.logWin = LogOn.LogOn()