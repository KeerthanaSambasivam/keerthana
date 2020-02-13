''' CSC 239 Programming Assignment 1 '''
'''Keerthana Sambasivam'''Student-Id : 2301604797''



import os
import re
import Tkinter
from Tkinter import *
from ttk import *
import sys
import time
import heapq


previous_user_value = [0]*5
previous_system_value = [0]*5
current_user_value = [0]*5
current_system_value = [0]*5

previous_procUser_val = 0
previous_procSystem_val = 0
current_procUser_val = 0
current_procSystem_val = 0
no_interrupts=0
no_context_switches=0
previous_memory_consume=0
current_memory_consume=0
total_memory_consume=0
current_Total=0
current_Free =0
Memory_percentage = 0
locallist=[]

heap=[]
p_uname = re.compile(r'^(?P<name>\w+):(?P<value>\w+):(?P<measure>\w+)?')
user_uid={} 
uid_user={}



class Read:
   
   def __init__(self):
      s=0
      self.firstInterval = 1
      self.h_proc={}
      
   def GetData(self): # Getting System Statistics #
        global previous_user_value,previous_system_value ,current_user_value ,current_system_value
        global no_interrupts, no_context_switches
        c=0
        d=0
        index=0
        self.h_Top={}
   
        self.utiliz_cpuUser =0
        self.utiliz_cpuSystem =0
        file_stat= open("/proc/stat","r")
        
        for line in file_stat :
            
            if line.startswith ('cpu'):
                split_total=line.split()
                self.CPU_Name=split_total[0]
                self.User_time=split_total[1]
                self.Nice_time=split_total[2]
                self.System_time=split_total[3]
                current_user_value[index] = self.User_time
                current_system_value[index] = self.System_time
                if previous_user_value[index] and previous_system_value[index] == 0 :
                     previous_user_value [index]= self.User_time
                     previous_system_value [index]= self.System_time                                     
                else:                 
                   self.utiliz_cpuUser = (((float(current_user_value[index])/100)-(float(previous_user_value[index])/100))/3)*100
                   self.utiliz_cpuSystem = (((float(current_system_value[index])/100)-(float(previous_system_value[index])/100))/3)*100
                   previous_user_value[index] = current_user_value[index]
                   previous_system_value[index] = current_system_value[index]
                   
                self.h_Top[c]=[self.CPU_Name,self.User_time,str(self.utiliz_cpuUser),str(self.utiliz_cpuSystem),self.Nice_time,self.System_time]   
                   
                index+=1
                c+=1             
        index = 0
	if line.find ('intr'):
            split_cpu=line.split()
            self.IntrCnt=split_cpu[1]
            no_interrupts=self.IntrCnt

	if line.find('ctxt'):
            split_cpu=line.split()
            self.CntSwtch=split_cpu[1]
            no_context_switches=self.CntSwtch
        
        file_stat.close()

   def GetMem(self):  # Getting Memory Statistics #
      global current_Total,current_Free,Memory_percentage 
      global previous_memory_consume,current_memory_consume,total_memory_consume      
      global currentBuff,currentCach
      a=0
      self.h_Mem={}
      file_meminfo= open("/proc/meminfo","r")
      for line in file_meminfo:
         if line.startswith('MemT'):
            split_mem=line.split()
            self.MemValue=split_mem[1]
            current_Total=self.MemValue

         if line.startswith('MemF'):
            split_mem=line.split()            
            self.MemValue=split_mem[1]           
            current_Free=self.MemValue

         if previous_memory_consume == 0:
            previous_memory_consume=20
               
         else:
               
            current_memory_consume = int(current_Total)- int(current_Free)
            Memory_percentage = (float(current_memory_consume) / float(current_Total)) * 100
               
         self.h_Mem[a]=[current_memory_consume,Memory_percentage]      
               
         if line.startswith('Buf'):
            split_mem=line.split()            
            self.MemValue=split_mem[1]            
            currentBuff=self.MemValue
            
         if line.startswith('Cach'):
            split_mem=line.split()
            self.MemValue=split_mem[1]
            currentCach=self.MemValue
            
      file_meminfo.close()

   def GetDisk(self):   # Getting Disk Statistics #
      d=0
      self.h_Disk={}
      
      file_diskinfo= open("/proc/diskstats","r")
      f = file_diskinfo.readlines()
      for line in f:
         if line.find('sda')!=-1:
            split_diskstats=line.split()
            self.sda=split_diskstats[2]
            self.Value1=split_diskstats[4]
            self.Value2=split_diskstats[8]
            self.h_Disk[d]=[self.sda,self.Value1,self.Value2]
            d+=1    
                       
      file_diskinfo.close()

   def GetNet(self): # Getting Network Statistics #
      self.h_Net={}
      n=0
      self.h_Net1={}
      l=0
      self.h_Net2={}
      k=0
      file_netStats= open("/proc/net/snmp","r")
      f = file_netStats.readlines()         
      for line in f:
         if line.startswith('Tcp'):
            split_netStats=line.split()
            self.net=split_netStats[0]
            self.active=split_netStats[5]
            self.est=split_netStats[9]
            self.tcpin=split_netStats[10]
            self.tcpout=split_netStats[11]
            self.h_Net[n]=[self.net,self.active,self.est,self.tcpin,self.tcpout]
            n+=1
         if line.startswith('Udp'):
            split_netStats=line.split()
            self.net=split_netStats[0]
            self.udpin=split_netStats[1]
            self.udpout=split_netStats[4]
            self.h_Net1[l]=[self.net,self.udpin,self.udpout]
            l+=1
         if line.startswith('Ip'):
            split_netStats=line.split()
            self.net=split_netStats[0]
            self.ipin=split_netStats[3]
            self.ipout=split_netStats[10]
            self.h_Net2[k]=[self.net,self.ipin,self.ipout]
            k+=1
      file_netStats.close()
      
   def GetProc(self):  # Getting Process Statistics#

      global previous_procUser_val,previous_procSystem_val ,current_procUser_val ,current_procSystem_val,cal
      global heap,locallist
      
      
      pid=0
      cal=0
      
      heap=[]
      ListDir= os.listdir("/proc")

      for folder in  ListDir:
           if folder.isdigit():
              try:
                 f=open("/proc/"+folder+"/stat","r")

              except IOError:
                 continue
              else:         
                 
                 
                 for line in f:
                    f_stats = line.split()
                    self.procId= f_stats[0]
                    self.procName= f_stats[1].strip('()')
                    self.procStatus= f_stats[2]
                    self.procUtime= f_stats[13]
                    self.procStime= f_stats[14]
                    self.procPriority= f_stats[17]
                    self.procNice= f_stats[18]
                    self.procVsize= f_stats[22]
                    self.procVss= f_stats[23]
                    pid = int(self.procId)
                                     
                    if self.firstInterval == 1:
                       previous_procUser_val=0
                       previous_procSystem_val=0
                       cal = 0
                       
                       self.h_proc[pid]=[self.procId,self.procName,self.procStatus,
                                            self.procPriority,self.procNice,self.procVsize,
                                         self.procVss,self.procUtime,self.procStime,
                                            previous_procUser_val,previous_procSystem_val,cal]
                       heapq.heappush(heap,(cal,self.procId,self.procName,self.procStatus,
                                            self.procPriority,self.procNice,self.procVsize,
                                         self.procVss,self.procUtime,self.procStime,
                                            previous_procUser_val,previous_procSystem_val))
                       
                       previous_procUser_val=int(self.procUtime)
                       previous_procSystem_val=int(self.procStime)                   

                    else:
                       try:
			       previous_procUser_val = self.h_proc[int(pid)][7]
		               previous_procSystem_val = int(self.h_proc[int(pid)][8])
		               cal = ((float(self.procUtime)+float(self.procStime)) - (float(previous_procUser_val)+float(previous_procSystem_val)))/3
		               
		               self.h_proc[pid]=[self.procId,self.procName,self.procStatus,
		                                    self.procPriority,self.procNice,self.procVsize,
		                                 self.procVss,self.procUtime,self.procStime,
		                                    previous_procUser_val,previous_procSystem_val,cal]
		               heapq.heappush(heap,(str(cal),self.procId,self.procName,self.procStatus,
		                                    self.procPriority,self.procNice,self.procVsize,
		                                 self.procVss,self.procUtime,self.procStime,
		                                    previous_procUser_val,previous_procSystem_val))
		       except: 
			       pass
                       
                       
                       previous_procUser_val=int(self.procUtime)
                       previous_procSystem_val=int(self.procStime)
                       
      locallist=heapq.nlargest (100,heap)
      self.firstInterval = 0
    

   def Status_file (self):
        m = 0  
        self.Status_dir={}
        ListDir= os.listdir("/proc")

        for folder in  ListDir:
           if folder.isdigit():
                 g=open("/proc/"+folder+"/status","r")

		 for line in g:
                    if line.startswith("Uid"):
			slpit_uid=line.split()
                        self.Uid=split_uid[1]
		    if line.startswith("Pid"):
			slpit_pid=line.split()
                        self.Pid=split_Pid[1]
                    self.Status_dir[m]=[self.Pid, self.Uid]     
                    
                 print (Status_dir)     



