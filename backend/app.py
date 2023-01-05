from flask import Flask, render_template 
from models import db, User as User, List as List, Task as Task
from api.resource import api, Users
from flask_cors import CORS
from security import user_datastore, sec
from flask_security import hash_password



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






# @app.before_first_request
# def create_db():
#     db.create_all()
#     if not user_datastore.find_user(email="narendra@gmail.com"):
#         user_datastore.create_user(
#             username="narendra", email="narendra@gmail.com", password=hash_password("1234"))
#         db.session.commit()

#     if not user_datastore.find_role('admin'):
#         user_datastore.create_role(
#             name='Admin', description='Admin Related Role')
#     lst = List(list_id="001",list_name="1st",list_description="Blah", user_id="1")
#     db.session.add(lst)
#     db.session.commit()


@app.route('/')
def home():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
