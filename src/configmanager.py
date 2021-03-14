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



typeMapping={Temperature:[t1,t2,t3,t4],Infrared:[i1,i2,i3,i4]}

#pop whenever anything is used and put that in used dict

used={Temperature:[],Infrared:[]}
#store the label to physical mappinf here
labelMapping={}

@app.route('/runApp',methos=['POST','GET'])
def runApp():

    jsondata = request.get_json()
    appID=jsondata('appid')
    #form the path name and get the contents .json file to know what is to be run
    os.path.join("")





@app.route('/getMapping/',methods=['POST'])
def getMapping():
    jsondata = request.get_json()
    sensorLabel=jsondata['label']
    sensorID=labelMapping[sensorLabel]
    send={'ID':sensorID}
    return json.dumps(send)


@app.route('/bindSensor',methods=['POST'])
def bindSensor():





if __name__ == "__main__":
   # recording_on = Value('b', True)
   
   app.run(debug=True,port=5112)
   




