from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from models import db, User as User, List as List, Task as Task
from flask_security import auth_required, current_user, hash_password
from security import user_datastore, sec
import datetime
from flask import send_file


api = Api(prefix="/api")

date_object = str(datetime.date.today())

#------------------USER---------------------
user_args = reqparse.RequestParser()
user_args.add_argument("username",type=str,required=True)
user_args.add_argument("email",type=str,required=True)
user_args.add_argument("password",type=str,required=True)
user_output_fields = {
    'id' : fields.Integer,
    'username' : fields.String,
    'email' : fields.String
}

class Users(Resource):
    
    @marshal_with(user_output_fields)
    @auth_required('token')
    def get(self,user_email=None):
        usr = User.query.filter_by(email=user_email).first()
        # if id==current_user.id:
        if usr and user_email==current_user.email:
            return usr, 200
            # This returned object will have proper credential only if user autherised --> check ../backend/views/login.vue -> res2 in loginMethod
        else:
            abort(404, message="Invalid Email address")

    # @marshal_with(user_output_fields)
    def post(self): #add list
        args = user_args.parse_args()
        if user_datastore.find_user(email=args['email']):
            abort(409, message = "Email already exist, please login.")

        user_datastore.create_user(
        username=args['username'], email=args['email'], password=hash_password(args['password']))
        db.session.commit()
        return {"User Name" : args['username']}, 201
    
    def delete(self,user_id):
        usr = User.query.filter_by(id=user_id).first()
        if usr:
            db.session.delete(usr)
            db.session.commit()
            return "User successsfully deleted", 200
        else:
            abort(404, message = "User doesn't exist")


api.add_resource(Users, "/user/", "/user/<string:user_email>", "/user/<int:user_id>")


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

list_put_args = reqparse.RequestParser()
list_put_args.add_argument("list_name",type=str)
list_put_args.add_argument("list_description",type=str)
list_put_args.add_argument("user_id",type=int,required=True)

class Lists(Resource):
    @marshal_with(list_output_fields)
    @auth_required('token')
    def get(self,id):
        lists = List.query.filter_by(user_id=id).all() # return a list 
        # return lists, 201
        
        if len(lists) == 0 or id != current_user.id:
            # return lists, 201
            abort(404, message = "No lists availavle or you have put some wrong credentials.")
            # return "List is not created yet.", 404
        else:
            return lists, 200

    @marshal_with(list_output_fields)
    @auth_required('token')
    def post(self): #add list
        args = list_args.parse_args()
        lists = List(list_name = args['list_name'], list_description = args['list_description'], user_id = args['user_id'])
        if lists.list_description == "":
            lists.list_description = None 
        db.session.add(lists)
        db.session.commit()
        return lists, 201

    @auth_required('token')
    def delete(self,id):
        list = List.query.filter_by(list_id = id).first()
        if list:
            task = Task.query.filter_by(list_id=id).all()
            for tsk in task:
                db.session.delete(tsk)
                db.session.commit()
            db.session.delete(list)
            db.session.commit()
            return "List successsfully deleted", 200
        else:
            abort(404, message = "List doesn't exist")
    
    @auth_required('token')
    def put(self, id):
        args = list_put_args.parse_args()
        list = List.query.filter_by(list_id = id).first()
        if list:
            list.list_name = args["list_name"]
            if args["list_description"] != list.list_description:
                list.list_description = args["list_description"]
                if args["list_description"] == "":
                    list.list_description = None
            db.session.commit()
            return "List successsfully updated", 200
        else:
            abort(404, message = "List doesn't exist")


api.add_resource(Lists, "/user/add_list", "/user/lists/<int:id>")#, "/user/lists/delete/<int:list_id>")




#------------------TASK---------------------
task_args = reqparse.RequestParser()
task_args.add_argument("task_title",type=str,required=True)
task_args.add_argument("task_content",type=str,required=True)
task_args.add_argument("task_deadline",type=str,required=True)
task_args.add_argument("task_created_time",type=str,required=True)
task_args.add_argument("task_completed_time",type=str)
task_args.add_argument("task_status",type=str,required=True)
task_args.add_argument("list_id",type=int,required=True)
task_output_fields = {
    'task_id' : fields.Integer,
    'task_title' : fields.String,
    'task_content' : fields.String,
    'task_deadline': fields.String,
    'task_created_time' : fields.String,
    'task_completed_time' : fields.String,
    'task_status' : fields.String,
    'list_id' : fields.String
}

