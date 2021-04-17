#template code for node maneger.
from flask import Flask,request,jsonify
import loadAnalyser
app=Flask(__name__)
#this method calculates the load in the machine and returns it.
@app.route('/getNodeLoad')
def getNodeLoad():
    print('querry to get load of this node')
    cpu_load=loadAnalyser.getCpuUsage()
    mem_load=loadAnalyser.getMemUsage()
    jsonret={'cpu':cpu_load,'mem':mem_load}    
    return jsonify(jsonret)
if __name__=='__main__':
    app.run(debug=True,port=5000)
