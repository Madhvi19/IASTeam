from pymongo import MongoClient

class ConnectMongo(object):
    def __init__(self):
        # Connecting with mongo Server 
        # mongodb+srv://anuragsahu:<password>@sensors.r1efb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority 
        self.client = MongoClient("mongodb+srv://anuragsahu:321@sensors.r1efb.mongodb.net/sensorRegistry?retryWrites=true&w=majority")
        self.database = self.client.get_database("sensorRegistry") # fill the collection name here ask Pradeep
        self.SensorType = self.database.sensor_types
        self.SensorInstance = self.database.sensor_instances
        self.sensor_id = 0
    
    def GetAllSensorTypes(self):
        AllSensorTypes = []
        sensorTypes = list(self.SensorType.find({}))
        for i in sensorTypes:
            AllSensorTypes.append(i['name'])
        return AllSensorTypes
    
    def checkSensorID(self, SensorInstance):
        AllSensorInstances = []

    def GetSensorID(self):
        sensorIds = []
        sensorInstances = list(self.SensorInstance.find({}))
        for i in sensorInstances:
            sensorId = i["sensorid"]
            sensorIds.append(sensorId)
        if(len(sensorIds) == 0):
            self.sensor_id = 0
        else:
            self.sensor_id = max(sensorIds) + 1
        return self.sensor_id
    
    def SensorTypeRegistration(self, sensorType):
        # Check if the sensor type name exists
        sensorTypesPresent = self.GetAllSensorTypes()
        sensor_type = sensorType['name']
        if(sensor_type in sensorTypesPresent):
            return [False, "Sensor type with this name is already Registered"]
        # Register This sensor Type
        self.SensorType.insert_one(sensorType)
        return [True, "Successfully Added Sensor Type"]

    def SensorInstanceRegistration(self, SensorInstance):
        sensorTypesPresent = self.GetAllSensorTypes()
        SensorType = SensorInstance["sensorType"]
        SensorInstance["sensorid"] = self.GetSensorID()
        print(sensorTypesPresent)
        if(SensorType not in sensorTypesPresent):
            return [False, "Sensor type with this name is Not Avilable, Please Register this sensor type first"]
        self.SensorInstance.insert_one(SensorInstance)
        return [True, "Successfully Added Sensor", SensorInstance["sensorid"]]

    #def getSensorURL(self, sensorID):
        #sensorInstance = list(self.SensorInstance.find({"sensorid" : sensorID}))
        #if(len(sensorInstance) == 0):
            #return "invalid sensor id"
        #return sensorInstance[0]["sensorurl"]

connectMongo = ConnectMongo()