class Tasks(Resource):
    @marshal_with(task_output_fields)
    @auth_required('token')
    def get(self,id):
        task = Task.query.filter_by(list_id=id).all() # return a list 
        # if len(tasks) == 0:
        #     abort(404, message = "Task is not created for this list.")
            
        # else:
        return task, 200
    
    @marshal_with(task_output_fields)
    @auth_required('token')
    def post(self): #add todo
        args = task_args.parse_args()
        tasks = Task(task_title = args['task_title'], task_content = args['task_content'], task_deadline = args['task_deadline'], task_created_time = args['task_created_time'], task_completed_time = args['task_completed_time'], task_status = args['task_status'], list_id = args['list_id'])
        if tasks.task_content == "":
            tasks.task_content = None
        if tasks.task_completed_time == "":
            tasks.task_completed_time = None
        db.session.add(tasks)
        db.session.commit()
        return tasks, 201

    @auth_required('token')
    def delete(self,id):
        task = Task.query.filter_by(task_id=id).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return "Task successsfully deleted", 200
        else:
            abort(404, message = "Task doesn't exist")
    
    @auth_required('token')
    def put(self,id):
        args = task_args.parse_args()
        task = Task.query.filter_by(task_id=id).first()
        if task:
            if args.task_title != task.task_title:
                task.task_title = args.task_title
            if args.task_content != task.task_content:
                task.task_content = args.task_content
            if args.task_deadline != task.task_deadline:
                task.task_deadline = args.task_deadline
            if args.task_status != task.task_status:
                if args.task_status == 'Pending':
                    task.task_completed_time = None
                if args.task_status == 'Completed':
                    task.task_completed_time = date_object
                task.task_status = args.task_status
            if task.task_content == "":
                task.task_content = None
            db.session.commit()
            return "Task successsfully updated", 200
        else:
            abort(404, message = "Task doesn't exist")

api.add_resource(Tasks, "/user/lists/task", "/user/lists/tasks/<int:id>")


class export_lst(Resource):
    # @auth_required('token')
    def get(self, lst_id):
        try:
            lst = List.query.filter_by(list_id=lst_id).first()
            file = open(f"./Export_files/list_{lst_id}.csv", "w")
            file.write(f"{lst.list_id}, {lst.list_name}, {lst.list_description}\n\n")
            tsk = Task.query.filter_by(list_id=lst_id).all()
            for tk in tsk:
                file.write(f"{tk.task_id}, {tk.task_title}, {tk.task_content}, {tk.task_deadline}, {tk.task_created_time}, {tk.task_completed_time}, {tk.task_status}\n")
            file.close()
            return send_file(f"./Export_files/list_{lst_id}.csv")#, attachment_filename='doc.html')
        except Exception as e:
            return str(e)
api.add_resource(export_lst, "/download/list/<int:lst_id>")


class export_tsk(Resource):
    # @auth_required('token')
    def get(self, tsk_id):
        try:
            tk = Task.query.filter_by(task_id=tsk_id).first()
            file = open(f"./Export_files/task_{tsk_id}.csv", "w")
            file.write(f"{tk.task_id}, {tk.task_title}, {tk.task_content}, {tk.task_deadline}, {tk.task_created_time}, {tk.task_completed_time}, {tk.task_status}\n")
            file.close()
            return send_file(f"./Export_files/task_{tsk_id}.csv")#, attachment_filename='doc.html')
        except Exception as e:
            return str(e)
api.add_resource(export_tsk, "/download/task/<int:tsk_id>")



class summary(Resource):
    def get(self,img_id,user_id):
        # will work simply by <img src="http://127.0.0.1:5000/api/summary_images/1/1"/>
        if img_id == 1:
            return send_file("./static/summaryTask.png")
        elif img_id == 2:
            return send_file("./static/sign-add-icon.jpeg")
api.add_resource(summary, "/summary_images/<int:img_id>/<int:user_id>")