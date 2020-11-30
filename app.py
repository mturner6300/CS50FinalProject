from flask import Flask, flash, redirect, render_template, request, session
from helpers import login_required
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os

app = Flask(__name__)

# Define function to intialise database
def make_cursor(database):
    connection = sqlite3.connect(database)
    return connection.cursor()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    home = "currentpage"
    return render_template("index.html", home=home)

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template("login.html")

""" Combine About and Contact Us?"""
@app.route("/about", methods=(["GET","POST"]))
def about():
    about = "currentpage"
    return render_template("about.html", about=about)

""" Track Search """
@app.route("/tracks", methods=(["GET","POST"]))
@login_required
def tracks():
    tracks = "currentpage"
    return render_template("tracks.html", tracks=tracks)

""" Replace Login with My Account when logged in?"""
@app.route("/myaccount", methods=(["GET","POST"]))
@login_required
def myaccount():
    myaccount = "currentpage"
    return render_template("myaccount.html", myaccount=myaccount)

""" Course Search """
@app.route("/search", methods=(["GET","POST"]))
def search():
    db = make_cursor("coursedatabase.db")
    """ Get accesses the in-depth search page with GET"""
    """ Search Courses with POST from any page """
    search = "currentpage"
    if request.method == "GET":
        return render_template("search.html", search=search)
    else:
        querystring = request.form.get("q")
        if not querystring:
            return render_template("search.html", querystring="nothing", search=search)
        else:
            db.execute("SELECT * FROM courses WHERE INSTR(LOWER(name),LOWER(?))", [querystring])
            results = db.fetchall()
            names = []
            descriptions = []
            codes = []
            for item in results:
                i, name, desc, code = item
                names.append(name)
                descriptions.append(desc)
                codes.append(code)
            
            if not results:
                return render_template("search.html", querystring=querystring, search=search)
            else:
                return render_template("results.html", querystring=querystring, search=search, name=names[0], description=descriptions[0], code=codes[0])
        
""" My Courses """

""" Schedule """

""" My Tracks """
    
        
        

    