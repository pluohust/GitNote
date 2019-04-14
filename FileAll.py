#!/usr/bin/python3
# -*- coding: utf-8 -*-

import main
import getpass

def storeConfig():
    writeHandle = open("/home/"+getpass.getuser()+"/.GitNote/config", 'w')
    writeHandle.write(main.userName + '\n')
    writeHandle.write(main.password + '\n')
    writeHandle.write(main.gitUrl + '\n')
    writeHandle.close()

def readConfig():
    readHandle = open("/home/"+getpass.getuser()+"/.GitNote/config", 'r')
    main.userName = readHandle.readline().strip()
    main.password = readHandle.readline().strip()
    main.gitUrl = readHandle.readline().strip()