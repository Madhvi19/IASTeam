from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from kafka.errors import KafkaError


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)


def sendToSLM(serviceName):
    topicName = "numtest"
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

    producer.send(topicName, serviceName.encode()).add_callback(on_send_success).add_errback(on_send_error) #send the name of failed service

def registerServices():

    consumer = KafkaConsumer('numtest',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))





     ##INsert into collections db
     #insertone 




#in a thread

def getStatus():

    #reads the collection from the db. onr by one.
    # exitting -(tims- cur tim ) >10 -> fail   
    if(cur_time-stored_time)> 10:
        # remove the entry from db
        sendToSLM(Name of the service)

    #otherwise continue
    while(True):
        # monitor the queue contents 
        # remove one by one and match the current time 





#Acts as pub and sends data to the SLM's topic in case of node failure