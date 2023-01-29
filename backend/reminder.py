"""
    This file contain functions used in celery_system.py to give user reminder.
"""

import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from models import db, User as User, List as List, Task as Task
import datetime
import matplotlib.pyplot as plt
import numpy as np

env = Environment(loader=FileSystemLoader('templates'))
date_object = str(datetime.date.today())


class trigger_reminder():

    def email_sender(user):
        msg = EmailMessage()
        msg['Subject'] = 'Kanban Monthly Activity Report'
        msg['From'] = 'Monthly Report'
        msg['To'] = str(user.email)
        msg.set_content(f"Hello {user.username},\n We hope you are doing well. Your monthly report is attatched in this mail.\n\nThanks and regards,\nKanboard Application Team")
        trigger_reminder.report_maker(user)
        with open("./Export_files/html_reportPDF.pdf", "rb") as f:
            file_data = f.read()
            file_name = f"{user.username}-MonthlyReport.pdf"
            msg.add_attachment(file_data,
                               maintype="application",
                               subtype="pdf",
                               filename=file_name)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("testingkanbanapp@gmail.com", "zxnmkprvlfkaojby")
        server.send_message(msg)
        server.quit()
        return "Email sent"

    def report_maker(user):
        var = List.query.filter_by(user_id=user.id)
        task = []
        for lt in var:
            task += Task.query.filter_by(list_id=lt.list_id)
        var = {"Completed": [], "Pending": [], "passdead": []}
        for tsk in task:
            if tsk.task_status == "Completed":
                if str(tsk.task_completed_time)[5:7] == date_object[5:7]:
                    var['Completed'].append(tsk)
            else:
                if tsk.task_deadline < date_object:
                    var['passdead'].append(tsk)
                else:
                    var['Pending'].append(tsk)
        
        trigger_reminder.summary_img(user)
        template = env.get_template('report_template.html')
        image_name = "../static/summaryTask" +".png"
        html = template.render(user=user.username,
                               completed_task=len(var['Completed']),
                               pending_task_len=len(var['Pending']),
                               pending_task=var['Pending'],
                               dead_task_len=len(var['passdead']),
                               dead_task=var['passdead'],
                               image_name=image_name)
        with open('./Export_files/html_report.html', 'w') as f:
            f.write(html)
        from weasyprint import HTML
        HTML('./Export_files/html_report.html').write_pdf('./Export_files/html_reportPDF.pdf')
    
    def summary_img(user):
        var = List.query.filter_by(user_id=user.id)
        task = []
        for lt in var:
            task += Task.query.filter_by(list_id=lt.list_id)
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
                

        # making graph of Task Completing Time vs Date
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
        print(complete_taskNo_dict)
        w = 0.4
        bar1 = np.arange(len(complete_taskNo_dict.keys()))
        bar2 = [i+w for i in bar1]
        plt.bar(bar1, list(create_taskNo_dict.values()),w, label='Created', color = ['brown'])
        plt.bar(bar2, list(complete_taskNo_dict.values()),w, label='Completed', color = ['green'])
        plt.xlabel('Date')
        plt.ylabel('No. of Tasks')
        plt.title('Date (Activity Time) Vs No. of Tasks')
        plt.xticks(bar1+w/2, complete_taskNo_dict.keys())
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.savefig("static/summaryTask" +".png")
        


    def user_task():
        """
        This function will return a dictionary.
        Key - > user_id
        value -> list -> 0th element User Name, rest task id having status not completed or "Pending"
        """
        user = User.query.all()
        lst = List.query.all()
        task = Task.query.all()
        user_lst_dict = {}
        lst_task_dict = {}
        user_task_dict = {}
        for usr in user:
            user_lst_dict[usr.id] = []
            user_task_dict[usr.id] = [usr.username]

        for lt in lst:
            lst_task_dict[lt.list_id] = []
            user_lst_dict[int(lt.user_id)].append(int(lt.list_id))
        for tsk in task:
            if tsk.task_status != "Completed":
                lst_task_dict[int(tsk.list_id)].append(int(tsk.task_id))
        for usr in user_lst_dict:

            for lt in user_lst_dict[usr]:

                user_task_dict[usr] += lst_task_dict[lt]
        return user_task_dict



