import sys

def getData(label):
    url = "http://localhost:5111/getData/"

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	res = requests.post(url, data=json.dumps(label), headers=headers)
	
	response_dict = json.loads(res.text)
	print(response_dict)
	print(response_dict['data'])
	return(response_dict['data'])
def setData(label):
    pass
