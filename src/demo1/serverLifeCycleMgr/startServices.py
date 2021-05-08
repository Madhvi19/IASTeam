import pymongo
from datetime import datetime
from json import loads
from json import dumps
import json
import threading
import paramiko
import argparse
import time
import os 
from os import walk
from os import listdir
from kafka import KafkaConsumer
sourceDir='platformRepository'

siervicesToStart = ["MonitoringUnit","scheduler", "deployer", "appRepo", "sensorManager", "dashboard",  "runtimeManager"]
# servicesToStart=[]
def getSignal():
    # '''
    #     A kafka consumer, gets signal to run all the services
    #     and call startService() for every service
    # '''
    global servicesToStart
    consumer = KafkaConsumer('startService',
                            bootstrap_servers=['localhost:9092'],
                            auto_offset_reset='earliest',
                            enable_auto_commit=True,
                            group_id='my-group',
                            value_deserializer=lambda x: loads(x.decode('utf-8')))
    for message in consumer:
        print(message)
        for service in servicesToStart:
                startService(service)

    # for service in servicesToStart:
    #   startService(service)
    #   break
def sftpToNewNode(ftp_client,sourceFiles,destination):
    # ftp_client.put(pathToNodeUNit,pathToNodeUNit)
    toStart=[]
    
    for files in listdir(sourceFiles):

        print("filesss ",files)
        
        try:
            toStart.append(files)
            finalSourcePath=os.path.join(sourceFiles,files)
            ftp_client.put(finalSourcePath,destination+files)
        except:
            continue
    return toStart
    
    

def getMachineAddr(serviceName):
    # client = pymongo.MongoClient('localhost:27017')
    # collection = client.initializer.initializer
    # for document in collection.find():
    #   print(document)
    
    myclient = pymongo.MongoClient("mongodb+srv://Test:Anurag@appregcluster.polvf.mongodb.net/numtest?retryWrites=true&w=majority")
    mydb = myclient["initializer"]
    mycol = mydb["initializer"]


    for x in mycol.find():
        print(x," 90")
        print(x['name'])
        print(x['port'])
        print(serviceName)
        if(x['name'] == serviceName):
            print("matched")
            print(x['ip'],x['port'],x['username'],x['password'])
            return x['ip'], x['port'], x['username'], x['password']


def copyFiles():
    pass

def getPathToService(serviceName):
    global count
    finalPath=os.path.join(sourceDir,serviceName)
    # print("final path ", finalPath)
    sourceFiles=os.path.join(finalPath,'src')
    configFiles=os.path.join(finalPath,'conf/config.json')
    # print("sourceFiles", sourceFiles)
    # print("configFiles", configFiles)
    return sourceFiles,configFiles

def updateDB(serviceName):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["initializer"]
    mycol = mydb["initializer"]

    x = mycol.update({'container': serviceName}, {'$push': {'Services': serviceName}})

    print("************************Updated DB successfully*****************")

def startService(serviceName):
    '''
        1.  Retrieve the ip and port of the container with the
            name same as service which is to be started.r
        
        2.  SSH the machine.

        3.  From platform repo copy and paste the whole directory
            structure  
        
        4.  From congif.json get the name of the file to run

        5. run the file

        6. On successfully running the service inserr it's name 
           into services[] in db

    '''
    print("Service Name is", serviceName)

    sourceFiles,configFiles=getPathToService(serviceName)
    print("sourceFiles= ",sourceFiles)

    ip, port, username, password = getMachineAddr(serviceName)
    print(username," ",password," ",port," ",ip)

    ssh_client =paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,port=port,username=username,password=password)

    ssh_client.exec_command('mkdir '+serviceName)
    ssh_client.exec_command('mkdir '+serviceName+'/src')
    ssh_client.exec_command('mkdir '+serviceName+'/conf')

    ftp_client=ssh_client.open_sftp()
    destination=serviceName+'/src/'
    toStart=sftpToNewNode(ftp_client,sourceFiles,destination)

        
    ftp_client.close()

    ftp_client=ssh_client.open_sftp()
    ftp_client.put(configFiles,serviceName+'/conf/config.json')
    ftp_client.close()
    # os.remove("tempfile.json")


    print("copied the config and src files")

    confRun=open(configFiles)
    runService=json.load(confRun)

    print(" serviceName: "+serviceName)
    print("command"+'cd '+serviceName+'/src')
    stdin, stdout, stderr=ssh_client.exec_command('cd '+serviceName+'/src;'+runService['run_command'],get_pty=True)


    filename=runService['run_command'].split(" ")[1].strip()
    print("filename is ",filename)
    # print('gonna run python '+serviceName+'/src/'+filename)
    # stdin, stdout, stderr=ssh_client.exec_command('python '+serviceName+'/src/'+filename)
    # stdin, stdout, stderr=ssh_client.exec_command(runService['run_command'])

    updateDB(serviceName)
    
