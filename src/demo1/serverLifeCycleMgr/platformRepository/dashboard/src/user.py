from flask import Flask, request, flash, url_for, redirect, render_template  
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder='./')  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ias_login.sqlite3'  
app.config['SECRET_KEY'] = "secret key"  
  
db = SQLAlchemy(app)  
  
class User(db.Model):  
	id = db.Column('id', db.Integer, primary_key = True)  
	name = db.Column(db.String(100), unique=True)  
	role = db.Column(db.String(50)) 
	password = db.Column(db.String(100)) 
   
  
	def __init__(self, name, role,password):  
		self.name = name  
		self.role = role  
		self.password=generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password, password)
 
# from user import db
# db.create_all()
# from user import User
# admin1 = User('admin1','admin','admin1')
# admin2 = User('admin2','admin','admin2')
# u1 = User('u1','user','u1')
# u2 = User('u2','user','u2')
# pd1 = User('pd1','developer','pd1')
# pd2 = User('pd2','developer','pd2')
# db.session.add(admin1)
# db.session.add(admin2)
# db.session.add(u1)
# db.session.add(u2)
# db.session.add(pd1)
# db.session.add(pd2)
# db.session.commit()

