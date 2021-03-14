import sys
import json
import requests
from flask import jsonify
from flask import Flask
from flask import request
import json
from flask import render_template
from flask import jsonify






@app.route('/verify/',methods=['POST'])
def verify():
	jsondata = request.get_json()

	# Write your code here
	return ok/not ok

if __name__ == "__main__":
   # recording_on = Value('b', True)
   
   app.run(debug=True,port=5003)
   