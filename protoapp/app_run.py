from flask import Flask, request, session
from flask import render_template
from flask import Response
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import MetaData
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import os
from matplotlib.figure import Figure
import numpy as np
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import base64
from PIL import Image

from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)
metadat = MetaData()

db_sess = scoped_session(sessionmaker(autocommit = False,autoflush = False, bind = engine))

def total_credits(prev_status = "MS"):
    if prev_status == "MS":
        return(42)
    else:
        return(65)

def total_milestones(prev_status = "MS"):
    if prev_status == "MS":
        return(10)
    else:
        return(12)

# Reference: https://buraksenol.medium.com/pass-images-to-html-without-saving-them-as-files-using-python-flask-b055f29908a
# Author: Burak Senol
# Reference: https://www.geeksforgeeks.org/donut-chart-using-matplotlib-in-python/
# Author: srivastava
# Reference: https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html

# Function based off of Matplotlib documentation to label the values of the donut chart
def percent_disp(pct, values):
    actual = int(np.round(pct/100.*np.sum(values)))
    return f"{pct:.1f}%\n({actual:d})"

# Function to draw donut chart for the number of credits
# completed_cred is for the number of completed credits
# total_credits is the total credits necessary for graduation
def create_credit_chart(completed_cred = 0, total_credits = 42):
    # Get the number of remaining credits
    remaining_credits = total_credits - completed_cred
    # List containing the info on the credits
    credits_data = [completed_cred, remaining_credits]
    # colors for the portions of the chart
    chart_colors = ["#0000FF", "#808080"]
    # Create the figure
    credit_fig = Figure()
    # Establish the subplot
    axis = credit_fig.add_subplot(1,1,1)
    # Set the title
    axis.set_title("My Progress")
    # Adjust to accomodate the legend
    credit_fig.subplots_adjust(right=0.6)
    # Include the data and establish labels
    wedge_elem, text_elem, autotexts = axis.pie(x = credits_data, colors = chart_colors, autopct = lambda pct: percent_disp(pct,credits_data))
    # Draw a circle to make a donut
    axis.pie(x = [100], colors = ["white"], radius =0.80)
    # Establish the legend for the plot
    axis.legend(wedge_elem, ["completed", "remaining"], title="Credits",loc = "center left", bbox_to_anchor = (1,0,0.5,1))
    # Store to memory and save to get around saving as a file
    outputted_info = io.BytesIO()
    credit_fig.savefig(outputted_info,format="png")
    encoded_chart = base64.b64encode(outputted_info.getvalue())
    decode_chart = encoded_chart.decode("utf-8")
    # return the necessary encoded information
    return(decode_chart)


# Based on the create_credit_chart() function
# Uses milestones to calculate the completion progress.
def create_completion_chart(completed_miles = 0, total_miles = 10):
    # Calculate the remaining milestones
    remaining_miles = total_miles - completed_miles
    # Put milestones data into a list
    miles_data = [completed_miles, remaining_miles]
    chart_colors = ["#0000FF", "#808080"]
    credit_fig = Figure()
    axis = credit_fig.add_subplot(1,1,1)
    credit_fig.subplots_adjust(right=0.6)
    wedge_elem, text_elem = axis.pie(x = credits_data,autopct = lambda pct: percent_disp(pct,miles_data), colors = chart_colors, title="My Completion")
    axis.pie(x = [100], colors = ["white"], radius =0.80)
    axis.legend(wedge_elem, ["completed", "remaining"], title="Credits",loc = "center left", bbox_to_anchor = (1,0,0.5,1))
    outputted_info = io.BytesIO()
    credit_fig.savefig(outputted_info,format="png")
    encoded_chart = base64.b64encode(outputted_info.getvalue())
    decode_chart = encoded_chart.decode("utf-8")
    return(decode_chart)

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


def start_student_db(db_conn):
    with Session(db_conn) as session:
        # propogate the Users within the table
        user_1 = Users(banner_id = 123245321, username = "CassJ", fname = "Cassandra", lname = "Lauryn",
         email = "cassandra@aggies.ncet.edu", status = "student")
        user_2 = Users(banner_id = 123245323, username = "JamesK", fname = "Jameson", lname = "Kart",
         email = "jkart@aggies.ncat.edu", status = "student")
        session.add_all([user_1, user_2])
        session.commit()
        session.delete(user_1)
        session.commit()


# Reference:https://stackoverflow.com/questions/24475645/sqlalchemy-one-to-one-relation-primary-as-foreign-key
# Reference: https://docs.sqlalchemy.org/en/20/orm/quickstart.html (02-12-2024)
class Users(Base):
    __tablename__ = "Users"
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
    student_info: Mapped["Students"] = relationship(back_populates="user_info", cascade="all, delete-orphan")
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
        return f"Users(banner_id = {self.id!r}, fname ={self.fname!r})"

class Students(Base):
    __tablename__ = "Students"
    banner_id: Mapped[int] = mapped_column(ForeignKey("Users.banner_id"),
    primary_key = True)

    user_info: Mapped["Users"] = relationship(back_populates="student_info")
    # firstname
    fname: Mapped[str]= mapped_column(String(40))
    # Last name
    lname: Mapped[str]= mapped_column(String(40))
    # Course/Program
    course: Mapped[str]= mapped_column(String(40))
    # Department
    department: Mapped[str]= mapped_column(String(40))
    # Advisor's name
    advisorname: Mapped[str]= mapped_column(String(90))
    
    def __repr__(self) -> str:
        return f"Students(banner_id = {self.id!r}, fname ={self.fname!r})"
"""
class advisorChair(Base):
    __tablename__ = "advisorChair"
    banner_id: Mapped[int] = mapped_column(ForeignKey("users.banner_id"),
    primary_key = True)
    # firstname
    fname: Mapped[str]= mapped_column(String(40))
    # Last name
    lname: Mapped[str]= mapped_column(String(40))
    # Department area Concentration
    depart_concen: Mapped[str]= mapped_column(String(40))
    
    def __repr__(self) -> str:
        return f"advisorChair(banner_id = {self.id!r}, fname ={self.fname!r})"
"""

Base.metadata.create_all(bind = engine)

start_student_db(db_conn = engine)


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

# Reference: https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
# Author: Messa
@app.route("/student-dash")
def dashboard():
    if session is not None and "banner_id" in session:
        student_id = session["banner_id"]
        # Get some information form the database
    else:
        student_id = None
        credits_figure = create_credit_chart()
        milestones_figure = create_completion_chart()
        # FigureCanvas(credits_figure).print_png(outputted_info)
        #credits_chart = Response(outputted_info.getvalue(), mimetype = "image/png")

    return render_template("student-dashboard.html", credits_plot =credits_figure, milestones_plot = milestones_figure)
    

@app.route("/existing-user")
def user_exists():
    return render_template("existing-users.html")



