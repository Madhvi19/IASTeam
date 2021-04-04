import monitorInit as mon
import threading
import time
#register service
def registerService():
    mon.register()
    
#send heartbeat
def sendHeartBeat():
   
    mon.heartBeat()

if(__name__)== "__main__":
    registerService()
    tq=threading.Thread(target=sendHeartBeat)
    tq.start()
    
    #write your program here
    
    i=0
    while(i<4):
        print("i  ",i)
        i+=1
        time.sleep(10)
    
