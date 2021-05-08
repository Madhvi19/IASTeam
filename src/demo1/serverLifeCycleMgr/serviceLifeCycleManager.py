
#acts as a consumer of monitoringUnit
#get the corresponding  code from the platform repo
# Go to a freely avaialble server by ssh
# run nodeUnit.py on it

#run the failed service on the new node


import startServices
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
import pymongo
sourceDir='platformRepository'
avaialableNodes='freeNodeList.json' 
pathToNodeUNit='nodeUnit.py'


def createLogs():
    consumer = KafkaConsumer('logging',
                                bootstrap_servers=['kafka:9092'],
                                auto_offset_reset='earliest',
                                enable_auto_commit=True,
                                group_id='my-group',
                                value_deserializer=lambda x: loads(x.decode('utf-8')))    
    while(True):
        for message in consumer:
            serviceName = message.value['serviceName']
            state = message.value['loggingInfo']

    

            f = open(serviceName, "a")
            f.write(state)
            f.close()



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
    

def editServiceName(configFiles):
    global count
    print("trying to open ",configFiles)
    configFileToRename=open(configFiles)
    
    tempFile=json.load(configFileToRename)
    print("tempFile")
    print(tempFile)
    tempName=tempFile["serviceName"]
    tempName=tempName+"_"+str(count)
    count+=1
    print(tempName)
    print("old ",tempFile['serviceName'])
    tempFile['serviceName']=tempName
    print("new ",tempFile['serviceName'])
    configFileToRename.close()

    #create a temp file to rename and then delete it
    
    print("opening temp file")
    
    
    configFileRenamed=open("tempfile.json","w")
    print(configFileRenamed)
    sta=json.dump(tempFile,configFileRenamed)
    print(sta)
    configFileRenamed.close()

def createClient():
    '''
        A kafka client listena on 'machineAddr' topic 
    '''

    consumer = KafkaConsumer('machineAddr',
                            bootstrap_servers=['localhost:9092'],
                            auto_offset_reset='earliest',
                            enable_auto_commit=True,
                            group_id='my-group',
                            value_deserializer=lambda x: loads(x.decode('utf-8')))
    return consumer

def getMachineAddr(consumer):
    for message in consumer:
        info = message.value
        return info['ip'], info['port'], info['username'], info['password']


def setUpNewServer(serviceName):
    
    status="OK"
    serviceName=serviceName.split("_")[0]
    file=open(avaialableNodes)
    freeNodes=json.load(file)
    if( len(freeNodes["Nodes"])==0):

        status = "NOT OK"
    
    else:
        
        

        sourceFiles,configFiles=getPathToService(serviceName)

        myclient = pymongo.MongoClient("mongodb+srv://Test:Anurag@appregcluster.polvf.mongodb.net/numtest?retryWrites=true&w=majority")
        mydb = myclient["initializer"]
        mycol=mydb["initializer"]
        
        #remove the ro from db
        for row in mycol.find():
                print("Row:"+str(row))
                if(row['Services'][0]==serviceName):

                    var=mycol.delete_one(row)
                    print(var)
                    break
        #request a new server
        consumer = createClient()
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

        topicName='toServerLCM'
        producer.send(topicName, serviceName) 
            
        ip, port, username, password = getMachineAddr(consumer)


        # ip = freeNodes["Nodes"][0]["ip"]
        # username = freeNodes["Nodes"][0]["username"]
        # password = freeNodes["Nodes"][0]["password"]
        # port = freeNodes["Nodes"][0]["port"]
        # print(username," ",password," ",port," ",ip)
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
        
        
        # ssh_client.exec_command("python3 nodeUnit.py ")
        
        

       #edit the json
        editServiceName(configFiles)
        
        #copy the config files
        ftp_client=ssh_client.open_sftp()
        ftp_client.put("tempfile.json",serviceName+'/conf/config.json')
        ftp_client.close()
        os.remove("tempfile.json")


        print("copied the config and src files")

        #get how to run the service
        confRun=open(configFiles)
        runService=json.load(confRun)



        #Run the code files

        print(" serviceName: "+serviceName)
        print("command"+'cd '+serviceName+'/src')
        stdin, stdout, stderr=ssh_client.exec_command('cd '+serviceName+'/src;'+runService['run_command'],get_pty=True)
        # for line in iter(stdout.readline, ""):
        #      print(line, end="")
        # print("&&&&&&&&&&&&&&&")
        # print(runService['run_command'])

        # filename=runService['run_command'].split(" ")[1].strip()
        # print("filename is ",filename)
        # # print('gonna run python '+serviceName+'/src/'+filename)
        # # stdin, stdout, stderr=ssh_client.exec_command('python '+serviceName+'/src/'+filename)
        # # stdin, stdout, stderr=ssh_client.exec_command(runService['run_command'])
        # for line in iter(stderr.readline, ""):
        #      print(line, end="")
        # for line in iter(stdout.readline, ""):
        #      print(line, end="")
        
        print("running the src files")
        # /print(stdout.readlines())
        # print(stderr.readlines())
        # for entry in toStart:
        #     print(entry)
        #     ssh_client.exec_command("python3 "+entry)

        
        ssh_client.close()


        



     





        
        
        
        
        
        
        
        # : freeNodes["Nodes"][0]
        
        file=open(avaialableNodes,"w")
        json.dump(freeNodes,file)
        file.close()
    
        return status

        
        
    


    



def restartService():
     
    consumer = KafkaConsumer('restartService',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))
    while(True):
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


#setUpNewServer("scheduler")
if __name__=="__main__":
    ''' To initialise all the services'''
    startServices.getSignal()

    ''' Restart service '''
    th=threading.Thread(target=restartService)
    th.start()
    
    ''' Logging '''
    th2=threading.Thread(target=createLogs)
    th2.start()

    



#acts as a consumer of monitoringUnit
#get the corresponding  code from the platform repo
# Go to a freely avaialble server by ssh
# run nodeUnit.py on it

#run the failed service on the new node




