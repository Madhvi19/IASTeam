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

def fromServerLifeCycleManager():
    #Server to Service
#Recieve a list of started nodes,ip,port,SERVICES TO BE STARTED.
#make an entry in db 

# TAKE AN ENTRY FROM DB CALCULATE LOAD. BELOW THREHOLD? yes-> start a service 
#                                                       no -> leave it
#   {Service , node id, ip, port}

# {nodes list  }
    pass
def restartService():
    #From Monitoring
#service failure
#Take the corresponding row from DB . start it on the same node if the load is BELOW THREHOLD? yes-> start a service 
#                                                       no -> leave it
#check the node status using flask.
#DEAD!! 
#take one by one from the node list and check theload status wherever the load is less, start the service
# When there is no such node, ask the server LM to start a new node.
#When the server is started, start the required service.

    pass

def toServerLifeCycleManager(params):
    topic='yourName'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
    # send the json of number of new nodes to be started
    #{"numberOfNodes":int}
