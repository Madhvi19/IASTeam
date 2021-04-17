import threading
import time
import monitorInit as mon
from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
from pymongo import MongoClient
intputTopic='toReadyQueue'
outputTopic='toBeConfigured'
monitorTopic='toApplicationMonitor'
client=MongoClient('mongodb+srv://nanu:merapassword@cluster0.hzfix.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=client.get_database('friday')
records=db.rtmInfo
#bind the mongodb instance with the application
class InputHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        consumer=KafkaConsumer(intputTopic,bootstrap_servers=['kafka:9092'],enable_auto_commit=True,group_id='rtm',value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        producer=KafkaProducer(bootstrap_servers=['kafka:9092'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
        for message in consumer:
            print('from the input topic',flush=True)
            print(message.value,flush=True)
            doc=message.value
            if doc['action']=='run':
                print('we have to run this',flush=True)
                producer.send(outputTopic,value=doc)
                producer.flush()
            elif doc['action']=='stop':
                print('we have to stop this',flush=True)
                #we have to include the process id.
                retDoc={}
                retDoc['action']='stop'
                retDoc['userName']=doc['userName']
                retDoc['appName']=doc['appName']
                retDoc['appId']=doc['appId']
                retDoc['algorithmName']=doc['algorithmName']
                retDoc['globalId']=doc['globalId']
                retDoc['localId']=doc['localId']
                numDocuments=records.count_documents({})
                if numDocuments==0:
                    continue
                temp=records.find_one({'localId':doc['localId']})
                retDoc['processId']=temp['processId']
                print('sending this file')
                print(retDoc)
                producer.send(outputTopic,value=retDoc)
                producer.flush()
                print('deleting the record from the registry',flush=True)
                records.delete_one({'localId':doc['localId']})
                print('deleted the record from the registry',flush=True)
            else:
                print('invalid message recived',flush=True)

class MonitorHandeler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def registerAlgo(self,doc):
        print('inserting the registration record',flush=True)
        records.insert_one(doc)
        print('inserted the registration record',flush=True)

    def updateTime(self,doc):
        print('updating the time stamp',flush=True)
        records.update({'localId':doc['localId']},{'$set':{'timestamp':doc['timestamp']}})
        print('updated the time stamp',flush=True)

    def run(self):
        consumer=KafkaConsumer(monitorTopic,bootstrap_servers=['kafka:9092'],enable_auto_commit=True,group_id='jok',value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        producer=KafkaProducer(bootstrap_servers=['kafka:9092'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
        for message in consumer:
            print('message recived from monitor topic',flush=True)
            print(message.value,flush=True)
            doc=message.value
            if doc['action']=='register':
                print('registring the update',flush=True)
                self.registerAlgo(doc)
            elif doc['action']=='update':
                print('updating the update',flush=True)
                self.updateTime(doc)
            elif doc['action']=='remove':
                localId=doc['localId']
                print('removing the record from the registry',flush=True)
                records.delete_one({'localId':localId})
                print('record removal from the registry is done.',flush=True)
            else:
                print('wrong input from monitor',flush=True)


class RegularCheck(threading.Thread):
    def __init__(self,interval,threshold):
        threading.Thread.__init__(self)
        self.interval=interval
        self.threshold=threshold
    def RunAlgoAgain(self,doc):
        retDoc={}
        retDoc['action']='run'
        retDoc['userName']=doc['userName']
        retDoc['appName']=doc['appName']
        retDoc['appId']=doc['appId']
        retDoc['algorithmName']=doc['algorithmName']
        retDoc['globalId']=doc['globalId']
        retDoc['localId']=doc['localId']
        retDoc['binding']=doc['binding']
        producer=KafkaProducer(bootstrap_servers=['kafka:9092'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
        producer.send(outputTopic,value=retDoc)
        producer.flush()

    def run(self):
        print('starting the checker',flush=True)
        while True:
            time.sleep(self.interval)
            docList=list(records.find())
            currTime=time.time()
            for doc in docList:
                docTime=doc['timestamp']
                if abs(docTime-currTime)>=self.threshold:
                    self.RunAlgoAgain(doc)



#register service
def registerService():
   mon.register()
    
#send heartbeat
def sendHeartBeat():
   mon.heartBeat()


print('starting runtimemaneger',flush=True)
registerService()
tq=threading.Thread(target=sendHeartBeat)
tq.start()


InputHandler().start()
MonitorHandeler().start()
RegularCheck(60,60*5).start()