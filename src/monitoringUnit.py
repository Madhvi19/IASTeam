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
    print("Inside restartService")
    topicName = "restartService"
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

    #send the name of failed service
    #get ack 
    #if not ACKED within some time 
    # unable to start 
    producer.send(topicName, serviceName) #send the name of failed service





def registerServices():
    while True:
        consumer = KafkaConsumer('toMonitorRegister',
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
            print("Hello")
            #if len(message.value)==2:
            # mess = message.value['number']
            name = message.value['name']
            mes={"time":timestamp,"name":name}
            x=collection.insert_one(mes)
            print(x.inserted_id)                      ##INsert into collections db
            #print('{} added to {}'.format(mes, collection))
        


def checkHeartBeat():
    while(1):
        consumer = KafkaConsumer('toMonitorHeartBeat',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        collection = client.numtest.numtest
    
        for message in consumer:
            name = message.value['name']
            print("name is:"+str(name))
            timestamp = (message.timestamp)
            print("Timestamp is:"+str(timestamp))
            x=collection.update_one({'name':name},{"$set":{"time":timestamp}})
            print(x)


#in a thread

def getStatus():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["numtest"]
    mycol=mydb["numtest"]

    while True:
        now=str(datetime.now())
        n=now.split(".")
        for y in mycol.find():
            print("Row:"+str(y))
            ts=datetime.fromtimestamp(int(str(y["time"])[0:-3]))
            fmt = '%Y-%m-%d %H:%M:%S'
            tstamp1 = datetime.strptime(str(n[0]), fmt)
            tstamp2 = datetime.strptime(str(ts), fmt)
            print("Time-1:"+str(tstamp1))
            print("Time-2:"+str(tstamp2))
            td = tstamp1 - tstamp2
            td_mins = int(round(td.total_seconds()))
            print("Time-diff:"+str(td_mins))
            if td_mins>10:
                mycol.delete_one(y)
                #print(y["name"])
                my_dict={"name":y["name"]}
                sendToSLM(my_dict)
            time.sleep(2)
        

#Acts as pub and sends data to the SLM's topic in case of node failure

if __name__=="__main__":
    th=threading.Thread(target=registerServices)
    th.start()
    #th.join()
    tq=threading.Thread(target=getStatus)
    tq.start()

    ts=threading.Thread(target=checkHeartBeat)
    ts.start()