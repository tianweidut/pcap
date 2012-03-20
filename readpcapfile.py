'''
Created on 2011-8-26

@author: sytmac
'''
# !/usr/bin/python

#coding=utf-8

import struct 
def decode_PcapFileHeader(B_datastring):
    """   
        4 bytes       2 bytes     2 bytes     4 bytes    4 bytes   4 bytes   4 bytes
        ------------------------------------------------------------------------------
Header  | magic_num | ver_major | ver_minor | thiszone | sigfigs | snaplen | linktype|
        ------------------------------------------------------------------------------
    """
    header = {}

    header['magic_number'] = B_datastring[0:4]

    header['version_major'] = B_datastring[4:6]

    header['version_minor'] = B_datastring[6:8]

    header['thiszone'] = B_datastring[8:12]

    header['sigfigs'] = B_datastring[12:16]

    header['snaplen'] = B_datastring[16:20]

    header['linktype'] = B_datastring[20:24]

    return header

 

 

def decode_PcapDataPcaket(B_datastring):
    """   

          4 bytes    4 bytes    4 bytes 4 bytes   

        ----------------------------------------------

Packet  | GMTtime | MicroTime | CapLen | Len |  Data |

        ----------------------------------------------

       |------------Packet Header----------|

    """

    packet_num = 0

    packet_data = []

    header = {}

    data = ''

    i = 24

 

    while(i<len(B_datastring)):

        header['GMTtime'] = B_datastring[i:i+4]

        header['MicroTime'] = B_datastring[i+4:i+8]

        header['CapLen'] = B_datastring[i+8:i+12]

        header['Len'] = B_datastring[i+12:i+16]

 

        # the len of this packet

        packet_len = struct.unpack('I',header['CapLen'])[0]

        # the data of this packet

        data = B_datastring[i+16:i+16+packet_len]

      

        # save this packet data

        packet_data.append((header,data))

 

        i = i + packet_len+16

        packet_num += 1

          

    return packet_data


def rdpcap(fileName):

    filepcap = open(fileName,'rb')

    string_data = filepcap.read()

    packet_data = decode_PcapDataPcaket(string_data)

    return packet_data
