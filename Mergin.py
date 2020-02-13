#!/usr/bin/env python3

import tkinter
from tkinter import *
from tkinter import ttk
import os
import string
import time
import heapq
#Declaration of Variables

interval = 5
intrCount = 0
intrOld = 0
ctxtCount = 0
ctxtOld = 0
anotherFlag = 0
Cur_FreeMemory =0
Pre_FreeMemory =0
CurrentUserModeTime =0
CurrentKernelModeTime=0
#### Disk ####
diskf = open("/proc/diskstats", "r")
diskfileRead = diskf.read()
#print(fileRead)
diskFileList = diskfileRead.split()
##################################Disk###########################
Noofsda =0
for word in diskFileList:
    if "sda" in word:
       Noofsda  +=1
Pre_diskread=[0 for i in range(0,Noofsda)]
Pre_diskwrite = [0 for i in range(0,Noofsda)]
Pre_sectorread = [0 for i in range(0,Noofsda)]
Pre_sectorwrite =  [0 for i in range(0,Noofsda)]
###################CPU UTILIZATION#######################################
f = open("/proc/stat", "r")
fileRead = f.read()
FileList = fileRead.split()
NoofCPU =0
for word in FileList:
    if "cpu" in word:
       NoofCPU  +=1
print ("Number of CPU is {0} \n".format(NoofCPU-2))

PreviousUserModeTime= [0 for i in range(0,NoofCPU-1)]
PreviousKernelModeTime=[0 for i in range(0,NoofCPU-1)]

###################################PROCESS#####################################################################
filenames = os.listdir("/proc") #Find all directories in /proc
count = len(filenames)
print("The number of filename in /proc are {0}".format(count))
#declaration of variable
lastRecord = 0
startTime = time.clock()
endTime = time.clock()
utime =[0 for i in range(0,count)]
pre_utime=[0 for i in range(0,count)]
cur_utime=[0 for i in range(0,count)]
stime=[0 for i in range(0,count)]
pre_stime=[0 for i in range(0,count)]
cur_stime=[0 for i in range(0,count)]
CPU_utilization=[0 for i in range(0,count)]
UserName=[0 for i in range(0,count)]
ProgramName=[0 for i in range(0,count)]
UID=[0 for i in range(0,count)]
PID=[0 for i in range(0,count)]
ProcessVirtualMem=[0 for i in range(0,count)]
ProcessPhysicalMem=[0 for i in range(0,count)]
dict_individualPID_info ={}
heap =[]
localist =[]
CPU_utilization_proc = [0 for i in range(0,count)]
status = [0 for i in range(0,count)]

#Find Total Physical Memory from /proc/meminfo  
memfile = open("/proc/meminfo","r")
memfileRead = memfile.read()
memfile.close()
memFileList = memfileRead.split()
TotalMemory = float(memFileList[1])/1024
count_ProcessNum =0
for fn in filenames:
    if(fn.isdigit()):
        filestatus = open("/proc/" +fn+"/status")        
        datastatus = filestatus.read()        
        filestatus.close()
        datalist_status = datastatus.split()
        
        UIDindex = datalist_status.index('Uid:')
        UID[count_ProcessNum] = datalist_status[UIDindex+1]
        filehandler = open("/proc/" +fn+"/stat")        
        data = filehandler.read()        
        filehandler.close()
        datalist = data.split()
        file_ProgramName = open("/etc/passwd")
        data_ProgramName = file_ProgramName.read()
        
        datalist_ProgramName = data_ProgramName.split(":")
       
        ProgramName[count_ProcessNum]= datalist[1]
        
        
        PID[count_ProcessNum] = datalist[0] #PID
        UserName[count_ProcessNum] = datalist[1] #UserName
        
        ProgramNameindex = datalist_ProgramName.index(UID[count_ProcessNum])
        ProgramName[count_ProcessNum] =datalist_ProgramName[ProgramNameindex+2]
       

        count_ProcessNum +=1
####### Network variables Declaration#####################################################

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

speed=1000 ####Mb/s


