# redis-server
# celery -A celery_system.celery worker -l info
# celery -A celery_system.celery beat --max-interval 1 -l info
from celery import Celery
import random
import time
from app import app
from celery.schedules import crontab
from json import dumps
from httplib2 import Http
from models import db, User as User, List as List, Task as Task
from reminder import trigger_reminder

def make_celery(app):
    celery = Celery(
        'app',
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        timezone = 'Asia/Calcutta',
        enable_utc = False
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)



@celery.task()
def send_report():
    user = User.query.all()
    for usr in user:
        trigger_reminder.email_sender(usr)

@celery.task()
def send_reminder():
    user_task_info = trigger_reminder.user_task()
    for itm in user_task_info:
        url = 'https://chat.googleapis.com/v1/spaces/AAAAhPw5wZA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=3yRP4xR36YSmd6EcF4hfnfQ586KWivaPqwpe5Kyzw-Y%3D'
        bot_message = {
            'text': f'Hello {user_task_info[itm][0]}, your {len(user_task_info[itm]) - 1} tasks are pending. Please complete it before deadline'}
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )
        print(response)



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=3, minute=0), send_reminder.s(), name='Daily Alert')
    sender.add_periodic_task(crontab(hour=3, minute=0, day_of_month='15'), send_report.s(), name="Monthly Progress Reports")

