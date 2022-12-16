# from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class User(db.Model):
    __tablename__ =  'user'
    user_id = db.Column(db.Integer, primary_key=True)  #should store locally to get whenever needed
    user_name = db.Column(db.String, unique=True, nullable=False)  #needed for log in
    user_email = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    lists = db.relationship("List", backref= "user")
    def __repr__(self):
        return "<User's ID is %r>" % self.user_id

class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer, primary_key = True)
    list_name = db.Column(db.String, nullable=False)
    list_description = db.Column(db.String)
    user_id = db.Column(db.String,db.ForeignKey("user.user_id"), nullable=False)
    tasks = db.relationship("Task", backref= "list")
    
    # list = db.relationship("Todo", backref="list")
    def __repr__(self):
        return "<List's ID is %r>" % self.list_id


class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String, nullable = False)
    task_content = db.Column(db.String, nullable = False)
    task_deadline = db.Column(db.String(10), nullable = False)
    task_created_time = db.Column(db.String(10), nullable = False)
    task_completed_time = db.Column(db.String(10), nullable = True)
    task_status = db.Column(db.String, nullable = False)  # if task is complete "Completed" else "Pending"
    list_id = db.Column(db.String,db.ForeignKey("list.list_id"), nullable=False)























