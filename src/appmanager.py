import sys
import json
import requests
from flask import jsonify
from flask import Flask
from flask import request
import json
from flask import render_template
from flask import jsonify
import zipfile
import os

app = Flask(__name__)
ids = 0




@app.route('/')
def submitApplication():
    return render_template('home.html')

@app.route('/receiveFile/',methods=['POST', 'GET'])
def receiveFile():
	global ids

	f = request.files["file"]
	f.filename  = str(ids)
	f.save("./Repository/"+ f.filename+".zip")

	with zipfile.ZipFile("./Repository/"+ f.filename+".zip","r") as zip_ref:
		zip_ref.extractall("./Repository/"+ f.filename)
	
	os.remove("./Repository/"+ f.filename+".zip")

	url = "http://localhost:5005/verify/"

	data = {"AppID": ids}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	res = requests.post(url, data=json.dumps(data), headers=headers)

	if res =="ok":
		ids+=1
	else:
		pass
		# os.remove("./Repository/"+ f.filename)
	
	ids+=1

	return "File Has been Received"

if __name__ == "__main__":
    # recording_on = Value('b', True)

    app.run(debug=True, port=5003)
