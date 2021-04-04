import monitorInit as mon

#register service
def registerService():
    mon.register()
    mon.heartBeat()
#send heartbeat


if(__name__)== "__main__":
    registerService()
