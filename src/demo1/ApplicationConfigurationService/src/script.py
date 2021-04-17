import threading
import subprocess
class IOTStarter(threading.Thread):
    def __init__(self,fp):
        threading.Thread.__init__(self)
        self.filePath=fp
    def run(self):
        subprocess.check_call(['python',self.filePath])

print('starting things')
path_list=['localRegistration.py','appconser.py']
for f in path_list:
    print('starting '+f)
    IOTStarter(f).start()

