import getterSetter
import time
import _thread


def requestServer(desiredTemperature):
    print("request will be sent to server")


desiredTemperature = 24.0
while(1):
    data  = getterSetter.getData("Temperature")

    try:
        for temp in data:
            if temp != desiredTemperature:
                _thread.start_new_thread( requestServer, (desiredTemperature,) )
                break
            
    except:
        print("Error: unable to start thread")
    
    time.sleep(60)
