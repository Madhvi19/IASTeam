from pymongo import MongoClient
client=MongoClient('mongodb+srv://anuragsahu:321@sensors.r1efb.mongodb.net/sensorRegistry?retryWrites=true&w=majority')
db=client.get_database('sensorRegistry')
records=db.sensor_types
records.delete_many({})
print('sensor types removed.....')
records=db.sensor_instances
records.delete_many({})
print('sensor instances removed.....')
