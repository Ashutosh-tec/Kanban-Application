from flask import Flask, render_template 
from models import db, User as User, List as List, Todo as Todo



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# @app.before_first_request
# def create_db():
    # db.create_all()
    # usr= User(user_id="001", user_password="001")
    # db.session.add(usr)
    # db.session.commit()
    # lst = List(list_id="001",list_name="1st",list_description="Blah", user_id="001")
    # db.session.add(lst)
    # db.session.commit()

@app.route('/')
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run()
