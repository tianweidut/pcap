#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2011-9-2

@author: tianwei

func:针对本地文件进行预处理，通过规则表达式进行筛选pcap，并保存到./pcap_file/YYMMDD_HH:MM:SS_pre.pcap
'''
import sys,string,os,time,commands
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

preThreadFlag = True        #预处理线程是否终止

class preprocessThread(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        self.exiting = False
        self.argv  = ""             #最终命令行
        self.final = ""             #规则字符串
        self.filePre = []           #存储待处理的文件名，绝对地址
        self.destFile = ""          #目标文件名
        
    def __del__(self):
        self.exiting = True
    
    def render(self,dumpStr,filePre):
        self.argv = dumpStr
        self.filePre = filePre
        self.start() 
    
    def run(self):
        i = 0
        while i < len(self.filePre):
            self.destFile = './pcap_file/' +str(time.strftime("%Y%m%d_%H:%M:%S_local", time.localtime(time.time())))+'.pcap'   
            self.final = "tcpdump -s 0 -r " + self.filePre[i] + " " + self.argv + " -w " + self.destFile 
            print self.final
            (status,out) = commands.getstatusoutput(self.final)
            if status == 0:
                print self.destFile
                self.returnFileName(self.destFile)   #完成一次处理，发射完成信号，传递文件名称
            i = i + 1
        print 'finish File'
        self.emit(SIGNAL('finishAllFile()'))
            
            
    def returnFileName(self,str):
        str = unicode(str,'utf-8')
        self.emit(SIGNAL('returnFileNamePre(QString)'),str)    
    
        