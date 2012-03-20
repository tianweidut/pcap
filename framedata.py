'''
Created on 2011-8-26

@author: sytmac
'''
import os,sys
import re
import string
EtherType = {'0x0600':'XEROX NS IDP',
    '0x0660':'DLOG',
    '0x0661':'DLOG',
    '0x0800':'IP',
    '0x0801':'X.75',
    '0x0802':'NBS',
    '0x0803':'ECMA',
    '0x0804':'Chaosnet',
    '0x0805':'X.25',
    '0x0806':'ARP',
    '0x0808':'Frame Relay ARP',
    '0x6559':'Raw Frame Relay',
    '0x8035':'RARP',
    '0x8037':'Novell Netware IPX',
    '0x809B':'Ether Talk',
    '0x80d5':'IBM SNA Service over Ethernet',
    '0x80f3':'AARP',
    '0x8100':'EAPS',
    '0x8137':'IPX',
    '0x814c':'SNMP',
    '0x86dd':'IPv6',
    '0x880b':'PPP',
    '0x880c':'GSMP',
    '0x8847':'MPLS(unicase)',
    '0x8848':'MPLS(multicast)',
    '0x8863':'PPPoE(Discovery stage)',
    '0x8864':'PPPoE(ppp session stage)',
    '0x88bb':'LWAPP',
    '0x88cc':'LLDP',
    '0x8e88':'EAP over LAN',
    '0x9000':'Loopback',
    '0x9100':'VLAN Tag PI',
    '0x9200':'VLAN Tag PI',
    '0xffff':'Reservations'
    }
ProtocolType={20:'FTP',
              21:'FTP',
              22:'SSH',
              23:'Telnet',
              25:'SMTP',
              26:'RSFTP',
              39:'RLP',
              53:'DNS',
              57:'MTP',
              67:'DHCP',
              68:'DHCP',
              69:'TFTP',
              80:'HTTP',
              107:'Telnet',
              109:'POP',
              110:'POP3',
              111:'SUN',
              115:'SFTP',
              153:'SGMP',
              137:'NetBIOS',
              138:'NetBIOS',
              194:'IRC',
              366:'SMTP',
              546:'DHCPV6',
              1900:'SSDP',
              1935:'RTMP',
              5353:'MDNS',
              5355:'LLMNR',
              6667:'IRC',
              9200:'WSP'
             }

class Protocol(object):
    
    def __init__(self):
        pass

# transform like '\x01\x0e\0xb0' to '0x010eb0'
    def str_to_hex(self,strs):

        hex_data =''
        for i in range(len(strs)):

            tem = ord(strs[i])
            
            tem = hex(tem)
            
            if len(tem)==3:
                
                tem = tem.replace('0x','0x0')
            tem = tem.replace('0x','')
            
            hex_data = hex_data+tem

        return '0x'+hex_data
    
   
class Ethernet(Protocol):
    
    def __init__(self,datastr=None):
        
        self.dstMac = None
        
        self.srcMac = None
        
        self.ethertype = None
        
        self.len = None
        
        self.type = None
        
        self.datastr = datastr
        
        self.listEthernet=[]
        
        self.upperType=None
        
        self.transportType=None
        
        self.netLayertype=None
        
        self.count=0
        
    def decode(self): 
        
        #global count
              
        #self.count+=1
            
        #self.listEthernet.append(self.count)

        tem = self.str_to_hex(self.datastr[0:6])
        
        self.dstMac = tem[2:4]+':'+tem[4:6]+':'+tem[6:8]+':'+tem[8:10]+':'+tem[10:12]+':'+tem[12:14]
        
        tem = self.str_to_hex(self.datastr[6:12])
        
        self.srcMac = tem[2:4]+':'+tem[4:6]+':'+tem[6:8]+':'+tem[8:10]+':'+tem[10:12]+':'+tem[12:14]
        
        self.unknow = self.str_to_hex(self.datastr[12:14])
        
        tem = int(self.unknow,16)
        
        dstMacstr = self.dstMac
        
        srcMacstr = self.srcMac
        
        if tem<=1500:
            
            self.ethertype='IEEE 802.3 Ethernet'
            
            self.len =tem
            
            lenstr = 'Length: '+str(self.len)
            
            IEEE802_type=self.str_to_hex(self.datastr[14:14+2])
            
            if IEEE802_type=='0xffff':#802.3 raw,for IPX/SPX only
                
                self.netLayertype=='0x8137'
            
                self.datastr=self.datastr.replace(self.datastr[14:14+2],"",1)
                
            elif IEEE802_type=="0xaaaa":#Ethernet 802.3 SNAP
                
                self.datastr=self.datastr.replace(self.datastr[12:20],"",1)
                
                self.unknow = self.str_to_hex(self.datastr[12:12+2])
                
            else:#Ethernet 802.3 SAP
                
                self.datastr=self.datastr.replace(self.datastr[14:14+3],"",1)
                

        elif tem>=1536:

            self.ethertype='Eternet II'
            
        #self.listEthernet.append(dstMacstr)
            
        #self.listEthernet.append(srcMacstr)
        #return self.unknow
       