root=Tkinter.Tk()

root.title("Task Manager")
root.geometry(("%dx%d")%(800,700))
note = Notebook(root)
note.place(x=20, y = 35, height = 600, width = 700)

frame1 = Frame(note)
frame2 = Frame(note)
frame3 = Frame(note)
frame4 = Frame(note)
frame5 = Frame(note)


note.add(frame1, text = "System Stats")
note.add(frame2, text = "Disk Stats")
note.add(frame3, text = "Network Stats")
note.add(frame4, text = "Process Stats")
note.add(frame5, text = "User Stats")

Label(frame5, text = "Username :", anchor = 'center', borderwidth = '4').grid(row = 0, column = 0)
Label(frame5, text = "Process name :", anchor = 'center', borderwidth = '4').grid(row = 1, column = 0)

e1 = Entry(frame5)
e2 = Entry(frame5)
e1.grid(row = 0, column = 1, padx = 4)
e2.grid(row = 1, column = 1, padx = 4)
#Button(frame5, text = "Find", command=Sample).grid(row = 0, column = 2,sticky = 'w', pady=4)      
Button(frame5, text = "clear").grid(row = 1, column = 2,sticky = 'w', pady=4)        

textBox1=Text(frame1,height=400,width=200)
textBox1.grid(row=0,column=0,columnspan=3)