class DataCollection:
    def __init__(self):
        self.firsttimeflag = 0
        self.firsttimeflag_disk = 0
       
      #self.h_proc={}

    def performance(self):
        global intrCount,intrOld, ctxtCount, ctxtOld,anotherFlag, Cur_FreeMemory, Pre_FreeMemory, CurrentUserModeTime, CurrentKernelModeTime, PreviousUserModeTime, PreviousKernelModeTime, TotalMemory,FreeMemory,TotalUtilization
        self.ctxtValue =0
        self.intrValue =0
        self.dict_CPU = {}
        list_CPUdata =[0,0,0,0]
        file = open ("/proc/stat","r")
        fileRead = file.read()
        
        file.close()
        FileList = fileRead.split()
        
        intrOld = intrCount
        ctxtOld = ctxtCount
        intrindex = FileList.index("intr")
        if (self.firsttimeflag ==1):
            intrCount =int(FileList[intrindex+1])
            self.intrValue =(float(intrCount - intrOld)/interval)
            print("intr count is {0}".format(self.intrValue))
        elif(self.firsttimeflag ==0):
            intrCount =int(FileList[intrindex+1])
            self.intrValue = intrCount             
            print("intrCount is {0}".format(self.intrValue))

        ctxtindex = FileList.index("ctxt")
        if (self.firsttimeflag ==1):
            ctxtCount =int (FileList[ctxtindex + 1])
            
            self.ctxtValue =(float(ctxtCount - ctxtOld)/interval)
            print("ctxt count is {0}".format(self.ctxtValue))
        elif(self.firsttimeflag ==0):
            ctxtCount =int (FileList[ctxtindex + 1])
            self.ctxtValue =ctxtCount
            print ("ctxtCount {0}".format(self.ctxtValue))
                
                
        #User Mode and kernel mode CPU calculation
        CPUcount = 0
 
       
        while (CPUcount <= (NoofCPU-2)):
            name = "cpu"+ str(CPUcount)
            print(name)

            print("NoofCPU = {0}".format(NoofCPU-2))
            print("PreviousUserModeTime = {0}".format(PreviousUserModeTime[0]))
            indexCPU = FileList.index(name)
            
            CurrentUserModeTime =float( FileList[indexCPU+1])/100
            CurrentKernelModeTime = float(FileList[indexCPU+3])/100
            UserMode = (CurrentUserModeTime  -PreviousUserModeTime[CPUcount])/interval
            KernelMode =(CurrentKernelModeTime  -PreviousKernelModeTime[CPUcount])/interval
            Utilization = ((UserMode+KernelMode)/interval)*100
           # if (firsttimeflag == 0):
            #     firsttimeflag =1
            # else:
            print("User Mode for {0} is {1}sec ".format(name,UserMode))
            print("Kernel Mode for {0} is  {1}sec ".format(name,KernelMode))
            print("Utilization for{0}  is {1}%\n ".format(name,Utilization))
            list_CPUdata = [name,UserMode,KernelMode,Utilization,CurrentUserModeTime,CurrentKernelModeTime]
            
            self.dict_CPU.update({CPUcount:list_CPUdata})
            print(self.dict_CPU)
            PreviousUserModeTime[CPUcount] = self.dict_CPU[CPUcount][4]
            PreviousKernelModeTime[CPUcount]= self.dict_CPU[CPUcount][5]

            CPUcount += 1

        memfile = open("/proc/meminfo","r")
        memfileRead = memfile.read()
        # print(memfileRead)
        memfile.close()
        memFileList = memfileRead.split()
        Pre_FreeMemory =Cur_FreeMemory
        Cur_FreeMemory = float(memFileList[4])/1024
        
        TotalMemory = float(memFileList[1])/1024
        FreeMemory = float(Pre_FreeMemory+Cur_FreeMemory)/2
        
        TotalUtilization = (float(TotalMemory - FreeMemory)/float(TotalMemory))*100
        if (self.firsttimeflag == 1):
            print("Total Memory is {0} MB".format(TotalMemory))
            print("Free Memory is {0} MB".format(FreeMemory))
            print("Total Utilization is {0} % ".format(TotalUtilization))

    def sys_Disk(self):
        file = open ("/proc/diskstats","r")
        diskstat_LineRead = file.readlines()
        self.dict_diskstat={}
        count =0
        for eachline in diskstat_LineRead:
                         
            if eachline.find('sda')!= -1:
                word = eachline.split()
                
                name = word[2]
                diskread  =int(word[3])
                diskwrite = int(word[7])
                sectorread = int(word[5])
                sectorwrite = int(word[9])
            
                print("self.firsttimeflag_disk {0}".format(self.firsttimeflag_disk) )
                
                Value_diskread =(float(diskread - Pre_diskread[count])/interval)
                Value_diskwrite =(float(diskwrite - Pre_diskwrite[count])/interval)
                Value_sectorread =(float(sectorread - Pre_sectorread[count])/interval)
                Value_sectorwrite =(float(sectorwrite - Pre_sectorwrite[count])/interval)
                list_disk =[name,Value_diskread,Value_diskwrite,Value_sectorread,Value_sectorwrite]
                self.dict_diskstat.update({count:list_disk})   
                 #  print("AFTER diskread is {0}".format(Value_diskread))
                 #  print("diskwrite is {0}".format(Value_diskwrite))
                  # print("sectorread is {0}".format(Value_sectorread))
                  # print("sectorwrite is {0}\n".format(Value_sectorwrite))
                Pre_diskread[count] = diskread
                Pre_diskwrite[count] =diskwrite
                Pre_sectorread[count] =sectorread
                Pre_sectorwrite[count] =sectorwrite
                
                
                count +=1
