#Server Life Cycle Mgr


#NOTE : PLEASE CHANGE THE NAMES OF CONSUMER/PRODUCER ACCORDINGLY


from kafka import KafkaConsumer
from json import loads
import json
import threading
import paramiko
import argparse
import time
import os 
from os import walk
from os import listdir
sourceDir='platformRepository'
avaialableNodes='freeNodeList.json' 
pathToNodeUNit='nodeUnit.py'
#Get the number of nodes to be started initially from the bootstrap 

{}


def initialiseNodes():
    consumer = KafkaConsumer('whateverName',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

#Task
#Recieve list of available nodes, ip and port
#start only the number thats needed =len(services) from platformInitialse.json
#maintain a free list (of remaining nodes) json as freeNodeList.json to be used in the third edpoint
#

def toServiceLifeCycleManager():
    topic='yourName'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

#second
#Communicate to service LM to start service
#send a json of started server(s). also the ip  details
#Port not needed
#the services part in the below jscon is same as obtained during initlisation. need not fill this during failure.Only servers neeeded in case of failure.
#{servers:["ip1",ip2,ip3],
# services:["scheduler,"dndkwdn']}



#Third endpoint

def fromServiceLifeCycleManager():
    consumer = KafkaConsumer('whateverName',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))
    #{"numberOfNodes":int}
    #get the number of nodes to be started and start the same using freeList .json

#serviceLM to Server LM


