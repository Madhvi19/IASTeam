#template code for sheduler.
import monitorInit as mon
import threading
import time
from flask import Flask,request,send_file
import json
app=Flask(__name__)
mydict={}
@app.route('/registerApplication',methods = ['GET','POST'])
def registerApplication():
    global mydict
    local_id=request.json['localId']
    mydict[local_id]=local_id
    return 'done'


@app.route('/querryApplication',methods = ['GET','POST'])
def querryApplication():
    global mydict
    local_id=request.json['localId']
    if local_id in mydict.keys():
        return "true"
    else:
        return "false"


@app.route('/remove',methods = ['GET','POST'])
def removeApplication():
    global mydict
    local_id=request.json['localId']
    del mydict[local_id]
    return 'done'
    


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
    app.run(debug=False,port=5050)#change it to any port which you want.
