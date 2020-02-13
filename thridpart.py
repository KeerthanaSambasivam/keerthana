###########Networking###################
#!/usr/bin/env python3
import time
import os


#######variables Declaration#####################################################

cur_Packetsent=0
cur_Packetrecv =0
cur_OutRequest=0
cur_ActiveOpen =0 #No of TCP connections
cur_CurrentEstablish = 0 # TCP connection establish
cur_InSeg =0 #TCP segments
cur_OutSeg =0 # TCP out segments
cur_InDataGrams=0 ##UDP 
cur_OutDataGrams =0 ## UDP

pre_Packetsent=0
pre_Packetrecv =0
pre_OutRequest=0
pre_ActiveOpen =0 #No of TCP connections
pre_CurrentEstablish = 0 # TCP connection establish
pre_InSeg =0 #TCP segments
pre_OutSeg =0 # TCP out segments
pre_InDataGrams=0 ##UDP 
pre_OutDataGrams =0 ## UDP
interval = 5
speed=1000 ####Mb/s
class DataCollection:
    def sys_networking(self):
        ####First part########
        #snmpFileListj
        global cur_Packetsent,cur_Packetrecv ,cur_OutRequest,cur_ActiveOpen ,cur_CurrentEstablish ,cur_InSeg ,cur_OutSeg ,cur_InDataGrams,cur_OutDataGrams,pre_Packetsent,pre_Packetrecv,pre_OutRequest,pre_ActiveOpen,pre_CurrentEstablish,pre_InSeg,pre_OutSeg ,pre_InDataGrams ,pre_OutDataGrams 

 
        self.Packetsent=0
        self.Packetrecv =0
        self.OutRequest=0
        self.ActiveOpen =0 #No of TCP connections
        self.CurrentEstablish = 0 # TCP connection establish
        self.InSeg =0 #TCP segments
        self.OutSeg =0 # TCP out segments
        self.InDataGrams=0 ##UDP 
        self.OutDataGrams =0 ## UDP

        filesnmp = open("/proc/net/snmp","r")
        snmpfileRead = filesnmp.read()
        
        snmpFileList = snmpfileRead.split() 
        
        pre_Packetsent= cur_Packetsent
        pre_Packetrecv =cur_Packetrecv 
        pre_OutRequest= cur_OutRequest
        pre_ActiveOpen = cur_ActiveOpen #No of TCP connections
        pre_CurrentEstablish = cur_CurrentEstablish # TCP connection establish
        pre_InSeg = cur_InSeg  #TCP segments
        pre_OutSeg = cur_OutSeg # TCP out segments
        pre_InDataGrams= cur_InDataGrams ##UDP 
        pre_OutDataGrams = cur_OutDataGrams ## UDP

        cur_Packetsent = float(snmpFileList[21])
        cur_Packetrecv = float(snmpFileList[22])
        cur_OutRequest = float(snmpFileList[30])
		
       
        indexTcp = snmpFileList.index("Tcp:")
        
        cur_ActiveOpen =float(snmpFileList[indexTcp+21]) #No of TCP connections
        cur_CurrentEstablish = float(snmpFileList[indexTcp+22]) # TCP connection establish
        cur_InSeg = float(snmpFileList[indexTcp+26]) #TCP segments
        cur_OutSeg =float(snmpFileList[indexTcp+27]) # TCP out segments
        indexUDP = snmpFileList.index("Udp:")
        cur_InDataGrams =float(snmpFileList[indexUDP+9]) #No of TCP connections
        cur_OutDataGrams = float(snmpFileList[indexUDP+12]) # TCP connection establish

        self.Packetsent= (cur_Packetsent - pre_Packetsent)/interval
        self.Packetrecv =(cur_Packetrecv- pre_Packetrecv)/interval
        self.OutRequest=(cur_OutRequest -pre_OutRequest)/interval
        self.ActiveOpen = (cur_ActiveOpen + pre_ActiveOpen)/2 #No of TCP connections
        self.CurrentEstablish = (cur_CurrentEstablish + pre_CurrentEstablish)/2 # TCP connection establish
        self.InSeg = (cur_InSeg - pre_I nSeg)/interval #TCP segments
        self.OutSeg = (cur_OutSeg-pre_OutSeg)/interval # TCP out segments
        self.InDataGrams=  (cur_InDataGrams -pre_InDataGrams)/interval ##UDP 
        self.OutDataGrams = (cur_OutDataGrams -pre_OutDataGrams)/interval ## UDP
        print( "No of Ip packets sent = {0} ,No of packets received {1} and OutRequest = {2} ".format(self.Packetsent,self.Packetrecv,self.OutRequest))     
        print( "ActiveOpen = {0} ,CurrentEstablish ={1}, InSeg = {2} and OutSeg = {3} ".format(self.ActiveOpen, self.CurrentEstablish, self.InSeg,self.OutSeg))  
        print ("InDataGrams = {0} and OutDataGrams ={1}".format(self.InDataGrams, self.OutDataGrams))  
        
        ##############table################################################
        self.dict_tcp_upd={}
        self.connectioncount =0
        list_connection=[]
        filenames = os.listdir("/proc")
        fileTCPopen = open("/proc/net/tcp")
        fileTCPread =   fileTCPopen.readlines()
        
        fileTCPopen.close()
        for TCPline in fileTCPread:
            datalist_TCP = TCPline.split()
            protocol = "TCP"
            list_connection=[datalist_TCP[11],datalist_TCP[9],datalist_TCP[2],datalist_TCP[1],protocol]
            self.dict_tcp_upd.update({self.connectioncount:list_connection})
            self.connectioncount += 1
            """print("inode {}".format(datalist_TCP[11])) 
            print("uid {}".format(datalist_TCP[9]))            
            print("rem_address {}".format(datalist_TCP[2])) 
            print("local_address {}".format(datalist_TCP[1])) 
            print("Protocol TCP")""" 
        fileUDPopen = open("/proc/net/udp")
        fileUDPread =   fileUDPopen.readlines()
        
        fileUDPopen.close()
        for UDPline in fileUDPread:
            datalist_UDP = UDPline.split()
            protocol = "UDP"
            list_connection=[datalist_UDP[11],datalist_UDP[9],datalist_UDP[2],datalist_UDP[1],protocol]
            self.dict_tcp_upd.update({self.connectioncount:list_connection})
            self.connectioncount += 1            
            """print("inode {}".format(datalist_UDP[11])) 
            print("uid {}".format(datalist_UDP[9]))            
            print("rem_address {}".format(datalist_UDP[2])) 
            print("local_address {}".format(datalist_UDP[1])) 
            print("Protocol UDP") """
        print(self.dict_tcp_upd)
        fileDEVopen = open("/proc/net/dev")
        fileDEVread = fileDEVopen.readlines()
        
        fileDEVopen.close()
        for fileDEVline in fileDEVread:
            word= fileDEVline.split()
            print(word)
            if (len(word)==17): 
                byte = float(word[9])
        self.networkUtilization = byte/speed   
        print(self.networkUtilization)      
data = DataCollection()
data.sys_networking()

