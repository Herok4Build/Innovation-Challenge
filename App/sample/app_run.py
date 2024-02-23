from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        if request.form["sb"] == "loginBtn":
            return render_template("app.html")
        elif request.form["sb"] == "newuser":
            return render_template("home.html")
        # email_var = request.form.get("useremail")
        # pass_var = request.form.get("userpass")
        # # Do something with email_var and pass_var (e.g., authenticate user)
        # return f"Email: {email_var}, Password: {pass_var}"
        
    else:
        return "Method Not Allowed"

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        if request.form["sb"] == "newuser":
            return render_template("home.html")
        # email_var = request.form.get("useremail")
        # pass_var = request.form.get("userpass")
        # # Do something with email_var and pass_var (e.g., authenticate user)
        # return f"Email: {email_var}, Password: {pass_var}"
        
    else:
        return "Method Not Allowed"

if __name__ == '__main__':
    app.run(debug=True)
