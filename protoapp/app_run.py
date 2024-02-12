from flask import Flask, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
import os



class Base(DeclarativeBase):
    pass

class Base(DeclarativeBase):
      pass

db_extend = SQLAlchemy(model_class=Base)

# Activate Flask app
app = Flask(__name__)
# Extending code from Quickstart guide
# Reference: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/

def initiate_db_path(path = None):
    # Set up path for database
    if path == None:
        path = "./db/"
        if os.path.isdir(path) == False:
            os.mkdir(path)
    path = path + "sqlite:///guide.db"


# Start up database extension
#db_extend = SQLAlchemy()
# Get path for database
db_path = initiate_db_path()
# Initial configuration of database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///guide.db"
# Initiate application with database

db_extend.init_app(app)


def start_student_db(db_conn):
    # propogate the Users within the table
    user_1 = Users(banner_id = 123245321, username = "CassJ", fname = "Cassandra", lname = "Lauryn",
    email = "cassandra@aggies.ncet.edu", status = "student")
    user_3 = Users(banner_id = 123245323, username = "JamesK", fname = "Jameson", lname = "Kart",
     email = "jkart@aggies.ncat.edu", status = "student")


class Users(db_extend.Model):
    # Banner ID
    banner_id = db_extend.Column(db_extend.Integer, 
    primary_key = True)
    # Username
    username = db_extend.Column(db_extend.String, unique = True, nullable = False)
    # firstname
    fname = db_extend.Column(db_extend.String)
    # Last name
    lname = db_extend.Column(db_extend.String)
    # Email
    email = db_extend.Column(db_extend.String)
    # Status
    status = db_extend.Column(db_extend.String)
    # Student data
    student_info = db_extend.relationship("Students", backref = "Users",
    uselist = False)
    '''
    # Start here for separating student table
    # Course/Program
    course = db_extend.Column(db_extend.String)
    # Department
    department = db_extend.Column(db_extend.String)
    # Advisor's name
    advisorname = db_extend.Column(db_extend.String)
    # End separate for student table
    # Start here fro separating department chair and advisor table
    # Department area Concentration
    depart_concen = db_extend.Column(db_extend.String)
    '''

class Students(db_extend.Model):
    banner_id = db_extend.Column(db_extend.Integer, db_extend.ForeignKey("users.banner_id"),
    primary_key = True)
    db_extend.relationship("Users")
    # firstname
    fname = db_extend.Column(db_extend.String)
    # Last name
    lname = db_extend.Column(db_extend.String)
    # Course/Program
    course = db_extend.Column(db_extend.String)
    # Department
    department = db_extend.Column(db_extend.String)
    # Advisor's name
    advisorname = db_extend.Column(db_extend.String)

class advisorChair(db_extend.Model):
    banner_id = db_extend.Column(db_extend.Integer,
                                primary_key = True)
    # firstname
    fname = db_extend.Column(db_extend.String)
    # Last name
    lname = db_extend.Column(db_extend.String)
    # Department area Concentration
    depart_concen = db_extend.Column(db_extend.String)

with app.app_context():
    db_extend.create_all()

start_student_db(db_conn = db_extend)


@app.route("/")
def home():
    # Render the home.html page for people to access
    # Currently the first page they land on
    return render_template("home.html")

@app.route("/login", methods = ["POST"])
# Login function
# Need to finish register function first before 
# continuoing with login function
def login():
    email_var = request.form["useremail"]
    pass_var = request.form["userpass"]
    return email_var, pass_var