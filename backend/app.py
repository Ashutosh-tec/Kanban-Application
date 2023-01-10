from flask import Flask, render_template, send_file 
from models import db, User as User, List as List, Task as Task
from api.resource import api, Users
from flask_cors import CORS
from security import user_datastore, sec
from flask_security import hash_password
from celery_system import *





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


#///////////////



# @app.route("/check")
# def func():
#     from reminder import trigger_reminder
#     from models import db, User as User, List as List, Task as Task
#     user = User.query.filter_by(id = 1).first()
#     trigger_reminder.email_sender(user)
#     return "Hello"
    # env = Environment(loader=FileSystemLoader('templates'))
    # date_object = str(datetime.date.today())   
    # var = List.query.filter_by(user_id=user.id)
    # task = []
    # for lt in var:
    #     task += Task.query.filter_by(list_id=lt.list_id)
    # var = {"Completed": [], "Pending": [], "passdead" : []}
    # for tsk in task:
    #     # if tsk.task_last_update == date_object[5:7]:
    #     if tsk.task_status == "Completed":
    #         if tsk.task_completed_time == date_object[5:7]:
    #             var['Completed'].append(tsk)
    #     else:
    #         if tsk.task_deadline < date_object:
    #             var['passdead'].append(tsk)
    #         else:
    #             var['Pending'].append(tsk)

    # template = env.get_template('report_template.html')
    # html = template.render(user=user.username, completed_task=len(var['Completed']), pending_task_len=len(var['Pending']), pending_task=var['Pending'], dead_task=var['passdead'])
    # with open('./Export_files/html_report.html', 'w') as f:
    #     f.write(html)

#     user = User.query.all()
#     lst = List.query.all()
#     task = Task.query.all()
#     user_lst_dict = {}
#     lst_task_dict = {}
#     user_task_dict = {}
#     for usr in user:
#         user_lst_dict[usr.id] = []
#         user_task_dict[usr.id] = [usr.username]

#     for lt in lst:
#         lst_task_dict[lt.list_id] = []
#         # print(lt.user_id, lt.list_id, "djshnfkjsd")
#         user_lst_dict[int(lt.user_id)].append(int(lt.list_id))
#     for tsk in task:
#         if tsk.task_status != "Completed":
#             print(tsk.list_id)
#             lst_task_dict[int(tsk.list_id)].append(int(tsk.task_id))
#             print(lst_task_dict)
#     for usr in user_lst_dict:
       
#         for lt in user_lst_dict[usr]:
            
#             print(lt)
#             print(user_task_dict[usr], lst_task_dict[lt])
#             user_task_dict[usr] += lst_task_dict[lt]
#     return user_task_dict
#///////////////

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


#<----- EXPORT ROUTES ------->


@app.route('/download/task/<tsk_id>')
def TSK(tsk_id):
    try:
        tk = Task.query.filter_by(task_id=tsk_id).first()
        file = open(f"./Export_files/task_{tsk_id}.csv", "w")
        file.write(f"{tk.task_id}, {tk.task_title}, {tk.task_content}, {tk.task_deadline}, {tk.task_created_time}, {tk.task_completed_time}, {tk.task_status}\n")
        file.close()
        return send_file(f"./Export_files/task_{tsk_id}.csv")#, attachment_filename='doc.html')
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
