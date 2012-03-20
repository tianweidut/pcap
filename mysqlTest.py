#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2011-9-3

@author: tianwei

func: Mysql 数据库基本测试
'''
import sys
from PyQt4 import QtSql,QtGui


app = QtGui.QApplication(sys.argv)

db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("127.0.0.1")
db.setDatabaseName("dbPcap")
db.setUserName("root")
db.setPassword("1")
ok = db.open() 

print ok

query = QtSql.QSqlQuery()
#query.exec_("load data local infile '/home/jacob/workspace/pcap/src/stamp.pcap.txt'  ignore into table text character set gbk fields terminated by ','enclosed by '''' lines terminated by '\n' (srcPort,dstPort,protocol,srcIp,dstIp,data);")
#query.exec_("insert  into text (srcPort,dstPort,protocol,srcIp,dstIp,data) values(1,1,1,1,1,1) ")
query.exec_("select * from text")
while query.next():
    print query.value(0).toInt(),query.value(1).toString(),query.value(2).toString(),query.value(3).toString(),query.value(4).toString(),query.value(5).toString(),query.value(6).toString()
