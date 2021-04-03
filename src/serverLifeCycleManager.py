
#acts as a consumer of monitoringUnit
#get the corresponding  code from the platform repo
# Go to a freely avaialble server by ssh
# run nodeUnit.py on it

#run the failed service on the new node

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



count=1
def getPathToService(serviceName):
    global count
    finalPath=os.path.join(sourceDir,serviceName)
    print("final path "+finalPath+" 999")
    sourceFiles=os.path.join(finalPath,'src')
    configFiles=os.path.join(finalPath,'conf/config.json')
    print(sourceFiles)
    print(configFiles)
    return sourceFiles,configFiles


def sftpToNewNode(ftp_client,sourceFiles):
    ftp_client.put(pathToNodeUNit,pathToNodeUNit)
    toStart=[]
    
    for files in listdir(sourceFiles):
        print("filesss ",files)
        toStart.append(files)
        finalSourcePath=os.path.join(sourceFiles,files)
        ftp_client.put(finalSourcePath,"src/"+files)
    return toStart
    

def editServiceName(configFiles):
    print("trying to open ",configFiles)
    configFileToRename=open(configFiles)
    
    tempFile=json.load(configFileToRename)
    print("tempFile")
    print(tempFile)
    tempName=tempFile["serviceName"]
    tempName=tempName+"_"+str(count)
    print(tempName)
    print("old ",tempFile['serviceName'])
    tempFile['serviceName']=tempName
    print("new ",tempFile['serviceName'])
    configFileToRename.close()
    print("opening ",configFiles)
    
    
    configFileRenamed=open(configFiles,"w")
    print(configFileRenamed)
    sta=json.dump(tempFile,configFileRenamed)
    print(sta)
    configFileRenamed.close()

def setUpNewServer(serviceName):
    
    status="OK"
    file=open(avaialableNodes)
    freeNodes=json.load(file)
    if( len(freeNodes["Nodes"])==0):

        status = "NOT OK"
    
    else:
        
        

        sourceFiles,configFiles=getPathToService(serviceName)
        ip = freeNodes["Nodes"][0]["ip"]
        username = freeNodes["Nodes"][0]["username"]
        password = freeNodes["Nodes"][0]["password"]
        port = freeNodes["Nodes"][0]["port"]
        print(username," ",password," ",port," ",ip)
        ssh_client =paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip,port=port,username=username,password=password)
        ssh_client.exec_command('mkdir src')
        ssh_client.exec_command('mkdir conf')
        
        ftp_client=ssh_client.open_sftp()

        toStart=sftpToNewNode(ftp_client,sourceFiles)

        
        ftp_client.close()
        # print("done")
        
        
        ssh_client.exec_command("python3 nodeUnit.py ")
        
        

       #edit the json
        editServiceName(configFiles)
        

        ftp_client=ssh_client.open_sftp()
        ftp_client.put(configFiles,'conf/config.json')
        ftp_client.close()
        print("phew!!! DONE")

        
        #Run the code files

        for entry in toStart:
            print(entry)
            ssh_client.exec_command("python3 "+entry)

        
        ssh_client.close()


        



     





        
        
        
        
        
        
        
        # del freeNodes["Nodes"][0]
        
        file=open(avaialableNodes,"w")
        json.dump(freeNodes,file)
        file.close()
    
        return status

        
        
    


    



def startService():
     
    consumer = KafkaConsumer('startService',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        # for message in consumer:
        print(message)
        details = message.value
        #get the name of the service first eg: Sscheduler_1 now truncate the _num part to get the original name to find the corresponding code and config details
        serviceName=details['name']
        serviceName=serviceName.split("_")[0]
        status=setUpNewServer(serviceName)
        if(status=="OK"):
            print("started server")


setUpNewServer("scheduler")



    



#acts as a consumer of monitoringUnit
#get the corresponding  code from the platform repo
# Go to a freely avaialble server by ssh
# run nodeUnit.py on it

#run the failed service on the new node




