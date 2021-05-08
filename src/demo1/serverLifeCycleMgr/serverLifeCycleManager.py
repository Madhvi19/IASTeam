import pymongo
import threading
from kafka import KafkaProducer
from kafka import KafkaConsumer
from time import sleep
from json import dumps
from json import loads
import json
import os
import subprocess


def createContainer(serviceName):
     os.system('docker build -t krishnapriya11/'+serviceName+' .')
     os.system('docker run -d -P --name '+serviceName+' krishnapriya11/'+serviceName)
     output = subprocess.check_output('docker inspect -f \'{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}\' '+serviceName, shell=True)
     return ((output).decode().strip())








def totellstartService():
    print("In start")
    topic='startService'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
    data="Done"
    print(data)
    producer.send(topic, value=data)
    print("End of start Service")


def initialiseNodes():
    consumer = KafkaConsumer('fromInitializer',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

    #client = pymongo.MongoClient('localhost:27017')
    client = pymongo.MongoClient("mongodb+srv://Test:Anurag@appregcluster.polvf.mongodb.net/numtest?retryWrites=true&w=majority")
    collection = client.initializer.initializer
    totellstartService()
    for message in consumer:
        print(message)
        key=message.value.keys()
        for k in key:
            ip = message.value[k]["ip"]
            cont=message.value[k]["name"]
            usr=message.value[k]["username"]
            passwd=message.value[k]["password"]
            port=message.value[k]["port"]
            # ip="172.17.0.2"
            # cont="MonitoringUnit"
            # port=22
            # usr="test"
            # passwd="test"
            mes={"name":cont,"ip":ip,"port":port,"username":usr,"password":passwd,"Services":[]}
            collection.insert_one(mes)
    
def restartServicesHelper():
    consumer = KafkaConsumer('toServerLCM',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))
    print("In helper")
    client = pymongo.MongoClient("mongodb+srv://Test:Anurag@appregcluster.polvf.mongodb.net/numtest?retryWrites=true&w=majority")
    collection = client.initializer.initializer
    for message in consumer:
        print(message)
        value=message.value
        ip=createContainer(serviceName=value)
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

        topicNaame='machineAddr'
       
        
        data={"name":value,"ip":ip,"port":22,"username":"test","password":"test"}
        collection.insert_one(data)
        producer.send(topicName,value=data) 
        



       
if __name__=="__main__":
    #th=threading.Thread(target=restartServicesHelper)
    #th.start()
    tq=threading.Thread(target=initialiseNodes)
    tq.start()
