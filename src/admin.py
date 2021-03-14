import sys
import json
import requests

import time

url = "http://localhost:5112/runApp/"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data={'appid':0}
res = requests.post(url, data=json.dumps(data), headers=headers)
print("***********", res)
# response_dict = json.loads(res.text)
# print(response_dict)
# print(response_dict['result'])