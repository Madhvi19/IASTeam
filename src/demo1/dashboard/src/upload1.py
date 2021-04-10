from flask import Flask,render_template,send_from_directory,request
import threading
import time
import monitorInit as mon
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy  
# from user import User
#register service
def registerService():
   mon.register()
    
#send heartbeat
def sendHeartBeat():
   mon.heartBeat()

app = Flask(__name__, template_folder='./')  
HOST="127.0.0.1"
DASHBOARD_PORT=7001 

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ias_login.sqlite3'  
# app.config['SECRET_KEY'] = "secret key"    
# db = SQLAlchemy(app)

# @app.route('/dashboard',methods=['POST'])  
# def upload():  
	
# 	print(User.query.all())
# 	print(request.form.get('username'))
# 	user = User.query.filter_by(name=request.form.get('username')).first()
# 	if user is None or not user.check_password(request.form.get('pwd')):
# 		return render_template("login.html",message="Incorrect credentials")
		
# 	else:
# 		message={'zip':-1,'schedule':-1,'role':user.role}
# 		return render_template("index.html",message=message)
		

@app.route('/')  
def upload(): 	
	message={'zip':-1,'schedule':-1}
	return render_template("index.html",message=message)

@app.route('/downloadTemplate',methods=['POST'])
def template():
    return send_from_directory('./', 'applicationDevelopmentTemplate.zip', as_attachment=True)






  
if __name__ == '__main__':  
    registerService()
    tq=threading.Thread(target=sendHeartBeat)
    tq.start()
    app.run(debug = False,host=HOST,port = DASHBOARD_PORT)  