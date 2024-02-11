from flask import Flask, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy, inspect
import os

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

def start_student_db(db_conn = db_extend):
    # Check if table exists
    # Reference: https://copyprogramming.com/howto/easily-check-if-table-exists-with-python-sqlalchemy-on-an-sql-database#flask-sqlalchemy-check-if-table-exists-in-database
    # Check solution 3 for Flask-SQLAlchemy
    db_inspector = inspector(db_conn)
    # Checking if Users table already exists
    user_table_bool = db_inspector.has_table("users")
    if user_table_bool == False:
        exit()
        # Create the Users table
    else:
        # propogate the Users within the table

class Users(db_conn.Model):
    banner_id = db_conn.Column(db_conn.Integer, primary_key = True)
    username = db.Column(db.String, unique = TRUE, nullable = False)
    email = db.Column(db.String)
    status = db.Column(db.String)

# Start up database extension
db_extend = SQLAlchemy()
# Get path for database
db_path = initiate_db_path()
# Initial configuration of database
app.config["SQLALCHEMY_DATABASE_URI"] = db_path
# Initiate application with database
db_extend.init_app(app)



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