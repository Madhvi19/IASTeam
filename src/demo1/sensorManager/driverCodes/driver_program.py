from ConnectCouch import connectCouch
import json
import requests

speaker = {
    "speaker_new" : {
        "seek" : "int",
        "volume" : "float",
        "play" : "boolean",
        "title" : "string"
    },
    "controls" : {
        "increaseVolume" : {
            "step" : "int",
            "mute" : "boolean"
        },
        "increaseSeek" : {
            "step" : "int"
        }
    }
}

s = {
    "sensorName" : "SensorName",
    "sensorid" : "abc",
    "sensorurl" : "<public-IP of intermediate server>",
    "sensorType" : "speaker",
    "description":"this is the 4th bulb in himalaya room number 3"
}
response = requests.post("http://localhost:5000/registerInstance/", json=json.dumps(s)).json()
response = requests.post("http://localhost:5000/registerType/",json=json.dumps(speaker)).json()

