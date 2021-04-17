#this should be working.
from pymongo import MongoClient
client=MongoClient('mongodb+srv://nanu:merapassword@cluster0.hzfix.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=client.get_database('friday')
groupTypeCollection=db.groupType
groupInstanceCollection=db.groupIns
groupId=0
def registerGroup(jsonData):
    global groupTypeCollection
    groupTypeCollection.insert_one(jsonData)

def registerGroupInstance(jsonData):
    global groupInstanceCollection
    global groupId
    jsonData['groupId']=str(groupId)
    groupId+=1
    groupInstanceCollection.insert_one(jsonData)

def getGroupInstance(groupId):
    global groupInstanceCollection
    return groupInstanceCollection.find_one({'groupId':groupId})

