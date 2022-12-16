from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from models import db, User as User, List as List, Task as Task

api = Api(prefix="/api")



#------------------USER---------------------
user_args = reqparse.RequestParser()
user_args.add_argument("user_name",type=str,required=True)
user_args.add_argument("user_email",type=str,required=True)
user_args.add_argument("user_password",type=str,required=True)
user_output_fields = {
    'user_id' : fields.Integer,
    'user_name' : fields.String
}

class Users(Resource):
    @marshal_with(user_output_fields)
    def get(self,user_id):
        usr = User.query.filter_by(user_id=user_id).first()
        if usr:
            return usr, 200
        else:
            abort(404, message="User doesn't exist")

    @marshal_with(user_output_fields)
    def post(self): #add list
        args = user_args.parse_args()
        usr = User.query.filter_by(user_name=args['user_name']).first()
        if usr:
            abort(409, message = "User name already exist")
        usr = User(user_name=args['user_name'],user_email=args['user_email'], user_password=args['user_password'])
        db.session.add(usr)
        db.session.commit()
        return usr, 201
    def delete(self,user_id):
        usr = User.query.filter_by(user_id=user_id).first()
        if usr:
            db.session.delete(usr)
            db.session.commit()
            return "User successsfully deleted", 200
        else:
            abort(404, message = "User doesn't exist")


api.add_resource(Users, "/user/", "/user/<int:user_id>")


#------------------LIST---------------------
list_args = reqparse.RequestParser()
list_args.add_argument("list_name",type=str,required=True)
list_args.add_argument("list_description",type=str)
list_args.add_argument("user_id",type=int,required=True)
list_output_fields = {
    'list_id' : fields.Integer,
    'list_name' : fields.String,
    'list_description': fields.String
}

class Lists(Resource):
    @marshal_with(list_output_fields)
    def get(self,user_id):
        lists = List.query.filter_by(user_id=user_id).all() # return a list 
        # return lists, 201
        
        if len(lists) == 0:
            # return lists, 201
            abort(404, message = "List is not created for you.")
            # return "List is not created yet.", 404
        else:
            return lists, 200

    @marshal_with(list_output_fields)
    def post(self): #add list
        args = list_args.parse_args()
        print(args['list_name'])
        lists = List(list_name = args['list_name'], list_description = args['list_description'], user_id = args['user_id'])
        db.session.add(lists)
        db.session.commit()
        return lists, 201

    def delete(self,list_id):
        lists = List.query.filter_by(list_id = list_id).first()
        if lists:
            db.session.delete(lists)
            db.session.commit()
            return "List successsfully deleted", 200
        else:
            abort(404, message = "List doesn't exist")


api.add_resource(Lists, "/user/lists", "/user/lists/<int:user_id>", "/user/lists/delete/<int:list_id>")




#------------------TASK---------------------
task_args = reqparse.RequestParser()
task_args.add_argument("task_title",type=str,required=True)
task_args.add_argument("task_content",type=str)
task_args.add_argument("task_deadline",type=str,required=True)
task_args.add_argument("task_created_time",type=str,required=True)
task_args.add_argument("task_completed_time",type=str)
task_args.add_argument("task_status",type=str,required=True)
task_args.add_argument("list_id",type=str,required=True)
task_output_fields = {
    'task_id' : fields.Integer,
    'task_title' : fields.String,
    'task_deadline': fields.String
}

class Tasks(Resource):
    @marshal_with(task_output_fields)
    def get(self,list_id):
        tasks = Task.query.filter_by(list_id=list_id).all() # return a list 
        
        if len(tasks) == 0:
            abort(404, message = "Task is not created for this list.")
            
        else:
            return tasks, 200
    
    @marshal_with(task_output_fields)
    def post(self): #add todo
        args = task_args.parse_args()
        tasks = Task(task_title = args['task_title'], task_content = args['task_content'], task_deadline = args['task_deadline'], task_created_time = args['task_created_time'], task_completed_time = args['task_completed_time'], task_status = args['task_status'], list_id = args['list_id'])
        db.session.add(tasks)
        db.session.commit()
        return tasks, 201

    def delete(self,task_id):
        tasks = Task.query.filter_by(task_id=task_id).first()
        if tasks:
            db.session.delete(tasks)
            db.commit()
            return "Task successsfully deleted", 200
        else:
            abort(404, message = "Task doesn't exist")
        

api.add_resource(Tasks, "/user/lists/tasks/", "/user/lists/tasks/<int:list_id>", "/user/lists/tasks/<int:task_id>")