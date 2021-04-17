# Mongo DB test Code

from ConnectMongo import connectMongo

speaker = {
    "speaker_new_2" : {
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
    "Location" : "<A1:A2:A3....>",
    "sensorType" : "speaker_new_2"
}

response = requests.post("http://localhost:5000/registerInstance/", json=json.dumps(s)).json()
response = requests.post("http://localhost:5000/registerType/",json=json.dumps(speaker)).json()
