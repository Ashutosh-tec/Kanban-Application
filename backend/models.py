# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(2555))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    lists = db.relationship("List", backref= "user")
    def __repr__(self):
        return "<User's ID is %r>" % self.id

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer, primary_key = True)
    list_name = db.Column(db.String, nullable=False)
    list_description = db.Column(db.String)
    user_id = db.Column(db.String,db.ForeignKey("user.id"), nullable=False)
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























