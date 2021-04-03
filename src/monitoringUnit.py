import pymongo
from datetime import datetime
from kafka import KafkaConsumer
from kafka import KafkaProducer
import calendar
import time
import threading
from json import loads
from json import dumps


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

    #send the name of failed service
    #get ack 
    #if not ACKED within some time 
    # unable to start 
    producer.send(topicName, serviceName).add_callback(on_send_success).add_errback(on_send_error) #send the name of failed service





def registerServices():
    consumer = KafkaConsumer('numtest',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    collection = client.numtest.numtest
    for message in consumer:
        #print(message)
        timestamp=str(message.timestamp)
        #print(message)
        #print(len(message.value))
        if len(message.value)==2:
            mess = message.value['number']
            name = message.value['name']
            mes={"num":mess,"time":timestamp,"name":name}
            collection.insert_one(mes)                      ##INsert into collections db
            #print('{} added to {}'.format(mes, collection))
     




#in a thread

def getStatus():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["numtest"]
    mycol=mydb["numtest"]

    while True:
        now=str(datetime.now())
        n=now.split(".")
        for y in mycol.find():
            ts=datetime.fromtimestamp(int(str(y["time"])[0:-3]))
            fmt = '%Y-%m-%d %H:%M:%S'
            tstamp1 = datetime.strptime(str(n[0]), fmt)
            tstamp2 = datetime.strptime(str(ts), fmt)
            if tstamp1 > tstamp2:
                td = tstamp1 - tstamp2
            else:
                td = tstamp2 - tstamp1
            td_mins = int(round(td.total_seconds()))
            #print(td_mins)
            if td_mins>80:
                mycol.delete_one(y)
                #print(y["name"])
                my_dict={"name":y["name"]}
                sendToSLM(my_dict)
        

#Acts as pub and sends data to the SLM's topic in case of node failure

if __name__=="__main__":
    th=threading.Thread(target=registerServices)
    th.start()
    #th.join()
    tq=threading.Thread(target=getStatus)
    tq.start()