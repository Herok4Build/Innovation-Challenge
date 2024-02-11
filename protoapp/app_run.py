from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods = ["POST"])
def login():
    email_var = request.form["useremail"]
    pass_var = request.form["userpass"]
    return email_var, pass_var