###############################PROCESS#######################################################################
    def sys_process(self):
                global locallist,heap
                print("Inside while loop")
      #if (endTime - startTime - lastRecord > 5):
       #         interval =endTime - startTime - lastRecord
        #        lastRecord = endTime - startTime
                count_ProcessNum =0
                for fn in filenames:
                    if(fn.isdigit()): 
                         filehandler = open("/proc/"+fn+"/stat")
                         data = filehandler.read()
		         #print(data)
                         filehandler.close()    
                         datalist = data.split() 
                         status[count_ProcessNum] = datalist[2]
                         pre_utime[count_ProcessNum-1] = cur_utime[count_ProcessNum-1]
                         cur_utime[count_ProcessNum] = (float(datalist[13]))/100 #user mode time
                        # print("cur {0}".format(cur_utime[count_ProcessNum]))
                         utime[count_ProcessNum] = cur_utime[count_ProcessNum]- pre_utime[count_ProcessNum]
                       
		        #print("Utime is {0}".format(utime[ProcessNum]))
                         pre_stime[count_ProcessNum-1] = cur_stime[count_ProcessNum-1]
                         cur_stime[count_ProcessNum] = (float(datalist[14]))/100 # kernel mode time                    
                    
                         stime[count_ProcessNum] = cur_stime[count_ProcessNum]- pre_stime[count_ProcessNum] 
                         print("Addition {0}".format(stime[count_ProcessNum] + utime[count_ProcessNum]))
                         CPU_utilization_proc[count_ProcessNum] =  ((stime[count_ProcessNum] + utime[count_ProcessNum])/5)
                         #cur_stime[count_ProcessNum]+cur_utime[count_ProcessNum])    
                         
                         rss = datalist[23]#rss
		         #print("RSS is {0}".format(rss)) 
                         VirtualMem = datalist[22]  #Virtual memory Size
		         #print("Virtual Mem Size is {0}".format(VirtualMem))
                         ProcessVirtualMem[count_ProcessNum] = (int(VirtualMem)*1024 / (2**64))*100 
		       #print("Process Virtual Mem Size is {0}".format(VirtualMem))   
                         ProcessPhysicalMem[count_ProcessNum] = (int(rss) /int(TotalMemory) )*100 
		       #print("Process Physical Mem Size is {0}".format(ProcessPhysicalMem))  
                         count_ProcessNum +=1
                       
                for count in  range(1,count_ProcessNum):
                     dict_individualPID_info.update({PID[count]:{'UID':UID[count],'ProgramName':ProgramName,'UserName':UserName[count],'utime':utime[count],'stime':stime[count],'ProcessVirtualMem':ProcessVirtualMem[count],'ProcessPhysicalMem':ProcessPhysicalMem[count]}})
                     ###########heap#############
                     listheap = [CPU_utilization_proc[count],PID[count],ProgramName[count],status[count],UserName[count],ProcessVirtualMem[count],ProcessPhysicalMem[count]]
                     heapq.heappush(heap,listheap)
                       
#                     print(dict_individualPID_info[PID[count]]['UserName'])
                locallist=heapq.nlargest (50,heap)
                          
##################################Networking################################################
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
        self.InSeg = (cur_InSeg - pre_InSeg)/interval #TCP segments
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
    
        


