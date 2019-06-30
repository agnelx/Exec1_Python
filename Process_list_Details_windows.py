import psutil
import time
import sys
import threading 
from time import sleep
from datetime import datetime

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
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"-------- Successful-----------------Start/Begin of Next Iteration----------Please wait-------------")
    self.start()
    self.function(*self.args, **self.kwargs)
    

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"*************************END OF PROCESS******************************************************")    

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
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
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
 
    return listOfProcessObjects;
   
def CalculateAvg(process_name):
 
    
    listOfProcessIds = findProcessIdByName(process_name)
    
    num_process = len(listOfProcessIds)
    sumcpuper = 0
    sumprivmem = 0
    sumfiledesc = 0
    
   
    if len(listOfProcessIds) > 0:
       
       for elem in listOfProcessIds:
           #processID = elem['pid']
           processName = elem['name']
           #processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
           processcpupercent=elem['cpu_percent']
           processprivatemem=elem['memory_info'].private
           processfiledesc=elem['open_files']
           countfiledesc=len(processfiledesc)
           
           sumcpuper = sumcpuper + processcpupercent
           sumprivmem = sumprivmem + processprivatemem
           sumfiledesc = sumfiledesc+countfiledesc
           
           
           #print((processID ,processName,processCreationTime,processcpupercent,processprivatemem,countfiledesc ))
    
    else :
        print('No Running Process found with given text')
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"*************************END OF PROCESS******************************************************")
        sys.exit("*****************************************")
           
    Avg_cpu = sumcpuper/num_process
    Avg_Private_mem = sumprivmem/num_process
    Avg_FileDesc = sumfiledesc/num_process
    
    
    print("Number of Process Running for ",process_name,"is:",num_process)
    print("ProcessName >>>>>>>>>>>>>>>>>>>>>>>>>",processName)
    #print("Process Creation Time >>>>>>>>>>>>>>>",processCreationTime)
    print("Average % of CPU >>>>>>>>>>>>>>>>>>>>>>>",Avg_cpu)
    print("Average PrivateMemory Used in Bytes >",Avg_Private_mem)
    print("Average handles/file Descriptor >>>>>>>>>>>>>",Avg_FileDesc)
    
    
def main():
    #get process name from user 
    process_name=input("Process Name (running on the system) :")
    process_end_time=input("Program Run Duration in minutes(Least is 1 min):")
    val = int(process_end_time)
    process_end_time_sec=val*60
    print("Initiate Process for  ",process_name,"and will be executed for next ",process_end_time,"minutes")
    
    print("-------------------Check if a process is running or not -------------------------------------")
 
    # Check if any chrome process was running or not.
    if checkIfProcessRunning(process_name):
        print('Yes a ',process_name,' process is running')
    else:
        print('No process with ',process_name,'is running')
        sys.exit("************END of PROCESS*****************************")
    
    
    timefunction = RepeatedTimer(10, CalculateAvg, process_name) #Sampling interval set as 10 sec 
    
    try:
        sleep(process_end_time_sec) 
        
    finally:
        timefunction.stop() 
    
 
if __name__ == '__main__':
   main()

