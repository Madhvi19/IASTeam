from pymongo import MongoClient
client=MongoClient('mongodb+srv://nanu:merapassword@cluster0.hzfix.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=client.get_database('friday')
records=db.scheduleInfo
records.delete_many({})
print('scheduler documents suhaaa.....')
records=db.rtmInfo
records.delete_many({})
print('rtm documents suhaaa.....')