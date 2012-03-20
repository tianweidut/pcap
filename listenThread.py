#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2011-9-1

@author: tianwei

func:执行tcpdump 命令行程序，解决挂起和线程暂停问题
'''
import sys,string,os,time,commands
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

ListenThreadFlag = True     #线程是否终止标志

class listenThread(QThread):    #监听线程，启动tcpdump
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        self.exiting = False
        self.dumpArgv = ''
        self.file = ''
    def __del__(self):
        self.exiting = True
        self.wait()
    def render(self,dumpStr):       #输入tcpdump部分字符串
        self.dumpArgv = dumpStr
        self.final = ''
        self.start()
    
    def returnFileName(self,str):
        str = unicode(str,'utf-8')
        self.emit(SIGNAL("returnFileName(QString)"),str)
    
    #不能直接调用，通过render传递信息，重写run方法
    def run(self):
        while ListenThreadFlag:
            #self.file = './pcap_file/'+str(time.strftime("%Y%m%d", time.localtime(time.time())))+'/'+str(time.strftime("%H:%M%S", time.localtime(time.time())))+'.pcap'
            self.file = './pcap_file/'+str(time.strftime("%Y%m%d_%H:%M:%S_net", time.localtime(time.time())))+'.pcap'            
            self.final = self.dumpArgv + ' -w ' + self.file
            print self.final
            (status,out) = commands.getstatusoutput(self.final)   #此处python线程挂起
            if status == 0 :     #成功运行或killall结果
                #将当前文件名保存到待处理文件名列表中
                #发射返回当前文件名
                if ListenThreadFlag == False:
                    print 'stop signal'
                    break;
                else:
                    print self.file
                    self.returnFileName(self.file)
                