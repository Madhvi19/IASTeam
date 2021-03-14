import getterSetter
import time
import _thread


def notifyGuard(data):
    print("Notification will be sent to the Guard")

while(1):
    data = getterSetter.getData("InfraRed")

    try:
        if 1 in data:
            _thread.start_new_thread( notifyGuard, (data, ) )
            
    except:
        print("Error: unable to start thread")
    time.sleep(60)






