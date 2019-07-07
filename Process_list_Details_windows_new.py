import psutil
import time
import sys
import os
import os.path
import logging
from threading import Timer
from time import sleep
from datetime import datetime
from statistics import mean

#This class is used for timer , to specify which function can be used to run in repetation
class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):  
    self.is_running = False
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"-------- running-------Please wait-------------")
    self.start()
    self.function(*self.args, **self.kwargs)
    

  def start(self):
    if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False   

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            logging.info('1.Checking if process name contains the given name string.')
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            logging.error('3.Error occurred in Checking if process name contains the given name string. ')
    return False;
 
def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
 
    listOfProcessObjects = []
 
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time','cpu_percent','memory_info','open_files'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
               logging.info('2.Checking if process name contains the given name string.')
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
           logging.error('4.Error occurred in Checking if process name contains the given name string. ')
 
    listOfProcessIds=listOfProcessObjects;
    
    try:
     if len(listOfProcessIds) > 0:
       
       for elem in listOfProcessIds:
           processID = elem['pid']
           processName = elem['name']
           processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
           processcpupercent=elem['cpu_percent']
           processprivatemem=elem['memory_info'].private
           processfiledesc=elem['open_files']
           countfiledesc=len(processfiledesc)
           
           try:
               with open('tmp_process_lst.txt','a') as f:
                   print(processID ,"|",processName,"|",processCreationTime,"|",processcpupercent,"|",processprivatemem,"|",countfiledesc,file=f )
           finally:
               f.close()
           
     else :
        print('No Running Process found with given text')
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"*************************END OF PROCESS******************************************************")
        sys.exit("*****************************************")
    except IOError as e:
               logging.error('Error occurred ' + str(e))
   
def calcAvg():
    
    try:
    #check file is availbe
     File='./tmp_process_lst.txt'
    
     if os.path.isfile(File) and os.access(File, os.R_OK):
        #print("File exists and is readable")
    
        
        listofprivatememory=[]
        listofFD=[]
        listofcpu=[]
        allrow=[]
        try:
         logging.info('Trying to read the file content')
         fileHandler = open(File,'r')
         for line in fileHandler:
            fields = line.split("|")
            
            cpuu=float(fields[3])
            privatememory=int(fields[4])
            FileDescriptor=int(fields[5])
            listofprivatememory.append(privatememory)
            listofFD.append(FileDescriptor)
            listofcpu.append(cpuu)
            allrow.append(line)
        finally:
         fileHandler.close()
        
        Avg_PM=round(mean(listofprivatememory),2)
        Avg_FD=round(mean(listofFD),2)
        Avg_Cpu=round(mean(listofcpu),2)
        try:
         with open('output.txt','a') as f:
          print("Average Private Memory : ",Avg_PM)
          print("Average Private Memory : ",Avg_PM,file=f)
          print("Average File Descriptor : ",Avg_FD)
          print("Average File Descriptor : ",Avg_FD,file=f)
          print("Average CPU % : ",Avg_Cpu)
          print("Average CPU % : ",Avg_Cpu,file=f)
        finally:
          f.close()
        for elem in allrow:
            fields=elem.split("|")
            p_memory=int(fields[4])
            F_Descriptor=int(fields[5])
            P_Cpu=float(fields[3])
            time=fields[2]
            pid=fields[0]
        try:
         with open('output.txt','a') as f:    
          if(p_memory >Avg_PM and F_Descriptor > Avg_FD and P_Cpu > Avg_Cpu):
           print("possible Memory Leak at",time,"with PID",pid,"memory Usage Was",P_Cpu)
           print("possible Memory Leak at",time,"with PID",pid,"memory Usage Was",P_Cpu,file=f)
          else :
           print("No Memory Leak to Report")
           print("No Memory Leak to Report",file=f)
        finally:
          f.close()
     else:
        print("Tmp file - Either the file is missing or not readable")
    except IOError as e:
        logging.error('Error occurred ' + str(e))
    
def main(process_name,process_end_time):
    File1='./tmp_process_lst.txt'
    if os.path.isfile(File1) and os.access(File1, os.R_OK):
        os.remove(File1)
    File2='./output.txt'
    if os.path.isfile(File2) and os.access(File2, os.R_OK):
        os.remove(File2)
    
    #get process name from user 
    #process_name=input("Process Name (running on the system) :")
    #process_end_time=input("Program Run Duration in minutes(Least is 1 min):")
    val = int(process_end_time)
    process_end_time_sec=val*60
    print("Process for  ",process_name,"and will be executed for next ",process_end_time,"minutes")
    
    print("-------------------Check if a process is running or not -------------------------------------")
 
    # Check if any chrome process was running or not.
    if checkIfProcessRunning(process_name):
        print('Yes a ',process_name,' process is running')
    else:
        print('No process with ',process_name,'is running')
        sys.exit("************END of PROCESS*****************************")
    
    
    timefunction = RepeatedTimer(10, findProcessIdByName, process_name) #Sampling interval set as 10 sec 
    
    try:
        logging.info('Setting process endtime')
        sleep(process_end_time_sec)     
    finally:
        timefunction.stop() 
        calcAvg()
    
    
if __name__ == '__main__':
   process_name =str(sys.argv[1])
   process_end_time=int(sys.argv[2])
   # initialize the log settings
   logging.basicConfig(filename='processdetail.log',level=logging.INFO)
   main(process_name,process_end_time)

