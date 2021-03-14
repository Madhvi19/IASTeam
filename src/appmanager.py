import sys
import json
import requests
from flask import jsonify
from flask import Flask
from flask import request
import json
from flask import render_template
from flask import jsonify






@app.route('/submitApplication/',methods=['POST'])
def submitApplication():
	jsondata = request.get_json()

	# Write your code here to assign id to the appln 




	# once the data is received and an id is associated with it , send the data with id to deployer to verify
	url = "http://localhost:5000/verify/" 

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	res = requests.post(url, data=json.dumps(data), headers=headers)
	
	response_dict = json.loads(res.text)

	# return if the app was deployed succesfully after verification from the deployers end
	return abc

if __name__ == "__main__":
   # recording_on = Value('b', True)
   
   app.run(debug=True,port=5003)
   