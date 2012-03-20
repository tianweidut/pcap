#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2011-9-1

@author: tianwei

func:pcap分析程序主界面
'''
import sys,string,os,commands
from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from maingraph import Ui_Form               #图形界面导入
import listenThread,preprocessThread        #监听线程 预处理线程导入
import subprocess                           #启动其他python程序
import findfiles
from readpcapfile import *
from framedata import  *
import filterThread
import searchthread

TCPDUMPNUM = 500000                #单个获取包数量 50w

class MyForm(QWidget):          #定义界面事件响应
    def __init__(self):
        QWidget.__init__(self,parent=None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #系统初始化变量/线程初始化
        #网络获取模块变量
        self.eth0           = "eth0"    #默认选择eht0网卡
        self.ruleListen     = ""        #监听规则表达式，默认为空
        self.keyWordListen  = ""        #关键字选择
        self.finalListen    = ""        #合并后的字符串
        self.captureFile    = {}        #保存已经捕获的文件名称
        #本地获取文件模块变量
        self.ruleProcess    = ""        #处理规则
        self.keyWordProcess = ""        #处理关键字
        self.preFile        = []        #本地预处理文件名保存
        self.preOkFile      = []        #本地预处理完成文件名保存

        #信号-槽
        self.connect(self.ui.btn_onlyListen, SIGNAL('clicked()'),self.onlyListen)       
        self.connect(self.ui.btn_search,SIGNAL('clicked()'),self.searchUI)
        self.connect(self.ui.btn_filtertoDB, SIGNAL('clicked()'),self.filtertoDB)
        #self.connect(self.ui.btn_listenToSaveDB, SIGNAL('clicked()'),self.listenToSaveDB)
        self.connect(self.ui.btn_selectFile, SIGNAL('clicked()'),self.selectFile)
        self.connect(self.ui.btn_stopListen, SIGNAL('clicked()'),self.stopListen)
        self.connect(self.ui.btn_clearSelectedFile, SIGNAL('clicked()'),self.clearSelected)

    def searchUI(self):
        #启动查询界面
        self.searchThread = searchthread.searchThread()
        self.connect(self.searchThread, SIGNAL("finished()"),self.updateUi)
        self.searchThread.render()
        
    
    def clearSelected(self):
        #清除选择文件
        self.debug("清除选择文件") 
        self.preOkFile[:]=[]
        #清空预处理文件列表
        self.preFile[:]=[]
           
    def onlyListen(self):
        self.ui.label_listenState.setText(unicode('正在监听...','utf-8'))
        self.ListenStringProcess()
                        
    def returnFileTCPdump(self,tmp):
        #每当单个文件处理capture完成，进行-->名称列表添加
        self.captureFile[str(tmp)] = False
        
    def returnFilePreProcess(self,tmp):
        #每当单个文件处理pre完成，进行-->名称列表添加
        self.preOkFile.append(str(tmp))
          
    def debug(self,str):
        #str = str + '\n'
        self.ui.text_debug.append(unicode(str,'utf-8'))     
            
    def filtertoDB(self):
        self.ui.label_processState.setText(unicode('正在处理...','utf-8'))
        
        #step1.获取字符串
        self.ruleProcess = str(self.ui.lineEdit_ruleLocal.text())
        self.keyWordProcess = str(self.ui.lineEdit_KeyWordLocal.text())
        #step2.文件列表验证
        if len(self.preFile) == 0:
            self.debug("\t[错误]-->[未选择本地文件]")
            return
        else:
            self.debug("...[本地文件选择]载入"+str(len(self.preFile))+"个预处理文件")
            print self.preFile
        #step3.启动线程进行预处理
        self.preprocessThread = preprocessThread.preprocessThread()          #创建线程
        self.connect(self.preprocessThread, SIGNAL("finished()"),self.updateUi)
        self.connect(self.preprocessThread, SIGNAL("terminated()"),self.updateUi)
        self.connect(self.preprocessThread, SIGNAL("returnFileNamePre(QString)"),self.returnFilePreProcess)
        self.connect(self.preprocessThread, SIGNAL("finishAllFile()"),self.finishFile)        
        self.preprocessThread.render(self.ruleProcess,self.preFile)
                
        #step4.启动pcap文件分析线程池，并将其存储到数据库中
            #字典
        print self.preOkFile
        self.filterLocalThread = filterThread.filterThread()
        self.connect(self.filterLocalThread, SIGNAL("finished()"),self.updateUi)
        self.connect(self.filterLocalThread, SIGNAL("terminated()"),self.updateUi)
        self.connect(self.filterLocalThread, SIGNAL("finishAllFileFilter()"),self.finishFileLocalFilter) 
        
        #此处可以追加其他接受信号
        #print self.preOkFile
        self.filterLocalThread.render(self.preFile)
        #print self.preOkFile
        self.preOkFile[:]=[]
        
    
    def finishFileLocalFilter(self):
        self.debug("*_* 完成本地所有文件分析并保存到数据库中 *_*")
    
    def finishFileNetFilter(self):
        self.debug("*_* 完成网络所有文件分析并保存到数据库中 *_*")
    
    def finishFile(self):
        self.debug("*_* 完成所有本地文件预处理工作 *_*")
        
    def listenToSaveDB(self):
        self.ui.label_listenState.setText(unicode('正在监听...','utf-8'))
        self.ListenStringProcess()
        #启动处理线程,并将其保存到数据库
                
    def selectFile(self):
        #清空预处理文件列表
        self.preFile[:]=[]
        #打开选择文件窗口
        cmd = ["python","findfiles.py"]
        subprocess.call(cmd,0,None,None,None,None)
        print "--------------"
        file = open(findfiles.fileName,"r")
        for tmp in file.readlines():
            tmp = tmp.strip()
            self.preFile.append(tmp)
            print tmp
        file.close()
        self.debug("选定 " + str(len(self.preFile)) + "个文件，等待选择处理")
                    
    def stopListen(self):       #停止监听
        self.ui.label_listenState.setText(unicode('停止监听','utf-8'))
        listenThread.ListenThreadFlag = False
        commands.getstatusoutput('killall -HUP tcpdump')  #将当前程序中tcpdump程序终止
    
    def updateUi(self):
        #此处需要验证是否有必要更新所有元素
        #self.ui.btn_clear.update()
        self.ui.btn_filtertoDB.update()
        #self.ui.btn_listenToSaveDB.update()
        self.ui.btn_onlyListen.update()
        self.ui.btn_search.update()
        self.ui.btn_selectFile.update()
        self.ui.btn_stopListen.update()
        #self.ui.tableView_DB.update()
           
    def ListenStringProcess(self):      #监听字符串预处理
        self.eth0 = str(self.ui.lineEdit_eth0.text())
        self.ruleListen = str(self.ui.lineEdit_ruleListen.text())
        self.keyWordListen = str(self.ui.lineEdit_keyWordListen.text())
        
        '''tcpdump 
            -i 端口
            -c 捕获包数量
            -w 写入指定文件中
            -s 截获数据包长度 -s 0 按照包长度自动调整，避免丢失数据包 
            ‘规则过滤’
        '''
        self.finalListen = "tcpdump -s 0 " + ' -i ' + self.eth0  +' -c ' + str(TCPDUMPNUM) + " '" + self.ruleListen + "' "
        print self.finalListen
        
        listenThread.ListenThreadFlag = True                     #单击后设定位True
        self.listenThread = listenThread.listenThread()          #创建线程
        self.connect(self.listenThread, SIGNAL("finished()"),self.updateUi)
        self.connect(self.listenThread, SIGNAL("terminated()"),self.updateUi)
        self.connect(self.listenThread, SIGNAL("returnFileName(QString)"),self.returnFileTCPdump)
        self.listenThread.render(self.finalListen)
        
if __name__ == '__main__':
    app   = QApplication(sys.argv)
    myapp = MyForm()        #界面实例化
    myapp.show()
    sys.exit(app.exec_())
     