textBox2=Text(frame4,height=400,width=200)
textBox2.grid(row=0,column=0,columnspan=3)

textBox3=Text(frame3,height=400,width=200)
textBox3.grid(row=0,column=0,columnspan=3)
 
textBox4=Text(frame2,height=400,width=200)
textBox4.grid(row=0,column=0,columnspan=3)



#username()


def Display_system():
	r.GetData()
	r.GetMem()

	textBox1.delete('1.0',END)
	textBox1.insert(END,"File: proc/stat \n\n")
	textBox1.insert(END,"Name\t"+"User Mode Time\t\t"+"\tNice Time\t\t"+"System Mode Time\t\t"+"CPU_Util_User\t\t"+ "CPU_Util_Sys\t\t"+"\n")
	textBox1.insert(END,r.h_Top[0][0]+'\t\t'+r.h_Top[0][1]+'\t\t'+r.h_Top[0][4]+'\t\t'+r.h_Top[0][5]+'\t\t\t'+"{0:.2f}".format(float(r.h_Top[0][2]))+'\t\t'+"{0:.2f}".format(float(r.h_Top[0][3]))+'\n')
	textBox1.insert(END,r.h_Top[1][0]+'\t\t'+r.h_Top[1][1]+'\t\t'+r.h_Top[1][4]+"\t\t"+r.h_Top[1][5]+'\t\t\t'+"{0:.2f}".format(float(r.h_Top[1][2]))+"\t\t"+"{0:.2f}".format(float(r.h_Top[1][3]))+'\n\n')
	textBox1.insert(END,"Number of Interrupts Serviced\t\t")
	textBox1.insert(END,str(no_interrupts)+'\t'+'\n')
	textBox1.insert(END,"Number of Context switches\t\t")
	textBox1.insert(END,str(no_context_switches)+'\t'+'\n')
	textBox1.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
	textBox1.insert(END,"File: proc/meminfo \n\n")
	textBox1.insert(END,"TotalMemory\t\t\t"+"FreeMemory\t\t"+"Buffer\t\t"+"Cache\t\t"+"MemoryUsed\t\t"+"Mem_Util\t\t"+"\n")
	textBox1.insert(END,str(current_Total)+'\t\t\t'+str(current_Free)+'\t\t'+str(currentCach)+'\t\t'+str(currentBuff)+"\t\t"+str(r.h_Mem[0][0])+"\t\t"+"{0:.2f}".format(float(r.h_Mem[0][1]))+'\n')      
	textBox1.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")

	r.h_Top.clear()     
	root.after(3000,Display_system)


