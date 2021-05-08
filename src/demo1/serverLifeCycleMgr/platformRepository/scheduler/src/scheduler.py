from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import time
import threading
from pymongo import MongoClient
import monitorInit as mon

f=open("testfile.txt",'w')
f.write("hey")
f.close()
i=0
while(True):
    i+=1
    time.sleep(2)
    f=open("testfile.txt",'a+')
    f.write("appn")
    f.close()



#register service
# def registerService():
#     mon.register()
# #send heartbeat
# def sendHeartBeat():
#     mon.heartBeat()





# consumerTopic='toBeScheduled'
# produserTopic='toReadyQueue'
# producer=KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
# def getEpochTime(date_time):
#     pattern = '%d.%m.%Y %H:%M:%S'
#     epoch = int(time.mktime(time.strptime(date_time, pattern)))
#     return epoch

# def getEpochList(time):
#     x=[]
#     for i in time:
#         x.append(getEpochTime(i))
#     return x

# #starting the mongo client.
# client=MongoClient('mongodb+srv://nanu:merapassword@cluster0.hzfix.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# db=client.get_database('friday')
# records=db.scheduleInfo
# lll=0
# class SheduleBucket(threading.Thread):
#     def __init__(self,msg):
#         threading.Thread.__init__(self)
#         self.schMsg=msg
#     def savetoDataBase(self):
#         global records
#         global lll
#         #before inserting we have to insert the localId in it
#         algodict=self.schMsg['algorithms']
#         for algoname in algodict.keys():
#             algodata=algodict[algoname]
#             n=len(algodata['startTime'])
#             l=[]
#             for i in range(n):
#                 l.append(str(lll))
#                 lll+=1
#             algodata['localId']=l
#             algodict[algoname]=algodata
#         self.schMsg['algorithms']=algodict
#         records.insert_one(self.schMsg)

#     def run(self):
#         print('saving the document to the storage',flush=True)
#         self.savetoDataBase()

# class SheduleIt(threading.Thread):
#     def __init__(self,msg):
#         print('constructor started',flush=True)
#         threading.Thread.__init__(self)
#         self.doc=msg
#         print('this line is also done',flush=True)

#     def run(self):
#         print('on the way to schedule',flush=True)
#         producer.send(produserTopic,value=self.doc)
#         print('this document is sent to the scheduler',flush=True)
#         print(self.doc,flush=True)




# class CheckTheAlgorithms(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.ll=0


#     def getEndTImes(self,st,et):
#         n=len(st)
#         res=[]
#         for i in range(n):
#             res.append(st[i]+int(et[i]))
#         return res
    
#     def Capable(self,currTime,st):
#         if st<=currTime:
#             return True
#         else:
#             return False
    
#     def updateDoc(self,doc,an,algo,index,startFlag):
#         if startFlag:
#             algo['startTime'][index]='08.04.2022 02:40:00'
#         else:
#             algo['endTime'][index]='08.04.2022 02:40:00'
#         doc['algorithms'][an]=algo
#         records.update({'globalId':doc['globalId']},doc)

#     def executeStart(self,doc,an,algo,currTime,st,index):
#         #generate the start document
#         msg={}
#         msg['action']='run'
#         msg['userName']=doc['userName']
#         msg['appName']=doc['appName']
#         msg['appId']=doc['appId']
#         msg['algorithmName']=an
#         msg['globalId']=doc['globalId']
#         msg['localId']=algo['localId'][index]
#         self.ll+=1
#         msg['binding']=algo['binding']
#         print('reached till here',flush=True)
#         SheduleIt(msg).start()
#         self.updateDoc(doc,an,algo,index,True)
    
#     def executeEnd(self,doc,an,algo,currTime,et,index):
#         msg={}
#         msg['action']='stop'
#         msg['userName']=doc['userName']
#         msg['appName']=doc['appName']
#         msg['appId']=doc['appId']
#         msg['algorithmName']=an
#         msg['globalId']=doc['globalId']
#         msg['localId']=algo['localId'][index]
#         SheduleIt(msg).start()
#         self.updateDoc(doc,an,algo,index,False)
#     def startCapable(self,currTime,st,et,algo,index):
#         if st<=currTime and et>currTime:
#             return True
#         else:
#             return False
#     def stopCapable(self,currTime,st,et,algo,index):
#         if et<=currTime and st>currTime:
#             return True
#         else:
#             return False
#     def checkDoc(self,doc):
#         algorithms=doc['algorithms']
#         print('checking the doc ',flush=True)
#         for algoName in algorithms.keys():
#             print(algoName,flush=True)
#             algoData=algorithms[algoName]
#             startTimes=getEpochList(algoData['startTime'])
#             #duration=algoData['duration']
#             endtime=getEpochList(algoData['endTime'])
#             currTime=time.time()
#             #currTimeList=[currTime]*len(startTimes)
#             #its good if we write end time rather than duration itself.
#             #endtime=self.getEndTImes(startTimes,duration)#made few fast changes should also run.
#             for i in range(len(startTimes)):
#                 st=startTimes[i]
#                 et=endtime[i]
#                 print(currTime,flush=True)
#                 print(st,flush=True)
#                 if(self.startCapable(currTime,st,et,algoData,i)):
#                     print('ready to execute',flush=True)
#                     self.executeStart(doc,algoName,algoData,currTime,st,i)
                
#                 if(self.stopCapable(currTime,st,et,algoData,i)):
#                     print('ready to exit',flush=True)
#                     self.executeEnd(doc,algoName,algoData,currTime,et,i)
            
    
#     def run(self):
#         while True:
#             global records
#             documents=list(records.find())
#             for doc in documents:
#                 print('starting the checking',flush=True)
#                 self.checkDoc(doc)
#             time.sleep(30)


# print('running scheduler',flush=True)





# registerService()
# tq=threading.Thread(target=sendHeartBeat)
# tq.start()


# consumer=KafkaConsumer(consumerTopic,bootstrap_servers=['localhost:9092'],enable_auto_commit=True,group_id='shed',value_deserializer=lambda x: json.loads(x.decode('utf-8')))
# CheckTheAlgorithms().start()
# for message in consumer:
#     print('recv the message',flush=True)
#     print(message.value)
#     SheduleBucket(message.value).start()