#############################################################################################################                  
root = Tk()
root.title("Task Manager")
#root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.geometry('%dx%d+%d+%d' % (750, 600, 0, 0))

#Tab for root and individual tab click
note = ttk.Notebook(root)

tab_CPU = Frame(note)
tab_Disk = Frame(note)
tab_Network = Frame(note)
tab_Process = Frame(note)

note.add(tab_CPU, text = "System Performance" )
note.add(tab_Disk, text = "Disk I/O")
note.add(tab_Network, text = "Network I/O")
note.add(tab_Process, text = "Process")

Network_textBox=Text(tab_Network,height=400,width=200)
Network_textBox.grid(row=0,column=0,columnspan=3)
CPU_textBox=Text(tab_CPU,height=400,width=200)
CPU_textBox.grid(row=0,column=0,columnspan=3)

Label(tab_Process, text = "Filter :", borderwidth = 0).grid(row = 0, column = 0)
t =Text(tab_Process,  borderwidth = 0,width =10,height =1).grid(row = 0, column = 1)
Key_Button=Button(tab_Process,text ="Search", borderwidth = 1,command = "SearchButtonclick")
Key_Button.grid(row=0,column=2)

def SearchButtonclick (self):
     s = self.t.get("1.0",END)
     print(s)

def sys_performance():
    
       
    data.performance()
    CPU_textBox.delete('1.0',END)
    CPU_textBox.insert(END,"CPU Utilization \n\n")
    CPU_textBox.insert(END,"Name\t"+"User Mode Time\t\t\t"+"Kernel Mode Time"+"\t\t\t"+"CPU_Utilization\t\t"+"\n")
    for i in range(0,NoofCPU-1):
        print("NoofCPU is {0}".format(i))
        CPU_textBox.insert(END,str(data.dict_CPU[i][0])+'\t'+str(round(data.dict_CPU[i][1],2))+'\t\t'+str(round(data.dict_CPU[i][2],2))+'\t\t'+str(round(data.dict_CPU[i][3],2))+'\n')

    CPU_textBox.insert(END,"Number of Interrupts Serviced\t\t")
    CPU_textBox.insert(END,str(data.intrValue)+'\t'+'\n')
    CPU_textBox.insert(END,"Number of Context switches\t\t")
    CPU_textBox.insert(END,str(data.ctxtValue)+'\t'+'\n')
    CPU_textBox.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
    CPU_textBox.insert(END,"Memory Info \n\n")
    CPU_textBox.insert(END,"TotalMemory\t\t\t"+"FreeMemory\t\t"+"Mem_Util\t\t"+"\n")
    CPU_textBox.insert(END,str(TotalMemory)+'\t\t\t'+str(FreeMemory)+'\t\t'+str(TotalUtilization)+'\n')      
    CPU_textBox.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
	     
    root.after(5000,sys_performance)

def Tab_disk():
    if (data.firsttimeflag_disk ==0):
         
         data.sys_Disk()
         data.firsttimeflag_disk =1
    else:
         data.sys_Disk()

    
    
    Label(tab_Disk,text ="Name",borderwidth =0,width=10).grid(row=4,column=0,padx =1,pady =1)
    Label(tab_Disk,text ="Disk Reads",borderwidth =0,width=10).grid(row=4,column=3,padx =1,pady =1)
    Label(tab_Disk,text ="Disk Writes",borderwidth =0,width=10).grid(row=4,column=6,padx =1,pady =1)
    Label(tab_Disk,text ="Sector Reads",borderwidth =0,width=13).grid(row=4,column=13,padx =1,pady =1)
    Label(tab_Disk,text ="Sector Writes",borderwidth =0,width=13).grid(row=4,column=25,padx =1,pady =1)
    b =5
    for i in range(0,Noofsda):
        b =b+1
        Label(tab_Disk,text =data.dict_diskstat[i][0],borderwidth =0,width=10).grid(row=b,column=0,padx =1,pady =1)
        Label(tab_Disk,text =str(data.dict_diskstat[i][1]),borderwidth =0,width=10).grid(row=b,column=3,padx =1,pady =1)
        Label(tab_Disk,text =str(data.dict_diskstat[i][2]),borderwidth =0,width=10).grid(row=b,column=6,padx =1,pady =1)
        Label(tab_Disk,text =str(data.dict_diskstat[i][3]),borderwidth =0,width=13).grid(row=b,column=13,padx =1,pady =1)
        Label(tab_Disk,text =str(data.dict_diskstat[i][4]),borderwidth =0,width=13).grid(row=b,column=25,padx =1,pady =1)
    root.after(5000,Tab_disk)    
  
