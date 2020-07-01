from werkzeug.security import generate_password_hash, check_password_hash
from flaskblog import db, app, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id)) 

class User(db.Model, UserMixin): 
	userid = db.Column(db.Integer, primary_key=True) 
	username = db.Column(db.String(20), unique=True, index=True)
	email = db.Column(db.String(120), unique=True, index=True)
	password_hash = db.Column(db.String(60)) 


	def set_password(self,password):
		self.password_hash = generate_password_hash(password)


	def check_password(self,password):
		return check_password_hash(self.password_hash, password)


	def getJsonData(self):
		return {"username": self.username, "email": self.email} 
		
