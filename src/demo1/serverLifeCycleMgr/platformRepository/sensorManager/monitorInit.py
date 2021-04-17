import threading
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json
from datetime import datetime 


def onSendSuccess(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def onSendError(excp):
    log.error('I am an errback', exc_info=excp)

def register():
    name = ""
    path = "conf/config.json"
    with open(path, 'r') as j:
        config = json.loads(j.read())
    #config = json.loads(path)
    name = config['serviceName']
    print(name)
    topic='toMonitorRegister'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

    
    ## Get the name & config from the config file of each comp
    
    # group = "group"
    now=datetime.now()
    now_epoch=str(now.timestamp())
    now_epoch=now_epoch.split(".")[0]
    data = {'status' : 'Alive',"name":name,"time":now_epoch}

    # data = {'name' :name}
    print("my name is ",name)
    producer.send(topic, value=data).add_callback(onSendSuccess).add_errback(onSendError)
    sleep(5)

def heartBeat():
    name = ""
    path = "conf/config.json"
    with open(path, 'r') as j:
        config = json.loads(j.read())
    name = config['serviceName']
    topic='toMonitorHeartBeat'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
    
    while(True):

        now=datetime.now()
        now_epoch=str(now.timestamp())
        now_epoch=now_epoch.split(".")[0]
        data = {'status' : 'Alive',"name":name,"time":now_epoch}

        
        producer.send(topic, value=data)
        print("hearbeating...")
        # print("hello")
        sleep(5)







