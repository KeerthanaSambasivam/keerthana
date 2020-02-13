#!/usr/bin/env python3
import time
f = open("/proc/stat", "r")
fileRead = f.read()
#print(fileRead)
FileList = fileRead.split()
#print(FileList)
NoofCPU =0
for word in FileList:
    if "cpu" in word:
       NoofCPU  +=1

diskf = open("/proc/diskstats", "r")
diskfileRead = diskf.read()
#print(fileRead)
diskFileList = diskfileRead.split()

Noofsda =0
for word in diskFileList:
    if "sda" in word:
       Noofsda  +=1


print ("Number of CPU is {0} \n".format(NoofCPU-1))
lastRecord = 0
startTime = time.clock()
endTime = time.clock()
intrCount = 0
intrOld = 0
ctxtCount = 0
ctxtOld = 0

anotherFlag = 0
Cur_FreeMemory =0
Pre_FreeMemory =0
PreviousUserModeTime=0
PreviousKernelModeTime=0
CurrentUserModeTime=0
CurrentKernelModeTime=0
firsttimeflag=0
Pre_diskread=[0 for i in range(0,Noofsda)]
Pre_diskwrite = [0 for i in range(0,Noofsda)]
Pre_sectorread = [0 for i in range(0,Noofsda)]
Pre_sectorwrite =  [0 for i in range(0,Noofsda)]
diskread = [0 for i in range(0,Noofsda)]
diskwrite =[0 for i in range(0,Noofsda)]
sectorread =[0 for i in range(0,Noofsda)]
sectorwrite =[0 for i in range(0,Noofsda)]
Packetsent=0
Packetreci =0
OutRequest=0
ActiveOpen =0 #No of TCP connections
CurrentEstablish = 0 # TCP connection establish
InSeg =0 #TCP segments
OutSeg =0 # TCP out segments

#Timer Starts
while True:
    if (endTime - startTime - lastRecord > 5):
        interval =endTime - startTime - lastRecord
        lastRecord = endTime - startTime
        print ("Current Time is {0}".format(time.asctime()))
        #Read Stat File
        file = open ("/proc/stat","r")
        fileRead = file.read()
    #   print(fileRead)
#       file.close()
        FileList = fileRead.split()
#       print(FileList)

        intrOld = intrCount
        ctxtOld = ctxtCount
        intrindex = FileList.index("intr")
        intrCount =int(FileList[intrindex+1])
        print("intrCount is {0}".format(intrCount))
        if (firsttimeflag ==1):
           Value =(float(intrCount - intrOld)/interval)
           print("intr count is {0}".format(Value))

        ctxtindex = FileList.index("ctxt")
        ctxtCount =int (FileList[ctxtindex + 1])
        print ("ctxtCount {0}".format(ctxtCount))

        if (firsttimeflag ==1):
            Value =(float(ctxtCount - ctxtOld)/interval)
            print("ctxt count is {0}".format(Value))

        memfile = open("/proc/meminfo","r")
        memfileRead = memfile.read()
       # print(memfileRead)
        memfile.close()
        memFileList = memfileRead.split()
        Pre_FreeMemory =Cur_FreeMemory
        Cur_FreeMemory = float(memFileList[4])/1024

        TotalMemory = float(memFileList[1])/1024
        FreeMemory = float(Pre_FreeMemory+Cur_FreeMemory)/2

        TotalUtilization = (float(TotalMemory - FreeMemory)/float(TotalMemory))/100
        if (firsttimeflag == 1):
            print("Total Memory is {0} MB".format(TotalMemory))
            print("Free Memory is {0} MB".format(FreeMemory))
            print("Total Utilization is {0} % ".format(TotalUtilization))

        #User Mode and kernel mode CPU calculation
        CPUcount =NoofCPU
        while (CPUcount > 1):
            name = "cpu"+ str(CPUcount-2)
            print(name)
            indexCPU = FileList.index(name)
            CPUcount -= 1
            PreviousUserModeTime = CurrentUserModeTime
            PreviousKernelModeTime=CurrentKernelModeTime
            CurrentUserModeTime =float( FileList[indexCPU+1])/100
            CurrentKernelModeTime = float(FileList[indexCPU+3])/100
            UserMode = CurrentUserModeTime # -PreviousUserModeTime
            KernelMode =CurrentKernelModeTime # -PreviousKernelModeTime
            Utilization = ((UserMode+KernelMode)/interval)*100
           # if (firsttimeflag == 0):
           #     firsttimeflag =1
           # else:
            print("User Mode for {0} is {1}sec ".format(name,UserMode))
            print("Kernel Mode for {0} is  {1}sec ".format(name,KernelMode))
            print("Utilization for{0}  is {1}%\n ".format(name,Utilization))


        file = open ("/proc/diskstats","r")
        diskstat_LineRead = file.readlines()
        print(diskstat_LineRead)
        
        for eachline in diskstat_LineRead:
                        
            if eachline.find('sda')!= -1:
                word = eachline.split()
                print(word)
                Pre_diskread = diskread
                Pre_diskwrite =diskwrite
                Pre_sectorread =sectorread
                Pre_sectorwrite =sectorwrite
                diskread  =int(word[3])
                diskwrite = int(word[7])
                sectorread = int(word[5])
                sectorwrite = int(word[9])
                print("diskread is {0}".format(diskread))
                print("diskwrite is {0}".format(diskwrite))
                print("sectorread is {0}".format(sectorread))
                print("sectorwrite is {0}".format(sectorwrite))
                if (firsttimeflag ==0):
                   firsttimeflag =1
                else:
                   Value_diskread =(float(diskread - Pre_diskread)/5.0)
                   Value_diskwrite =(float(diskwrite - Pre_diskwrite)/5.0)
                   Value_sectorread =(float(sectorread - Pre_sectorread)/5.0)
                   Value_sectorwrite =(float(sectorwrite - Pre_sectorwrite)/5.0)

                   print("diskread is {0}".format(Value_diskread))
                   print("diskwrite is {0}".format(Value_diskwrite))
                   print("sectorread is {0}".format(Value_sectorread))
                   print("sectorwrite is {0}\n".format(Value_sectorwrite))
        
			
        #snmpFileListj
        filesnmp = open("/proc/net/snmp","r")
        snmpfileRead = filesnmp.read()
        print(snmpfileRead)
        snmpFileList = snmpfileRead.split() 
        print(snmpFileList)
        Packetsent = snmpFileList[21]
        Packetreci = snmpFileList[22]
        OutRequest = snmpFileList[30]
		
        print( "No of Ip packets sent = {0} ,No of packets received {1} and OutRequest = {2} ".format(Packetsent,Packetreci,OutRequest)) 
        index = snmpFileList.index("Tcp:")
        print(index)
        ActiveOpen =snmpFileList[124] #No of TCP connections
        CurrentEstablish = snmpFileList[127] # TCP connection establish
        InSeg =snmpFileList[129] #TCP segments
        OutSeg =snmpFileList[130] # TCP out segments
        print( "ActiveOpen = {0} ,CurrentEstablish ={1}, InSeg = {2} and OutSeg = {3} ".format(ActiveOpen, CurrentEstablish, InSeg, OutSeg))  
		
        InDataGrams =snmpFileList[142] #No of TCP connections
        OutDataGrams = snmpFileList[145] # TCP connection establish
        print ("InDataGrams = {0} and OutDataGrams ={1}".format(InDataGrams, OutDataGrams))  
    endTime = time.clock()

