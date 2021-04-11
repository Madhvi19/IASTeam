# Mongo DB test Code
import requests
import json
from ConnectMongo import connectMongo

# sensor Type
bulb = {
    "name":"Bulb",  ## sensor type name
    "sensors":{
        "color":"int",
        "intensity":"float"
        },
    "controls":{
        "changeColor":{"color_r":"int","color_g":"int","color_b":"int"},
        "changeIntensity":{"intensity":"int"}
        }
}

# sensor Instances
s1 = {
    "sensorName" : "Bulb1",
    "sensorurl" : "Topic0",
    "Location" : "<A1:A2:A3....>",
    "sensorType" : "Bulb"
}

s2 = {
    "sensorName" : "Bulb2",
    "sensorurl" : "Topic1",
    "Location" : "<A1:A2:A3....>",
    "sensorType" : "Bulb"
}

## registering sensorType
response = requests.post("http://localhost:7006/registerType/",json=json.dumps(bulb)).json()

##registering sensorInstance
response = requests.post("http://localhost:7006/registerInstance/", json=json.dumps(s1)).json()
response = requests.post("http://localhost:7006/registerInstance/", json=json.dumps(s2)).json()