def Tab_process():
        global locallist
        print(time.ctime())
        data.sys_process()
        Label(tab_Process,text ="PID",borderwidth =0,width=10).grid(row=1,column=0,padx =1,pady =1)
        Label(tab_Process,text ="Username",borderwidth =0,width=10).grid(row=1,column=3,padx =1,pady =1)
        Label(tab_Process,text ="Status",borderwidth =0,width=10).grid(row=1,column=6,padx =1,pady =1)
        Label(tab_Process,text ="Vitual Memory",borderwidth =0,width=13).grid(row=1,column=13,padx =1,pady =1)
        Label(tab_Process,text ="Physical Memory",borderwidth =0,width=13).grid(row=1,column=25,padx =1,pady =1)
        Label(tab_Process,text ="%CPU",borderwidth =0,width=13).grid(row=1,column=30,padx =1,pady =1)
        Label(tab_Process,text ="Command",borderwidth =0,width=15).grid(row=1,column=35,padx =1,pady =1)

        
        b=1
        for f in locallist:
               b =b +1
              Label(tab_Process,text = str(f[1]),borderwidth =0,width=10).grid(row=b,column=0,padx =1,pady =1)
              Label(tab_Process,text = str(f[2]),borderwidth =0,width=10).grid(row=b,column=3,padx =1,pady =1)
              Label(tab_Process,text = str(f[3]),borderwidth =0,width=10).grid(row=b,column=6,padx =1,pady =1)
              Label(tab_Process,text = str(round(f[5],2)),borderwidth =0,width=13).grid(row=b,column=13,padx =1,pady =1)
              Label(tab_Process,text = str(round(f[6],2)),borderwidth =0,width=13).grid(row=b,column=25,padx =1,pady =1)
              Label(tab_Process,text = str(round(f[0],2)),borderwidth =0,width=13).grid(row=b,column=30,padx =1,pady =1)
              Label(tab_Process,text = str(f[4]),borderwidth =0,width=15).grid(row=b,column=35,padx =1,pady =1)

		
        root.after(5000,Tab_process)

def Tab_network():    
        data.sys_networking() 
        Network_textBox.delete('1.0',END)
        Network_textBox.insert(END,"\n")
        Network_textBox.insert(END, "Packets sent \t\t Packets received \t\tOutRequest\n ")
        Network_textBox.insert(END,str(data.Packetsent)+" \t\t\t"+str(data.Packetrecv)+"\t\t"+str(data.OutRequest)+"\n")     
        Network_textBox.insert(END, "ActiveOpen \t CurrentEstablish \t\tInSeg \t\tOutSeg\n ")
        Network_textBox.insert(END,str(data.ActiveOpen)+"\t\t"+str( data.CurrentEstablish)+"\t\t"+ str(data.InSeg)+"\t"+str(data.OutSeg)+'\n')  
        
        Network_textBox.insert(END,"InDataGrams \t\t OutDataGrams\n")
        Network_textBox.insert(END,str(data.InDataGrams)+"\t\t"+ str(data.OutDataGrams)+'\n')
        Network_textBox.insert(END, "UserName \t\t Program Name \t\tRemote address \t\tLocal address \t\t Protocol\n")
        
        for i in range(1,data.connectioncount):
   
            Network_textBox.insert(END,data.dict_tcp_upd[i][0]+'\t'+data.dict_tcp_upd[i][1]+'\t\t'+data.dict_tcp_upd[i][2]+'\t\t'+data.dict_tcp_upd[i][3]+'\t'+data.dict_tcp_upd[i][4]+'\n')
        Network_textBox.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
        Network_textBox.insert(END,"Network Utilization" +'\n')
        Network_textBox.insert(END,str(data.networkUtilization) +'\n')
        Network_textBox.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")

      
        root.after(5000,Tab_network)
        

data = DataCollection()
sys_performance()
Tab_disk()
Tab_process()
Tab_network()
note.pack()
root.mainloop()





