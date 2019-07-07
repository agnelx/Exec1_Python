** **Project Title** ** : Python Script to get Process details<br/>
** **Project Description** **
> Develop an application, which does the following: <br/>
- Application is developed in Python Script
- Executable on windows machine
- Takes as an input:
  * Process Name (running on the system)
  * Program Run Duration<br/>
  * Sampling Interval (default 10 sec)
* For the given Program Run Duration, in the specified Sampling Intervals, gather the
following data about the process:<br/>
  *  % of CPU<br/>
  * private memory<br/>
  * number of handles/file descriptors<br/>
* And it Reports
  * Report the average value for each observed parameters<br/>
 * Raise error for any suspicion of memory leak<br/>

** **Getting Started** **
* Please clone or copy the project/file into to your local machine  
* A simple copy paste from GIT also works
* If you do copy - Please save the file with extension .py 

** **Prerequisites** **
1. Please make sure your Windows machine has Python3x Installed 
2. Recommended Version is above 3 (3.7)

** **Installing** **
1. If you don't have python installed , Best would be Install Anaconda from below link ,
https://www.anaconda.com/distribution/
2. This would automatically take care of all import packages as we need below packages for this script to execute 
    import psutil
    import time
    import sys
    import threading 
3.To run from command line please run below command
   python3 -m pip install psutil (required if not installed in your machine)


** **Running the tests** **
* Have a look at below Screenshot 
   ![alt text](Running.jpg)
* Please verify and follow the steps 
 1. Version of Python
 2. Sampling interval already hardcoded to 10
 4.Go to your command line and execute below commands
  *goto <path/of/the/script>
  *python Process_list_Details_windows_new.py notepad 1   
    note : Hear we are checking for process notepad for 1 minute

    
 ** **Author** **
 Agnel Leon
    
