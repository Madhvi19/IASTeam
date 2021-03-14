import sys
import json
import requests
from flask import jsonify
from flask import Flask
from flask import request
import json
from flask import render_template
from flask import jsonify


data_dict={t1:[],t2:[],t3:[],t4:[],i1:[],i2:[]}


@app.route('/pushData/',methods=['POST'])
def pushData():
	jsondata = request.get_json()
    # jsondata = request.get_json()
	sensorID=jsondata['id']
	sensorData=jsondata['data']
    data_dict[sensorID].extend(sensorData)




@app.route('/getData/',methods=['POST'])
def getData():
    #Whenever a request for data comes, wipe out the enire data that was stored and pushdata adds to an empty list

	jsondata = request.get_json()
    sensorLabel=jsondata['label'] # This is the label that was assigned by app developer. You need to as the config mgr to get the id of the sensor which the is mapped to
	
    url = "http://localhost:5112/getMapping/"
    mapping={'label':sensorLabel}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	res = requests.post(url, data=json.dumps(mapping), headers=headers)
	
	response_dict = json.loads(res.text)
	print(response_dict)
    
    sensorID=response_dict['ID']

    dataToSend=data_dict[sensorID]
    data_dict[sensorID]=[]
    result ={'data':dataToSend}
    return json.dumps(result)



    # return dataToSend
    

