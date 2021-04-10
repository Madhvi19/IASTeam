from flask import Flask
from flask import request
from flask import send_file,render_template
import json
import repositoryModules
import os
import os.path 
import threading
import time
import monitorInit as mon
flag=1

def registerService():
   global flag
   if(flag):
       print("flag"+str(flag)) 
       flag=0

       print("Hey I am registering.")
       mon.register()
    
#send heartbeat
def sendHeartBeat():
   mon.heartBeat()






app = Flask(__name__, template_folder='../../dashboard/src')

HOST="127.0.0.1"
APPLICATIONREPOSITORY_PORT = 7002

@app.route('/appIdVerification/', methods = ['POST'])
def appIdVerification():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    result = repositoryModules.checkApplicationStatus(data)
    return json.dumps(result)


@app.route('/generateAppId/', methods = ['POST'])
def generateAppId():
    result = repositoryModules.generateAppId()
    return json.dumps(result)


@app.route('/uploadZipInRepository', methods = ['POST'])
def uploadZipInRepository():
    if request.method == 'POST':
        f = request.files['file']
        appId = generateAppId()
        folderName = repositoryModules.applicationFolder + str(appId) + "/"
        print(appId)
        os.mkdir(folderName)
        print(folderName)
        f.save(folderName + f.filename)
    # return json.dumps(appId)
    message={'zip':appId,'schedule':-1}
    return render_template("index.html",message=message)


@app.route('/retrieve', methods = ['POST'])
def retrieve():
    
    x = request.json
    appId=x['appid']
    # appId = json.loads(jsondata)
    print("appId",appId)
    folderName = "../applications/" + (appId) + "/"
    print("folderName",folderName) 
    fileNames = os.listdir(folderName)
    print("fileNames",fileNames)
    file_to_return = fileNames[0]
    print("file_to_return",file_to_return)
    file_path = folderName + file_to_return
    print("file_path",file_path)
    return send_file(file_path)
    

#register service
def register():
    print("register...")
    registerService()
def flaskstart():
    app.run(debug=True,host=HOST,port=APPLICATIONREPOSITORY_PORT,use_reloader=False)

if __name__ == '__main__':
    
    folderName = "../applications"
    tp=threading.Thread(target=register)
    tp.start()
    
    tq=threading.Thread(target=sendHeartBeat)
    tq.start()
    

    # tr=threading.Thread(target=app.run)
    if(os.path.isdir(folderName) != True):
        os.mkdir(folderName)
     # debug=True, use_reloader=False
    tr=threading.Thread(target=flaskstart)
    tr.start()
    
