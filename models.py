# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# app = Flask(__name__)

db = SQLAlchemy()
class User(db.Model):
    __tablename__ =  'user'
    user_id = db.Column(db.String, primary_key=True)
    user_password = db.Column(db.String, nullable=False)
    # user = db.relationship("Todo", backref= "user")
    lists = db.relationship("List", backref= "user")
    def __repr__(self):
        return "<User's ID is %r>" % self.user_id

class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    list_name = db.Column(db.String, nullable=False)
    list_description = db.Column(db.String)
    user_id = db.Column(db.String,db.ForeignKey("user.user_id"), nullable=False)
    tasks = db.relationship("Todo", backref= "list")
    
    # list = db.relationship("Todo", backref="list")
    def __repr__(self):
        return "<List's ID is %r>" % self.list_id


class Todo(db.Model):
    __tablename__ = 'todo'
    todo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    todo_title = db.Column(db.String, nullable = False)
    todo_content = db.Column(db.String, nullable = False)
    todo_deadline = db.Column(db.String(10), nullable = False)
    todo_created_time = db.Column(db.String(10), nullable = False)
    todo_completed_time = db.Column(db.String(10), nullable = True)
    todo_status = db.Column(db.String, nullable = False)  # if task is complete "Completed" else "Pending"
    list_id = db.Column(db.String,db.ForeignKey("list.list_id"), nullable=False)























