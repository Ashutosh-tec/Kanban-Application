from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from models import db, User as User, List as List, Task as Task
from flask_security import auth_required, current_user, hash_password
from security import user_datastore, sec
import datetime
from flask import send_file

from flask import jsonify

# import sys
# # setting path
# sys.path.append('../')
# from app import cache


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
    # @auth_required('token')
    def get(self,user_email=None):
        usr = User.query.filter_by(email=user_email).first()
        
        if usr: # and usr.email == current_user.email:
            return usr, 200
            # This returned object will have proper credential only if user autherised --> check ../backend/views/login.vue -> res2 in loginMethod
        else:
            abort(404, message="Invalid Email address")

    # @marshal_with(user_output_fields)
    def post(self): 
        args = user_args.parse_args()
        print(args)
        if user_datastore.find_user(email=args['email']):
            abort(409, message = "Email already exist, please login.")

        user_datastore.create_user(
        username=args['username'], email=args['email'], password=hash_password(args['password']))
        db.session.commit()
        return {"User Name" : args['username']}, 201
    @auth_required('token')
    def delete(self,user_id):
        usr = User.query.filter_by(id=user_id).first()
        if usr:

            lst=List.query.filter_by(user_id = user_id).all()
            for lt in lst:
                tsk = Task.query.filter_by(list_id = lt.list_id).all()
                for tk in tsk:
                    db.session.delete(tk)
                    db.session.commit()
                db.session.delete(lt)
                db.session.commit()



            db.session.delete(usr)
            db.session.commit()
            return "User successsfully deleted", 200
        else:
            abort(404, message = "User doesn't exist")


api.add_resource(Users, "/adduser", "/user/<string:user_email>", "/user/<int:user_id>")


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
    # @cache.memoize(timeout=60)
    def get(self,id):
        lists = List.query.filter_by(user_id=id).all() # return a list 
        
        if id != current_user.id:
            
            abort(404, message = "No lists availavle or you have put some wrong credentials.")
            
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
            if args.list_id != "":
                task.list_id = args.list_id
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
    @auth_required('token')
    def get(self,img_id,user_id):
        from matplotlib import pyplot as plt
        import numpy as np
        # will work simply by <img src="http://127.0.0.1:5000/api/summary_images/1/1"/>
        var = List.query.filter_by(user_id=user_id)
        task = []
        for lt in var:
            task += Task.query.filter_by(list_id=lt.list_id)
        if img_id == 1:
            
            var = {"Completed": [], "Pending": [], "passdead": []} #storing info of task in this month
            for tsk in task:
               
                if tsk.task_status == "Completed":
                    var['Completed'].append(tsk) 
                elif tsk.task_deadline < date_object:
                        var['passdead'].append(tsk)
                elif tsk.task_status != "Completed":
                    var['Pending'].append(tsk)
                           
           
            task_no=[len(var["Completed"]),len(var["Pending"]),len(var["passdead"])]
            
            if task_no == []:
                return "No task to show", 404
            return jsonify(task_no)
            


        elif img_id == 2:
            
            var = {"Completed": [], "Created": [], "passdead": []} #storing info of task in this month
            for tsk in task:
                
                if str(tsk.task_created_time)[5:7] == date_object[5:7]:
                    var['Created'].append(tsk)
                if tsk.task_status == "Completed":
                    if str(tsk.task_completed_time)[5:7] == date_object[5:7]:
                        var['Completed'].append(tsk)
                else:
                    if tsk.task_deadline < date_object:
                        var['passdead'].append(tsk)
            
            plt.clf() #used to clear the current figure
            var['Completed'].sort(key = lambda x : x.task_completed_time)
            
            complete_taskNo_dict = {}
            for tsk in var['Completed']:
                complete_taskNo_dict[tsk.task_completed_time] = 0
            for tsk in var['Created']:
                complete_taskNo_dict[tsk.task_created_time] = 0

            create_taskNo_dict = complete_taskNo_dict.copy()
            for tsk in var['Completed']:
                complete_taskNo_dict[tsk.task_completed_time] += 1
            for tsk in var['Created']:
                create_taskNo_dict[tsk.task_created_time] += 1
            print(complete_taskNo_dict, create_taskNo_dict)
            w = 0.4
            
            dates = list(complete_taskNo_dict.keys())
            dates.sort()
            

            return jsonify(dates, list(create_taskNo_dict.values()), list(complete_taskNo_dict.values()))

        elif img_id == 3:
            var = List.query.filter_by(user_id=user_id)
            tskNoComp = {}
            tskNoPend = {}
            # print(var)
            for lst in var:
                tskNoComp[lst.list_name] = 0
                tskNoPend[lst.list_name] = 0
                tk = Task.query.filter_by(list_id=lst.list_id)
                # print(task)            
                for tsk in tk:
                    if tsk.task_status == 'Completed':
                        tskNoComp[lst.list_name] += 1
                    else:
                        tskNoPend[lst.list_name] += 1
            return jsonify(list(tskNoPend.keys()), list(tskNoPend.values()), list(tskNoComp.values()))
                



api.add_resource(summary, "/summary_images/<int:img_id>/<int:user_id>")