import sys
import json
import requests
from flask import jsonify
from flask import Flask
from flask import request
import json
from flask import render_template
from flask import jsonify

app = Flask(__name__)
ids = 0

@app.route('/')
def submitApplication():
    return render_template('home.html')
    # jsondata = request.get_json()
	
    # Write your code here to assign id to the appln

    # once the data is received and an id is associated with it , send the data with id to deployer to verify


    # return if the app was deployed succesfully after verification from the deployers end
    # return abc

@app.route('/receiveFile/',methods=['POST', 'GET'])
def receiveFile():
    global ids
	if request.method == 'POST':
		f = request.files['file']
        f.save(f.filename)
         
		url = "http://localhost:5005/verify/"

        data = {"AppID": ids}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post(url, data=json.dumps(data), headers=headers)

        response_dict = json.loads(res.text)

        if response_dict == "ok":
            ids+=1
        else:
            

	return "File Has been Received"


if __name__ == "__main__":
    # recording_on = Value('b', True)

    app.run(debug=True, port=5003)
