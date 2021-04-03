import monitorInit as mon

#register service
def registerService():
    mon.register()
    sendHeartBeat()
#send heartbeat
def sendHeartBeat():
    mon.heartBeat()

if(__name__)== "__main__":
    registerService()
