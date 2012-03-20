#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2011-9-3

@author: tianwei

func:数据库连接
'''

import sys
from PyQt4 import QtSql,QtGui,QtCore

def dbconnect():    #数据库初始连接
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName("127.0.0.1")
    db.setDatabaseName("dbPcap")
    db.setUserName("root")
    db.setPassword("1")
    ok = db.open()
    if not ok:
        QtGui.QMessageBox.critical(None, 
                                   QtGui.qApp.tr("cannot open database!!!"), 
                                   QtGui.qApp.tr("unable to establish a database connection\n" "please contract QQ:416774905 tianweidut *_*"), 
                                   QtGui.QMessageBox.Cancel)
        return False
    else:
        return True


def createDBTable():        #创建数据库表，待选
    pass

def initModel(model,tableName):       #模型初始化
    model.setTable(tableName)
    
    model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    
    model.setHeaderData(0,QtCore.Qt.Horizontal,"id")
    model.setHeaderData(1,QtCore.Qt.Horizontal,"srcPort")    
    model.setHeaderData(2,QtCore.Qt.Horizontal,"destPort")
    model.setHeaderData(3,QtCore.Qt.Horizontal,"protocol")     
    model.setHeaderData(4,QtCore.Qt.Horizontal,"srcIp")
    model.setHeaderData(5,QtCore.Qt.Horizontal,"dstIp")    
    model.setHeaderData(6,QtCore.Qt.Horizontal,"data")

    model.select()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    