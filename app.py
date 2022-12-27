import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import login_required, checkLogin, getData

import json

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

data = []

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():

    if not data:
        populate()   
    
    return render_template("index.html", data=data, a_day=data[0]["Schedule"]["A Day"], b_day=data[0]["Schedule"]["B Day"])

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("login.html")

        name = checkLogin(request.form.get("username"), request.form.get("password"))
        id = request.form.get("username")

        if name=='':
            flash("invalid student id (don't use @sbschools.org) and/or password")    
            return render_template("login.html")

        # # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #     return apology("invalid username and/or password", 403)

        # # Remember which user has logged in
        session["user_id"] = request.form.get("username")+" "+request.form.get("password")

        data.append(json.loads(getData(request.form.get("username"), request.form.get("password"))))

        # # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    data.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/grades", methods=["GET", "POST"])
@login_required
def grades():
    if not data:
        populate() 
    return render_template("grades.html",  mp1=data[0]["Grades"]["MP1"], mp2=data[0]["Grades"]["MP2"], mp3=data[0]["Grades"]["MP3"], mp4=data[0]["Grades"]["MP4"])

@app.route("/assignments", methods=["GET", "POST"])
@login_required
def schedule():
    if not data:
        populate() 
    return render_template("assignments.html", data=data)    

@app.route("/extra", methods=["GET", "POST"])
@login_required
def settings():
    if not data:
        populate() 
    return render_template("extra.html", data=data[0])    

def populate():
    data.clear()

    user = session["user_id"]
    name = user[0:user.find(" ")]
    password = user[user.find(" ")+1:]

    data.append(json.loads(getData(name, password))) 

