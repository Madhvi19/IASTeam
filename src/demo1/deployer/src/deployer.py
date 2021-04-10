import os,random
from flask import * 
import json
from kafka import KafkaProducer
from time import sleep
from flask import Flask
from flask import request
import json
import sys
import json
import requests
import os
import random
import threading
import monitorInit as mon
import json
import time
from json import dumps
schedulerTopicName = 'toBeScheduled'
from datetime import date
from datetime import datetime
import _thread
import threading
HOST="127.0.0.1"
SCHEDULER_PORT=7003
import os.path
from os import path
import json
fileName = "../config/metaData.json"

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))



def writeFile(data):
    with open(fileName, 'w') as fp:
        json.dump(data, fp)


def globalId():
    global data
    # generate 3 no instances
    gID = 0
    while True:
        gID = random.randint(100,999)
        if gID in data.keys():
            continue
        else:
            data[gID] = 1
            writeFile(data)
            break
    return gID


def verifyAppId(appId):
    s = json.dumps(appId)
    res = requests.post("http://127.0.0.1:7002/appIdVerification/", json=s).json()
    print("appIdVerification",res)
    return res

def verifySensorData():
    return True


def validateConfig(configJson):
    if( "userName" in configJson and 
    "appId" in configJson and 
    verifyAppId(configJson["appId"]) and
    verifySensorData() and 
    "appName" in configJson and 
    "algorithms" in configJson ):
        return "valid"
    else:
        return "invalid"


app = Flask(__name__,template_folder='../../dashboard/src') 
@app.route('/uploadScheduleConfig', methods = ['POST']) 
def uploadScheduleConfig(): 
    if request.method == 'POST':
        f = request.files['file']
        configJson = json.load(f)
        status = validateConfig(configJson)
        print("status:",status)
        # status = "valid"
        if(status == "invalid"):
            return "error in scheduleConfig.json File!"
        appInstanceId = globalId()
        configJson["globalId"] = str(appInstanceId)
        # configJson is dictionary , send to scheduler 
        # print("*********************",type(configJson["localId"]))
        producer.send(schedulerTopicName,configJson)
        producer.flush()

        # fileName = str(appInstanceId) + "_scheduleConfig.json"
        # filePath = "../scheduleConfigurationsFile/" + fileName
        # print("filePath:",filePath) 
        # with open(filePath, "w") as outfile: 
        #     json.dump(configJson, outfile)
        # outfile.close()
        # sendFileInTopic(filePath)
    # return str(appInstanceId)
    message={'zip':-1,'schedule':appInstanceId}
    return render_template('index.html',message=message)


#register service
def registerService():
   mon.register()
    
#send heartbeat
def sendHeartBeat():
   mon.heartBeat()

if __name__ == '__main__':
    registerService()
    tq=threading.Thread(target=sendHeartBeat)
    tq.start()

    data = {}
    if(path.exists(fileName) != True):
        data[1]=1
        writeFile(data)
    f=open(fileName,"r")
    data=json.load(f)
    
    app.run(debug = False,host=HOST, port=SCHEDULER_PORT)
