#stopping part of application is remaining to test.
from kafka import KafkaConsumer
import json
import threading
import requests
import os
from zipfile import ZipFile
import subprocess
import signal
#import monitorInit as mon
import threading
import time
import psutil

class ApplicationLauncher(threading.Thread):
    def __init__(self,scheduleInfo):
        threading.Thread.__init__(self)
        self.appInfo=scheduleInfo
    
    def getApplicationRepository(self):
        #here we have to write the name of the cointainer of application repository
        return 'http://appRepo:7002/retrieve' #hardcoded for now.
    
    def saveAppData(self,local_id,app_id):
        myjson={'appid':app_id}
        r=requests.post(self.getApplicationRepository(),json=myjson)
        #r=requests.post(self.getApplicationRepository())
        if not os.path.exists('./'+local_id):
            os.mkdir(local_id)
        #f=open(local_id+'/'+local_id+'.zip','wb')
        with open('./'+local_id+'/'+local_id+'.zip','wb') as f:
            f.write(r.content)
        print('the content is ',flush=True)
        print(r.content,flush=True)
        self.zip_path='./'+local_id+'/'+local_id+'.zip'
        self.dir_path='./'+local_id+'/'
    
    def createEnviorment(self,local_id):
        print('creating the enviorment',flush=True)
        ZipFile(self.zip_path, 'r').extractall(self.dir_path)
        print('extracted the zipfile',flush=True)
        #now we will copy a sensor maneger file.
        os.system('cp baseAPI.py '+self.dir_path+'ApplicationDevelopmentTemplate/src/baseAPI.py')
        os.system('cp groupDataHandeler.py '+self.dir_path+'ApplicationDevelopmentTemplate/src/groupDataHandeler.py')
        f=open(self.dir_path+'ApplicationDevelopmentTemplate/src/scheduleConfig.json','w')
        json.dump(self.appInfo,f)#this should work
        f.close()
        #now we will create a new schedule config
        #and there will be some changes to the base api.
    

    #this method will get changed.
    def executeApplication(self,local_id):
        startingScript=self.appInfo['algorithmName']+'.py'
        try:
            subprocess.check_call(['python',startingScript], cwd=self.dir_path+'ApplicationDevelopmentTemplate/src/')
        except:
            print('catched the exeption',flush=True)
    #--------------------------------------------------------------------------------------------------------
    def stopProcess(self,local_id,pid):#this method is not yer tested.
        #first we have to check the app exist or not #this will be done with the help of flask
        print('trying to stop the process '+str(pid),flush=True)
        #getting from the local registration.
        r=requests.post('http://127.0.0.1:5050/querryApplication',json={'localId':local_id})
        print('this request is getting finished',flush=True)
        if r.content==b'true':
            print('this process exist in the system',flush=True)
            print('starting the termination of the application',flush=True)
            print(pid)
            print(type(pid))
            t=psutil.Process(pid)#doing this causes a exeption in this programme which stops the process.
            t.kill()
            #for this launch a new programme which terminates its sibling.
            print('got the process',flush=True)
            #p.terminate()
            print('termination of the application done.',flush=True)

            #the exception is occuring here.
            #removing from the local registration
            r=requests.post('http://127.0.0.1:5050/remove',json={'localId':local_id})
    #---------------------------------------------------------------------------------------------------------
    
    def run(self):
        #here we will run everything.
        print('proccesing a new information',flush=True)
        print(self.appInfo,flush=True)
        appId=self.appInfo['appId']
        localId=self.appInfo['localId']
        globalId=self.appInfo['globalId']
        typeOfAction=self.appInfo['action']


        if typeOfAction=='run':
            print('running a application',flush=True)
            self.saveAppData(localId,appId)
            self.createEnviorment(localId)
            self.executeApplication(localId)
            print('done with running it',flush=True)
        elif typeOfAction=='stop':
            print('stoping a application',flush=True)
            print(localId,flush=True)
            print(self.appInfo['processId'],flush=True)
            self.stopProcess(localId,self.appInfo['processId'])


#register service
#def registerService():
#    mon.register()
    
#send heartbeat
#def sendHeartBeat():
#    mon.heartBeat()

#registerService()
#tq=threading.Thread(target=sendHeartBeat)
#tq.start()


consumer=KafkaConsumer('toBeConfigured',bootstrap_servers=['kafka:9092'],enable_auto_commit=True,group_id='appconfig',value_deserializer=lambda x: json.loads(x.decode('utf-8')))
for message in consumer:
    print('the message recived is',flush=True)
    print(message.value,flush=True)
    print('starting/exiting of the application',flush=True)
    ApplicationLauncher(message.value).start()