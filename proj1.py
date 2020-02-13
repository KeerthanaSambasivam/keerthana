#!/usr/bin/env python
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

print ("Number of CPU is {0} \n".format(NoofCPU-1))
diskf = open("/pr`oc/diskstats", "r")
diskfileRead = diskf.read()
#print(fileRead)
diskFileList = diskfileRead.split()

Noofsda =0
for word in diskFileList:
    if "sda" in word:
       Noofsda  +=1
    


lastRecord = 0
startTime = time.clock()
endTime = time.clock()

intrCount = 0
intrOld = 0
ctxtCount = 0
ctxtOld = 0
#startTime = time.clock()
#endTime = time.clock()
anotherFlag = 0
Cur_FreeMemory =0
Pre_FreeMemory =0
PreviousUserModeTime=0
PreviousKernelModeTime=0
CurrentUserModeTime=0
CurrentKernelModeTime=0
firsttimeflag=0
Pre_diskread=0
Pre_diskwrite =0
Pre_sectored =0
Pre_sectorwrite =0
diskread = 0
diskwrite =0
sectorread =0
sectorwrite =0
#Timer Starts
while True:
      	print "Current Time is {0}".format(time.ctime())
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
           Value =(float(intrCount - intrOld)/5.0)
           print("intr count is {0}".format(Value))

        ctxtindex = FileList.index("ctxt")
        ctxtCount =int (FileList[ctxtindex + 1])
        print ("ctxtCount {0}".format(ctxtCount))
                
        if (firsttimeflag ==1):
            Value =(float(ctxtCount - ctxtOld)/5.0) 
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
            Utilization = ((UserMode+KernelMode)/5.0)*100
           # if (firsttimeflag == 0):
           #     firsttimeflag =1
           # else:
            print("User Mode for {0} is {1}sec ".format(name,UserMode))
            print("Kernel Mode for {0} is  {1}sec ".format(name,KernelMode))
            print("Utilization for{0}  is {1}%\n ".format(name,Utilization))
     
       
        file = open ("/proc/diskstats","r")
        diskstat_fileRead = file.read()
        print(diskstat_fileRead)
        diskstat_file = diskstat_fileRead.split()
        print("No of SDA {}".format(Noofsda))
        SDAcount =Noofsda
        while (SDAcount >= 1):
            if (SDAcount == 1):
                name ="sda"
            else:
                name = "sda"+ str(SDAcount-1)
            print(name)
            SDAcount -= 1
            statindex = diskstat_file.index(name)
            Pre_diskread = diskread
            Pre_diskwrite =diskwrite
            Pre_sectorread =sectorread
            Pre_sectorwrite =sectorwrite
            diskread  =int(diskstat_file[statindex+1])
            diskwrite = int(diskstat_file[statindex+5])
            sectorread = int(diskstat_file[statindex+3])
            sectorwrite = int(diskstat_file[statindex+7])
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
    	time.sleep(5)
#    endTime = time.clock()        
 
    
                    

