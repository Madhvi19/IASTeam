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
        
@app.route('/uploadSensorInstance', methods = ['POST'])
def uploadSensorInstance():
    sensorInstance = None
    if request.method == 'POST':
        f = request.files['file']
        sensorInstance = json.load(f) #dictionary
    if(sensorInstance == None):
        return "No sensor Instance received"
    status, response, sensorid = connectMongo.SensorInstanceRegistration(sensorInstance)
    topic = "Topic"+str(sensorid)
    if(status == True):
        x= Thread(target=listen,args=(str(sensorid),topic,))
        x.start()
    return response

@app.route('/uploadSensorType', methods = ['POST'])
def uploadSensorType():
    sensorType = None
    if request.method == 'POST':
        f = request.files['file']
        sensorType = json.load(f)  ## dictionary
    if(sensorType == None):
        return "No sensor Type received"
    status, response = connectMongo.SensorTypeRegistration(sensorType)
    return response

def control(Topic):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
    consumer = KafkaConsumer(Topic,bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',value_deserializer=lambda x: loads(x.decode('utf-8')))
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
        
def notify():
    consumer = KafkaConsumer('notify',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',enable_auto_commit=True,value_deserializer=lambda x: loads(x.decode('utf-8')))
    for msg in consumer:
        message = msg.value
        message = message["message"]
        data= message['user_email']
    #flag=True
    #for key in data:
    #print("ok")
    #if(key=="user_email"):
    #flag=False
    for email_id in data:
        print(type(email_id))
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls()
        s.login("botbotter98@gmail.com",  "viking@008") 
        s.sendmail("botbotter98@gmail.com",	email_id, messages) 
        s.quit()
				#break
			#if(flag==False):
				#break

## initializer Function of the sensormanager -> can be called in init.py and init.py can be used by serverLifeCycle to start sensorManager in a Node.    
def initializeSensorManager():
    th = Thread(target=app_serve)
    th.start()
    th = Thread(target=control,args=('control',))
    th.start()
    th = Thread(target=notify)
    th.start()
    app.run(debug=False,host=HOST,port=PORT)

registerService()
tq=threading.Thread(target=sendHeartBeat)
tq.start()
initializeSensorManager()
