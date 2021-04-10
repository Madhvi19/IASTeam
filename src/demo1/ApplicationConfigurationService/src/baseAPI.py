#this is my modified base file
import threading
import os
import socket
import json
import time
import requests
import copy
from kafka import KafkaProducer
updateTimedelay=2*60
class ApplicationHearBeatManeger(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #now we have to get few data about the system.
        self.processId=os.getpid()
        self.ipAddress=socket.gethostbyname(socket.gethostname())
        self.appInfo=json.load(open('scheduleConfig.json')) 
        self.localId=self.appInfo['localId']
        self.appid=self.appInfo['appId']
        #for registring a application to the RTM.
        #{
        #action:<update/register>//register
        #local_id:<>
        #app_id:<>
        #process_id:<>
        #ip:<>
        #timestamp:<>
        #}
        

        #for updating the time of a application to the RTM.
        #{
        #action:<update/register>//update
        #local_id:<>
        #app_id:<>
        #timestamp:<> 
        #}
    def doLocolRegistration(self):
        r=requests.post('http://127.0.0.1:5050/registerApplication',json={'localId':self.localId})
    
    def run(self):
        appInfo=json.load(open('scheduleConfig.json')) 
        monitorProducer=KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
        registerApplicationJson=copy.deepcopy(appInfo)
        registerApplicationJson['action']='register'
        registerApplicationJson['timestamp']=time.time()
        registerApplicationJson['processId']=self.processId
        del registerApplicationJson['binding']
        monitorProducer.send('toApplicationMonitor',value=registerApplicationJson)
        monitorProducer.flush()

        #registring in the local node.
        self.doLocolRegistration()
        

        #doing regular time stamp update.
        #updateTimeStampJson={'action':'update','localId':self.localId,'timestamp':time.time()}
        updateTimeStampJson=copy.deepcopy(appInfo)
        updateTimeStampJson['action']='update'
        updateTimeStampJson['timestamp']=time.time()
        registerApplicationJson['processId']=self.processId
        del updateTimeStampJson['binding']
        while True:
            updateTimeStampJson['timestamp']=time.time()
            monitorProducer.send('toApplicationMonitor',value=updateTimeStampJson)
            monitorProducer.flush()
            time.sleep(updateTimedelay)
def appInit():
    ApplicationHearBeatManeger().start()

#{
#action:<remove>
#local_id:<>
#app_id:<>
#}
def removeLocalReg(f):
    r=requests.post('https://127.0.0.1:5050/remove',json=f)

def appExit():
    appInfo=json.load(open('scheduleConfig.json')) 
    #removeJson={'action':'remove','localId':localId,'appid':appid}
    removeJson=copy.deepcopy(appInfo)
    del removeJson['binding']
    removeJson['action']='remove'
    removeJson['']
    monitorProducer=KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
    monitorProducer.send('toApplicationMonitor',key=b'mykey',value=removeJson)
    monitorProducer.flush()

    #removing from the local registration.
    removeLocalReg({'localId':appInfo['localId']})
    exit()


#this perticualr code base will change.
#when we will be dealing with all the group id.
def getSensorId(label):
    appInfo=json.load(open('scheduleConfig.json'))
    bindingInfo=appInfo['binding']
    return bindingInfo[label]



#will be provided by vikram and pradeep.
def get_(appid,sensorid,nameOfInputField):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
    req = {}
    req['appid'] = appid
    req['sensorid'] = sensorid
    req['inputType'] = inputType
    consumer = KafkaConsumer('response',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',value_deserializer=lambda x: loads(x.decode('utf-8')))
    producer.send('request',req)
    for message in consumer:
        response = message.value
        if(response['appid'] == appid):
            return response['val']

def executeControl(appid,sensorid,controlParamenter):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
    req = {}
    req['appid'] = appid
    req['sensorid'] = sensorid
    req['controlname'] = control['name']
    req['param'] = control['parameter']
     
    producer.send("control",req)

def get(label,field):
    appInfo=json.load(open('scheduleConfig.json'))
    appid=appInfo['appId']
    return get_(appid,getSensorId(label),field)

def applyControl(label,field,dict):
    appInfo=json.load(open('scheduleConfig.json'))
    appid=appInfo['appId']
    executeControl(appid,getSensorId(label),{'name':field,'parameter':dict})
