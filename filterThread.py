'''
Created on 2011-8-26

@author: sytmac
'''
#-*-encoding utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from readpcapfile import *
from framedata import *
import time
import re
import commands
from PyQt4 import QtSql,QtGui
protocol_filter={'tcp':1,
                 'udp':2,
                 'icmp':3,
                 'igmp':4,
                 'ip':5,
                 'arp':6,
                 'rarp':7,
                 'ipx':8,
                 'all':0
                 }

class filterThread(QThread):
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        self.exiting = False
       
    def __del__(self):
        self.exiting = True
       
    def render(self,argv1=[]):   
        print argv1
        self.preFile=argv1       
        self.start()
    def run(self):
         
        self.filterthread() 
        self.emit(SIGNAL('finishAllFileFilter()'))
    
    def filterthread(self):
        
        #app = QtGui.QApplication(sys.argv)
        db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName("127.0.0.1")
        db.setDatabaseName("dbPcap")
        db.setUserName("root")
        db.setPassword("1")
        ok = db.open()
        query = QtSql.QSqlQuery()
        
        for j in range(len(self.preFile)):
            count=0
            start=time.time()
            data =rdpcap(self.preFile[j])
            ftxt = open(self.preFile[j]+'.txt','w')
            #args=protocol_filter[sys.argv[1]]
            #print args
            for i in range(len(data)):
                strs = data[i][1]
                test = Netlayer(strs)
                test.decode()
                list=test.decodeNetlayer(0)
                if list==None:
                    ftxt.write('')
                
                writing=str(list)        
                #ftxt.write(re.sub('[\\[\\]]','',writing)+'\n')
                writing=re.sub('[\\[\\]]','',writing)
                ftxt.write(re.sub('[\'\']','',writing)+'\n')
                #ftxt.write(writing+'\n')
                count+=1
            print count
            
            sql_execute="load data local infile '"+self.preFile[j]+".txt"+"' ignore into table text  fields terminated by ', ' lines terminated by '\n' (srcPort,dstPort,protocol,srcIp,dstIp,data);"
            #sql_execute="select * from text"
           
            print  sql_execute
            query.exec_("use dbPcap;")
            query.exec_(sql_execute)
            
            command='rm '+self.preFile[j]+'.txt  -f'
            (status,out) = commands.getstatusoutput(command)
            print command
            #while query.next():
                #print query.value(0).toInt(),query.value(1).toString(),query.value(2).toString(),query.value(3).toString(),query.value(4).toString(),query.value(5).toString(),query.value(6).toString()
            end=time.time()
            print "cost all time:%s"%(end-start)
            
            
            
    
