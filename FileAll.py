#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main
import getpass, os

def storeConfig():
    writeHandle = open(os.path.join(main.gitNoteHome, "config"), 'w')
    writeHandle.write(main.userName + '\n')
    writeHandle.write(main.password + '\n')
    writeHandle.write(main.gitUrl + '\n')
    writeHandle.close()

def readConfig():
    readHandle = open(os.path.join(main.gitNoteHome, "config"), 'r')
    main.userName = readHandle.readline().strip()
    main.password = readHandle.readline().strip()
    main.gitUrl = readHandle.readline().strip()
