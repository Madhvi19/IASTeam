import threading
import subprocess
import sys
import os
class IOTStarter(threading.Thread):
    def __init__(self,fp):
        threading.Thread.__init__(self)
        self.filePath=fp
    def run(self):
        #subprocess.check_call(['python',self.filePath])
        os.system(self.filePath)
        

print('starting things')
path_list=['python nodeUnit.py','service ssh start']
for f in path_list:
    print('starting '+f)
    IOTStarter(f).start()

