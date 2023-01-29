from flask import Flask, render_template, send_file 
from models import db, User as User, List as List, Task as Task
from api.resource import api, Users
from flask_cors import CORS
from security import user_datastore, sec
from flask_security import hash_password
from celery_system import *
import time



app = Flask(__name__)


CORS(app, support_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "thisissecret"
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'


db.init_app(app)
api.init_app(app)
sec.init_app(app, user_datastore)






@app.route('/')
def home():
    
    return render_template('dashboard.html')




if __name__ == "__main__":
    app.run(debug=True, port=5000)
