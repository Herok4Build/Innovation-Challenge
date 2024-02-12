from flask import Flask, request
from flask import render_template
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MetaData
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
import os

from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)
metadat = MetaData()

db_sess = scoped_session(sessionmaker(autocommit = False,autoflush = False, bind = engine))

class Base(DeclarativeBase):
    pass


#db_extend = SQLAlchemy(model_class=Base)

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
# db_path = initiate_db_path()
# Initial configuration of database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///guide.db"
# Initiate application with database

# db_extend.init_app(app)


def start_student_db(db_conn,app):
    with app.app_context():
        # propogate the Users within the table
        user_1 = Users(banner_id = 123245321, username = "CassJ", fname = "Cassandra", lname = "Lauryn",
         email = "cassandra@aggies.ncet.edu", status = "student")
        user_2 = Users(banner_id = 123245323, username = "JamesK", fname = "Jameson", lname = "Kart",
         email = "jkart@aggies.ncat.edu", status = "student")
        db_conn.session.add(user_1)
        db_conn.session.add(user_2)
        db_conn.session.commit()

# Reference:https://stackoverflow.com/questions/24475645/sqlalchemy-one-to-one-relation-primary-as-foreign-key
# Reference: https://docs.sqlalchemy.org/en/20/orm/quickstart.html (02-12-2024)
class Users(db_extend.Model):
    # Banner ID
    banner_id: Mapped[int] = mapped_column(primary_key=True)
    # Username
    username:  Mapped[str] = mapped_column(String(40))
    # firstname
    fname: Mapped[str] = mapped_column(String(40))
    # Last name
    lname: Mapped[str] = mapped_column(String(40))
    # Email
    email: Mapped[str] = mapped_column(String(80))
    # Status
    status: Mapped[str] = mapped_column(String(20))
    # Student data
    student_info: Mapped[List["Student"]] = relationship(back_populates="user", cascade="all, delete-orphan")
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
    def __repr__(self) -> str:
        return f"Users({banner_id = {self.id!r}, fname =self.fname!r})"

class Students(db_extend.Model):
    banner_id: Mapped[int] = mapped_column(ForeignKey("users.banner_id"),
    primary_key = True)
    # firstname
    fname = Mapped[str]: mapped_column(String(40))
    # Last name
    lname = Mapped[str]: mapped_column(String(40))
    # Course/Program
    course = Mapped[str]: mapped_column(String(40))
    # Department
    department = Mapped[str]: mapped_column(String(40))
    # Advisor's name
    advisorname = Mapped[str]: mapped_column(String(90))
    
    def __repr__(self) -> str:
        return f"Students({banner_id = {self.id!r}, fname =self.fname!r})"

class advisorChair(db_extend.Model):
    banner_id = : Mapped[int] = mapped_column(ForeignKey("users.banner_id"),
    primary_key = True)
    # firstname
    fname = Mapped[str]: mapped_column(String(40))
    # Last name
    lname = Mapped[str]: mapped_column(String(40))
    # Department area Concentration
    depart_concen = Mapped[str]: mapped_column(String(40))
    
    def __repr__(self) -> str:
        return f"advisorChair({banner_id = {self.id!r}, fname =self.fname!r})"


start_student_db(db_conn = db_extend, app = app)


@app.route("/")
def home():
    # Render the home.html page for people to access
    # Currently the first page they land on
    return render_template("home.html")

@app.route("/registered", methods = ["POST"])
def register_user():
    # To register the users
    pass

@app.route("/checkdb1")
def checkdb1():
    return(Users.query.all())

@app.route("/login", methods = ["POST"])
# Login function
# Need to finish register function first before 
# continuoing with login function
def login():
    email_var = request.form["useremail"]
    pass_var = request.form["userpass"]
    return email_var, pass_var