class Netlayer(Ethernet):
    
    
    def __init__(self,datastr):
        
        Ethernet.__init__(self,datastr)
        
        self.dstIp=None
        
        self.srcIp=None
        
        
        self.srcPort=None
        
        self.dstPort=None
        
        self.data=None
        
        
    def decodeIpfromHexToDec(self,string): #decode ip ,transform hex to decimal
        
        ip4=int(string[2:4],16)
        
        ip3=int(string[4:6],16)
        
        ip2=int(string[6:8],16)
        
        ip1=int(string[8:10],16)
        
        return str(ip4)+'.'+str(ip3)+'.'+str(ip2)+'.'+str(ip1)
    
    def Tcpdecode(self,location):
        
        srcPort=self.str_to_hex(self.datastr[location:location+2])
                #print srcPort
        self.srcPort=int(srcPort[2:6],16)
        
        self.listEthernet.append(str(self.srcPort))
                
        dstPort=self.str_to_hex(self.datastr[location+2:location+4])
      
                
        self.dstPort=int(dstPort[2:6],16)
        
          
        self.listEthernet.append(str(self.dstPort))
                
        # for protcol type
        if ProtocolType.has_key(self.srcPort):
                    
            self.upperType=ProtocolType[self.srcPort]
                    
        if ProtocolType.has_key(self.dstPort):
                    
            self.upperType=ProtocolType[self.dstPort] 
                
        #print self.transportType
        #tcp data decoding
        
                
        length=(int(self.str_to_hex(self.datastr[location+12:location+12+1]),16)&0xf0)>>2
                
        self.data=re.sub(',','',self.datastr[location+length:])
        
    def Udpdecode(self,location):
        
        srcPort=self.str_to_hex(self.datastr[location:location+2])
        #print srcPort
        self.srcPort=int(srcPort[2:6],16)
        
        self.listEthernet.append(str(self.srcPort))
                
        dstPort=self.str_to_hex(self.datastr[location+2:location+4])
                
        self.dstPort=int(dstPort[2:6],16)
        
        self.listEthernet.append(str(self.dstPort))
                
        # for protcol type
        if ProtocolType.has_key(self.srcPort):
                    
            self.upperType=ProtocolType[self.srcPort]
            
                    
        if ProtocolType.has_key(self.dstPort):
                    
            self.upperType=ProtocolType[self.dstPort] 
                          
        self.data=re.sub(',','',self.datastr[location+8:])
        
    def ipv4addr(self):#for TCP , UDP AND TCMP of ipv4 version 
        
        tem=self.str_to_hex(self.datastr[13+13:13+17])
            
        self.srcIp=self.decodeIpfromHexToDec(tem)
            
        tem=self.str_to_hex(self.datastr[13+17:13+21])
            
        self.dstIp=self.decodeIpfromHexToDec(tem)
            
        self.listEthernet.append(self.srcIp)
            
        self.listEthernet.append(self.dstIp)
        
        #print self.listEthernet    
        
    def ipv6addr(self):# for TCP AND UDP and ICMP of ipv6 version
        
        temp=self.str_to_hex(self.datastr[14+8:14+24])
            
        self.srcIp=temp[2:6]+':'+temp[6:10]+':'+temp[10:14]+':'+temp[14:18]+':'+temp[18:22]+':'+temp[22:26]+':'+temp[26:30]+':'+temp[30:34]
            
        temp=self.str_to_hex(self.datastr[14+24:14+40])
            
        self.dstIp=temp[2:6]+':'+temp[6:10]+':'+temp[10:14]+':'+temp[14:18]+':'+temp[18:22]+':'+temp[22:26]+':'+temp[26:30]+':'+temp[30:34]
            
        self.listEthernet.append(self.srcIp)
            
        self.listEthernet.append(self.dstIp)
            
         
                
        
    def decodeNetlayer(self,protocol):
        
        self.netLayertype=self.unknow #judge whether type is Ip
        
        #print self.netLayertype

        #print protocol
        if (self.netLayertype=='0x0800') and (protocol ==0 or protocol ==1 or protocol ==2 or protocol ==3 or protocol ==4 or protocol==5):# ipv4
            
            self.transportType=self.str_to_hex(self.datastr[13+10:13+11])
            
            #print self.transportType
            
            if (self.transportType=='0x06')and(protocol ==1 or protocol ==0 or protocol ==5):
                
                self.transportType= 'TCP'
                
                self.Tcpdecode(34)
                
                if self.upperType==None:
                    
                    self.upperType=self.transportType
                
                self.listEthernet.append(self.upperType)              
                
                self.ipv4addr()
                
                self.listEthernet.append( self.data)
                
                return  str(self.listEthernet)
                #print self.datastr
  
            elif (self.transportType=='0x11')and(protocol ==2 or protocol ==0 or protocol ==5):
                
                self.transportType= 'UDP'
              
                self.Udpdecode(34)
                
                if self.upperType==None:
                    
                    self.upperType=self.transportType
                
                self.listEthernet.append(self.upperType)
                
                self.ipv4addr()
                
                #print self.listEthernet
                
                self.listEthernet.append( self.data)
                
                #print self.data
                
                return  str(self.listEthernet)
            elif (self.transportType=='0x01')and(protocol ==3 or protocol ==0 or protocol ==5):
                
                self.transportType='ICMP'
                
                self.srcPort=""
                
                self.dstPort=""
                
                self.listEthernet.append(self.srcPort)
                
                self.listEthernet.append(self.dstPort)
                
                self.upperType=self.transportType
                
                self.listEthernet.append(self.upperType)
                
                self.ipv4addr()
                
                self.data=re.sub(',','',self.datastr[34:])
                
                self.listEthernet.append(self.data)
                
                
                return  str(self.listEthernet)
                
            elif (self.transportType=='0x02')and(protocol ==4 or protocol ==0 or protocol ==5):
                
                self.transportType='IGMP'
                
                self.srcPort=""
                
                self.dstPort=""
                
                self.listEthernet.append(self.srcPort)
                
                self.listEthernet.append(self.dstPort)
                               
                self.upperType=self.transportType
                
                self.listEthernet.append(self.upperType)
                
                self.ipv4addr()
                
                self.listEthernet.append('')
                
                return  str(self.listEthernet)
        
             
        elif (self.netLayertype=='0x86dd') and (protocol ==0 
                or protocol ==1 or protocol ==2 or protocol ==3 or protocol ==4 or protocol==5):#ipv6
            
            self.transportType=self.str_to_hex(self.datastr[14+6:14+7])
            
            if (self.transportType=='0x06')and(protocol ==1 or protocol ==0 or protocol ==5):
                
                self.transportType= 'TCP'
                
                self.Tcpdecode(54)
                
                if self.upperType==None:
                    
                    self.upperType=self.transportType
                
                self.listEthernet.append(self.upperType)
                
                self.ipv6addr()
                     
                self.listEthernet.append( self.data)
                
                
                return  str(self.listEthernet)
                  
            elif (self.transportType=='0x11')and (protocol ==2 or protocol ==0 or protocol ==5):
                
                self.transportType= 'UDP'
                
                self.Udpdecode(54)
                
                if self.upperType==None:
                    
                    self.upperType=self.transportType
                
                self.listEthernet.append(self.upperType)
                
                self.ipv6addr()
                
                self.listEthernet.append( self.data)
                
                #m=re.findall('/[[.*]/]',str(self.listEthernet))
                
                #return  self.listEthernet[0]+self.listEthernet[1]+self.listEthernet[2]+self.listEthernet[3]+self.listEthernet[4]+self.listEthernet[5]+self.listEthernet[6]      
        
                return  str(self.listEthernet)
            
            elif (self.transportType=='0x3a'):#and (protocol ==3 or protocol ==0 or protocol ==5):
                
                self.transportType='ICMPV6'
                
                self.srcPort=" None"
                
                self.dstPort=" None"
                
                self.listEthernet.append(self.srcPort)
                
                self.listEthernet.append(self.dstPort)
                
                
                self.upperType=self.transportType
                
                self.listEthernet.append(self.upperType)
                
                self.ipv6addr()
                
                self.data=re.sub(',','',self.datastr[54:])
                
                self.listEthernet.append(self.data)
                
                return  str(self.listEthernet)
            
            elif (self.transportType=='0x02')and(protocol ==4 or protocol ==0 or protocol ==5):
                
                self.transportType='IGMPV6'
                
                self.srcPort="None"
                
                self.dstPort=" None"
                
                self.listEthernet.append(self.srcPort)
                
                self.listEthernet.append(self.dstPort)
                
                
                self.upperType=self.transportType
                
                self.listEthernet.append(self.upperType)
                           
                self.ipv6addr()
                
                self.listEthernet.append("")
            
                return  str(self.listEthernet)
            
            
        elif (self.netLayertype=='0x0806')and (protocol ==6 or protocol ==0):
            
            self.netLayertype='ARP'
            
            self.listEthernet.append("")
            
            self.listEthernet.append("")
            
            self.listEthernet.append(self.netLayertype)
            
            tem=self.str_to_hex(self.datastr[14+14:14+14+4])
            
            self.srcIp=self.decodeIpfromHexToDec(tem)
            
            tem=self.str_to_hex(self.datastr[14+24:14+32])
            
            self.dstIp=self.decodeIpfromHexToDec(tem)
            
            self.listEthernet.append(self.srcIp)
            
            self.listEthernet.append(self.dstIp)          

            self.data="who has "+self.dstIp+" tell "+self.srcIp
            
            self.listEthernet.append(self.data)
            
            return str(self.listEthernet)
        
        elif (self.netLayertype=='0x8035')and (protocol ==7 or protocol ==0):
            
            self.netLayertype='RARP'

            self.listEthernet.append("")
            
            self.listEthernet.append("")
                        
            self.listEthernet.append(self.netLayertype)
            
            tem=self.str_to_hex(self.datastr[14+14:14+14+4])
            
            self.srcIp=self.decodeIpfromHexToDec(tem)
            
            tem=self.str_to_hex(self.datastr[14+24:14+32])
            
            self.dstIp=self.decodeIpfromHexToDec(tem)
            
            self.listEthernet.append(self.srcIp)
            
            self.listEthernet.append(self.dstIp)
                       
            self.listEthernet.append("")
            
            return str(self.listEthernet)
        
        elif (self.netLayertype=='0x8137')and (protocol ==8 or protocol ==0):
            
            self.netLayertype='IPX'
            
            self.listEthernet.append("")
            
            self.listEthernet.append("")
            
            self.listEthernet.append(self.netLayertype)
            
            self.listEthernet.append(self.srcIp)
            
            self.listEthernet.append(self.dstIp)
    
            self.data=self.datastr[14:]
            
            self.listEthernet.append(self.data)
         
        elif (self.netLayertype!='0x8137' and self.netLayertype!='0x8035'
              
              and self.netLayertype!='0x0806'and self.netLayertype!='0x86dd'and self.netLayertype!='0x0800' and protocol==0):
            
            self.netLayertype='unknow'
            
            self.listEthernet.append("")
            
            self.listEthernet.append("")
            
            self.listEthernet.append(self.netLayertype)
            
            self.listEthernet.append('')
            
            self.listEthernet.append('')
    
            self.data=self.datastr[14:]
            
            self.listEthernet.append(self.data)
                        
            return  self.listEthernet
        
        #print self.netLayertype
        