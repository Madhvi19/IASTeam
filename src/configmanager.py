import sys
import json
import requests
from flask import jsonify
from flask import Flask
from flask import request
import json
from flask import render_template
from flask import jsonify

import os
import glob


app = Flask(__name__)
typeMapping={"Temperature":["t1","t2","t3","t4"],"InfraRed":["i1","i2","i3","i4"]}

#pop whenever anything is used and put that in used dict

used={"Temperature":[],"InfraRed":[]}
#store the label to physical mappinf here
labelMapping={}

def bindSensor(appID,data):
    status=1
    keys_labels=data.keys()
    for entry in keys_labels:
        available=typeMapping[entry]
        toUse=available.pop()
        typeMapping[entry]=available
        used[entry].append(toUse)
        labelMapping[entry]=toUse



    return status



@app.route('/runApp/',methods=['POST','GET'])
def runApp():

    jsondata = request.get_json()
    appID=jsondata['appid']
    print("*************", appID)
    data={}
    labels={}
    
    #form the path name and get the contents .json file to know what is to be run
    for filename in glob.glob('/home/madhvi/Semester4/InternalsOfApplicationServer/Hackathon1/IASTeam/src/Repository'+str(appID)):
        print("*******************", filename)
        if(filename=='Contents.json'):
            data=json.load(filename)
            print("******************",data)
        if(filename=='Labels.json'):
            labels=json.load(filename)
            print("*********************",labels)

    mainFile=data['MainFile']
    status=bindSensor(appID,labels)
    os.system('python3 '+mainFile)
    # os.system('python my_file.py')

    # return "Temperature is high"

@app.route('/getMapping/',methods=['POST'])
def getMapping():
    jsondata = request.get_json()
    sensorLabel=jsondata['label']
    sensorID=labelMapping[sensorLabel]
    send={'ID':sensorID}
    return json.dumps(send)









if __name__ == "__main__":
   # recording_on = Value('b', True)
   
   app.run(debug=True,port=5112)
   




