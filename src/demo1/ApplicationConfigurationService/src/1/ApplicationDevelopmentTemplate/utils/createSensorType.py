import sys
import json
import os
intend_count=0
def applyIntend(fd):
    global intend_count
    for i in range(intend_count):
        fd.write('\t')

#no changes needs to be done in this
def createGetMethod(fieldName,fd):
    global intend_count
    applyIntend(fd)
    methodName='get'+fieldName
    fd.write('def '+methodName+'(self):\n')
    intend_count+=1
    applyIntend(fd)
    #return sensorManeger_get(self.label,'Temprature')
    fd.write('return baseAPI.get(self.label,\''+fieldName+'\')\n')
    intend_count-=1

#
def createControlMethod(fieldName,fd):
    global intend_count
    applyIntend(fd)
    methodName=fieldName
    fd.write('def '+methodName+'(self,dict):\n')
    intend_count+=1
    applyIntend(fd)
    #return sensorManeger_get(self.label,'Temprature')
    fd.write('baseAPI.applyControl(self.label,\''+fieldName+'\',dict)\n')
    intend_count-=1


#done.
def createConstructor(fd):
    global intend_count
    applyIntend(fd)
    fd.write('def __init__(self,l):\n')
    intend_count+=1
    applyIntend(fd)
    fd.write('self.label=l\n')
    intend_count-=1

def createFile(jsonFile,deviceName,targetPath):#it is just the name of the json file not the file.
    global intend_count
    intend_count=0
    print(jsonFile)
    print(targetPath)
    print(deviceName)
    print('printing till here')
    f=open(jsonFile,'r')
    deviceJson=json.load(open(jsonFile))
    print('not printing here')
    print(deviceJson)
    sensorJson=deviceJson['sensors']
    controlJson=deviceJson['controls']
    f=open(targetPath+deviceName+'.py','w')
    applyIntend(f)
    f.write('import baseAPI\n')
    f.write('class '+deviceName+':\n')
    intend_count+=1
    createConstructor(f)
    for sensor in sensorJson.keys():
        createGetMethod(sensor,f)
    for control in controlJson.keys():
        createControlMethod(control,f)
    #we are done
    f.close()


#starting the creation of library.
print('creating all the library.....')
path_to_json_config='./../configFiles/sensorTypes/'
targetPath='./../src/'
file_list=os.listdir(path_to_json_config)
for jsonfile in file_list:
    createFile(path_to_json_config+jsonfile,jsonfile[:-5],targetPath)