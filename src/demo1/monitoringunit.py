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
    print("Inside restartService"+serviceName["name"])
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

        client = pymongo.MongoClient("mongodb+srv://Test:Anurag@appregcluster.polvf.mongodb.net/numtest?retryWrites=true&w=majority")
        collection = client.numtest.numtest
        for message in consumer:
            #print(message)
            
            print("Hello you have registered ")
            #if len(message.value)==2:
            # mess = message.value['number']



            name = message.value['name']
            print("name!!!"+name)
            


            timestamp=message.value['time']
            mes={"time":timestamp,"name":name}
            # present=0
            # for y in mycol.find({"name":name}):
            #     present=1
            #     print("present.")
            # if(present==0):
            #     x=collection.insert_one(mes)
            #     print(x.inserted_id)



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

        client = pymongo.MongoClient("mongodb+srv://Test:Anurag@appregcluster.polvf.mongodb.net/numtest?retryWrites=true&w=majority")
        collection = client.numtest.numtest
    
        for message in consumer:
            # print("mess=",message.value)
            name = message.value['name']
            # print("name is:"+str(name))
            # timestamp = (message.timestamp)
            timestamp=message.value['time']
            # print("Timestamp is:"+str(timestamp))
            x=collection.update_one({'name':name},{"$set":{"time":timestamp}})
            print(x)


#in a thread

def getStatus():
    myclient = pymongo.MongoClient("mongodb+srv://Test:Anurag@appregcluster.polvf.mongodb.net/numtest?retryWrites=true&w=majority")
    mydb = myclient["numtest"]
    mycol=mydb["numtest"]

    while True:
        now=str(datetime.now())
        n=now.split(".")
        for y in mycol.find():
            print("Row:"+str(y))
            ts=datetime.fromtimestamp(int(str(y["time"])))
            fmt = '%Y-%m-%d %H:%M:%S'
            tstamp1 = datetime.strptime(str(n[0]), fmt)
            tstamp2 = datetime.strptime(str(ts), fmt)
            # print("name , Time-1:"+y["name"]+str(tstamp1))
            # print("Time-2:"+str(tstamp2))
            td = tstamp1 - tstamp2
            td_mins = int(round(td.total_seconds()))
            # print("Time-diff:"+str(td_mins))
            if td_mins>30:
                print("Oops threshold crossed for "+y["name"]+str(td_mins))
                var=mycol.delete_one(y)
                print(var)
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
