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

@app.route('/verify/',methods=['POST'])
def verify():
	jsondata = request.get_json()

	
	print("File verified")
	# Write your code here
	#if ok kisi application Repository naam ke folder me id naam ke folder me save krwana hai 
	return "ok"


if __name__ == "__main__":
   # recording_on = Value('b', True)
   
   app.run(debug=True,port=5005)
   