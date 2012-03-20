#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2011-10-24

@author: tianwei
'''

import sys,string,os,commands
from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4 import QtSql
import dbconnect
from search import searchUi

class MySearch(QWidget):
    def __init__(self):
        #界面初始化
        QWidget.__init__(self,parent=None)
        self.ui = searchUi()
        self.ui.setupUi(self)
        #数据库查询模块变量
        self.srcPort        = -1        #源端口
        self.destPort       = -1
        self.srcIP          = "0.0.0.0"
        self.destIP         = "0.0.0.0"
        self.protocol       = "TCP"     #统一大小写
        self.keywordSearch  = ""
        #信号和槽声明
        self.connect(self.ui.btn_clear, SIGNAL('clicked()'),self.clear)
        self.connect(self.ui.btn_connectDB, SIGNAL('clicked()'),self.connectDB)
        self.connect(self.ui.btn_search, SIGNAL('clicked()'),self.search)
        #控件初始化
        self.ui.btn_search.setEnabled(False)
        
    def connectDB(self):
        #数据库连接
        if not dbconnect.dbconnect():
            self.debug("\t[错误]-->[数据库未能打开]")
            return
        
        self.model = QtSql.QSqlRelationalTableModel()
        
        dbconnect.initModel(self.model, "text")
        self.ui.tableView_DB.setModel(self.model)
        self.ui.tableView_DB.setItemDelegate(QtSql.QSqlRelationalDelegate(self.ui.tableView_DB))
        self.ui.tableView_DB.setWindowTitle("tianwei")
        
        self.ui.btn_connectDB.setEnabled(False)
        self.ui.btn_search.setEnabled(True)
    def clear(self):
        self.ui.lineEdit_KeyWordDB.clear()
        self.ui.lineEdit_srcIP.clear()
        self.ui.lineEdit_destIP.clear()
        self.ui.lineEdit_destPort.clear()
        self.ui.lineEdit_srcPort.clear()
        self.ui.lineEdit_protocol.clear()
        
    def search(self):
        #载入输入框
        destIP      = str(self.ui.lineEdit_destIP.text())
        destPort    = str(self.ui.lineEdit_destPort.text())
        srcIP       = str(self.ui.lineEdit_srcIP.text())
        srcPort     = str(self.ui.lineEdit_srcPort.text())
        protocol    = str(self.ui.lineEdit_protocol.text())
        keyword     = str(self.ui.lineEdit_KeyWordDB.text())
        #查询语句
        query = QtSql.QSqlQuery()
        #拼接语句
        val = "select * from text where 1=1 "
        if destPort != '':
            val = val + ' and dstPort="' + destPort+'"'
        if destIP != '':
            val = val + ' and dstIp="' + destIP+'"'
        if srcIP != '':
            val = val + ' and srcIp="' + srcIP+'"'
        if srcPort != '':
            val = val + ' and srcPort="' + srcPort+'"'
        if protocol != '':
            val = val + ' and protocol="' + protocol+'"'
        if keyword != '':
            val = val + ' and data LIKE "%' + keyword + '%"'     
        
        print val
        query.exec_(val)
        
        self.model.setQuery(query)
        self.ui.tableView_DB.setModel(self.model)   
             
if __name__ == '__main__':
    app   = QApplication(sys.argv)
    myapp = MySearch()        #界面实例化
    myapp.show()
    sys.exit(app.exec_())