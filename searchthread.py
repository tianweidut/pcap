#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2011-10-24

@author: tianwei
'''
import sys,string,os,commands
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

searchThread = True

class searchThread(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        self.exiting = False
    def __del(self):
        self.exiting = True
        self.wait()
    def render(self):
        self.start()
    def run(self):
        os.popen(r'python searchMain.py').read()