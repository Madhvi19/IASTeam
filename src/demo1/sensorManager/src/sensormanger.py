from kafka import KafkaConsumer
from kafka import KafkaProducer
from flask import Flask,request
from threading import Thread
from ConnectMongo import connectMongo
import threading
import time
import monitorInit as mon
import os
import json
import time
from json import loads
from json import dumps
app = Flask(__name__)
sensorDataPath = os.getcwd()+"/db/"
HOST = '127.0.0.1'
PORT = 7006

#register service
def registerService():
    mon.register()

#send heartbeat
def sendHeartBeat():
    mon.heartBeat()
 
os.system('python3 clean.py')  ## cleaned on every invoke
def listen(sensorId,topic):
    consumer = KafkaConsumer(topic,bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        d = message.value
        print(sensorId,topic)
        f = open(sensorDataPath+str(sensorId),'w')
        print("file created")
        json.dump(d,f)
        f.close()
        time.sleep(1.2)
        
@app.route('/registerInstance/', methods = ['POST'])
def registerInstance():
    Sinst  = json.loads(request.get_json())
    status, response, sensorid = connectMongo.SensorInstanceRegistration(Sinst)
    topic = connectMongo.getSensorURL(sensorid)
    if(topic != 'invalid sensor id'):
        x= Thread(target=listen,args=(str(sensorid),topic,))
        x.start()
    else:
        response = 'failed to get topic'
    return json.dumps({status:response})

@app.route('/registerType/', methods = ['POST'])
def registerType():
    Stype  = json.loads(request.get_json())
    status, response = connectMongo.SensorTypeRegistration(Stype)
    return json.dumps({status:response})
    
@app.route('/showTypes/',methods = ['POST'])
def showTypes():
    return connectMongo.GetAllSensorTypes()

@app.route('/showInstances/',methods = ['POST'])    
def showInstances():
    return connectMongo.GetAllSensorIDs()

def control(topic):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
    consumer = KafkaConsumer(topic,bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        reqd = message.value
        topic = "Topic"+str(reqd['sensorid'])+'-'
        producer.send(topic,reqd)

## Data Request handling from different Appids     
def app_serve():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
    consumer = KafkaConsumer('request',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        reqd = message.value
        f = open(sensorDataPath+str(reqd['sensorid']),'r') 
        data = json.load(f)
        f.close()
        res = {'appid':reqd['appid'],'val':data[str(reqd['inputType'])]}
        time.sleep(0.2)
        producer.send('response',res)
        
## initializer Function of the sensormanager -> can be called in init.py and init.py can be used by serverLifeCycle to start sensorManager in a Node.    
def initializeSensorManager():
    th = Thread(target=app_serve)
    th.start()
    th = Thread(target=control,args=('control',))
    th.start()
    app.run(debug=False,host=HOST,port=PORT)
registerService()
tq=threading.Thread(target=sendHeartBeat)
tq.start()
initializeSensorManager()