def Display_network():
	r.GetNet()
	textBox3.delete('1.0',END)
	textBox3.insert(END,"File: proc/net/snmp \n\n")
	textBox3.insert(END,r.h_Net[0][0]+'\t'+r.h_Net[0][1]+'\t\t'+r.h_Net[0][2]+'\t\t'+r.h_Net[0][3]+'\t'+r.h_Net[0][4]+'\n')
	textBox3.insert(END,r.h_Net[1][0]+'\t'+r.h_Net[1][1]+'\t\t'+r.h_Net[1][2]+'\t\t'+r.h_Net[1][3]+'\t'+r.h_Net[1][4]+'\n')
	textBox3.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
	textBox3.insert(END,r.h_Net1[0][0]+'\t'+r.h_Net1[0][1]+'\t\t'+r.h_Net1[0][2]+'\n')
	textBox3.insert(END,r.h_Net1[1][0]+'\t'+r.h_Net1[1][1]+'\t\t'+r.h_Net1[1][2]+'\n')
	textBox3.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
        textBox3.insert(END,r.h_Net2[0][0]+'\t'+r.h_Net2[0][1]+'\t\t'+r.h_Net2[0][2]+'\n')
	textBox3.insert(END,r.h_Net2[1][0]+'\t'+r.h_Net2[1][1]+'\t\t'+r.h_Net2[1][2]+'\n')
	textBox3.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")   
        r.h_Net.clear()
      
	root.after(3000,Display_network)

def Display_disk():
	r.GetDisk()
	textBox4.delete('1.0',END)
	textBox4.insert(END,"File: proc/diskstats \n\n")
	textBox4.insert(END,"Name"+'\t'+"No. Of Reads"+'\t\t'+"No. of Writes"+'\n')
	textBox4.insert(END,r.h_Disk[0][0]+'\t\t'+r.h_Disk[0][1]+'\t\t'+r.h_Disk[0][2]+'\n')
	textBox4.insert(END,r.h_Disk[1][0]+'\t\t'+r.h_Disk[1][1]+'\t\t'+r.h_Disk[1][2]+'\n')
	textBox4.insert(END,"----------------------------------------------------------------------------------------------------------\n\n")
	r.h_Disk.clear()
      
	root.after(3000,Display_disk)


def Display_process():
	global locallist
        r.GetProc()
	textBox2.delete('1.0',END)
	textBox2.insert(END,"File: proc/pid/stat \n\n")
	textBox2.insert(END,"PID"+"\t" + "Name\t\t" + "Status\t"+"Priority\t"+"Nice\t"+"Vss\t\t"+ "Rss\t"+"UsrTime\t"+"SysTime\t"+"%CPU"+"\n")
	
	for f in locallist:

		textBox2.insert(END,f[1]+'\t'+f[2]+'\t\t '+f[3]+'\t '+f[4]+'\t '+f[5]+'\t'+f[6]+'\t\t'+f[7]+'\t'+f[8]+'\t'+f[9]+'\t'+"{0:.2f}".format(float(f[0]))+'\n')

		
	root.after(3000,Display_process)

def username():
   global user_uid
   global uid_user

   handler = open('/etc/group');
   for line in handler:
	line = (line.strip())
        user = p_uname.search(line)
        if user:
		groups = user.groupdict()
		user_uid[groups['measure']] = groups['name']
		uid_user[groups['name']] = groups['measure']

   handler.close()
   print (user_uid)

r=Read()

Display_system()
Display_process()
Display_network()
Display_disk()
root.mainloop()

  



