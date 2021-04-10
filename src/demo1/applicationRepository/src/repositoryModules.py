import os
import random 

applicationFolder = "../applications/"


def checkApplicationStatus(applicationName):
    listOfApplication = os.listdir(applicationFolder)
    for application in listOfApplication:
        if(application == applicationName):
            return True
    return False


def generateAppId():
    fileName = os.listdir(applicationFolder)
    fileList = []
    for file in fileName:
        fileList.append(int(file))
    
    newFileNum = random.randint(100,999)
    for fileNum in fileList:
        if(newFileNum == fileNum):
            newFileNum = random.randint(100,999)

    return newFileNum

# print(generateAppId())



# print(checkApplicationStatus('123.txt'))
# print(checkApplicationStatus('234.txt'))

