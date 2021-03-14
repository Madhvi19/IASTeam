from flask import Flask
import random
import json
from flask import request
import time
import requests
import numpy as np
app=Flask(__name__)


while True:

    values = np.random.choice([0, 1], size=30, p=[.1, .9])
    url = "http://localhost:5999/pushData/"
    toClient ={'id':"i2",'data':list(values)}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post(url, data=json.dumps(toClient), headers=headers)
    # msg=
    time.sleep(0.8)
    # return msg
