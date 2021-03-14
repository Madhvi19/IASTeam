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



typeMapping={Temperature:[t1,t2,t3,t4],InfraRed:[i1,i2,i3,i4]}

#pop whenever anything is used and put that in used dict

used={Temperature:[],Infrared:[]}
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



@app.route('/runApp',methos=['POST','GET'])
def runApp():

    jsondata = request.get_json()
    appID=jsondata('appid')
    data={}
    labels={}
    
    #form the path name and get the contents .json file to know what is to be run
    for filename in glob.glob('Repository/'+str(appID)):
        if(filename=='Contents.json'):
            data=json.load(filename)
        if(filename=='Labels.json'):
            labels=json.load(filename)


    mainFile=data['MainFile']
    status=bindSensor(appID,labels)
    os.system('python3 '+mainFile)
    # os.system('python my_file.py')



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
   




