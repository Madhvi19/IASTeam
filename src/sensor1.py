from flask import Flask
from flask import Flask
import random
import json
from flask import request
import time
import requests
import numpy as np
app=Flask(__name__)



url="http://127.0.0.1:5999/pushData/"
while True:

    value=random.randint(20,30)
    url = "http://localhost:5999/pushData/"
    toClient ={'id':"t1",'data':value}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post(url, data=json.dumps(toClient), headers=headers)
    # msg=
    time.sleep(0.8)
    # return msg
