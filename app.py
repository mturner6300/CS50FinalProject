from flask import Flask, flash, redirect, render_template, request, session
from helpers import login_required
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

import sqlite3
connection = sqlite3.connect("coursedatabase.db")
db = connection.cursor()

@app.route('/')
def index():
    home = "currentpage"
    return render_template("index.html", home=home)

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/about", methods=(["GET","POST"]))
def about():
    about = "currentpage"
    return render_template("about.html", about=about)

@app.route("/explore", methods=(["GET","POST"]))
@login_required
def explore():
    explore = "currentpage"
    return render_template("explore.html", explore=explore)

@app.route("/tracks", methods=(["GET","POST"]))
@login_required
def tracks():
    tracks = "currentpage"
    return render_template("tracks.html", tracks=tracks)

@app.route("/myaccount", methods=(["GET","POST"]))
@login_required
def myaccount():
    myaccount = "currentpage"
    return render_template("myaccount.html", myaccount=myaccount)

@app.route("/contactus", methods=(["GET","POST"]))
def contactus():
    contactus = "currentpage"
    return render_template("contactus.html", contactus=contactus)

@app.route("/search", methods=(["GET","POST"]))
def search():
    """ Get accesses the in-depth search page with GET"""
    """ Search Courses with POST from any page """
    advancesearch = "currentpage"
    if request.method == "GET":
        return render_template("search.html", advancesearch=advancesearch)
    else:
        querystring = request.form.get("q")
        if not querystring:
            return render_template("search.html", querystring="nothing", advancesearch=advancesearch)
        else:
            results = db.execute("SELECT * FROM courses WHERE name CONTAINS ?", querystring)
            if not results:
                return render_template("search.html", querystring=querystring, advancesearch=advancesearch)
            else:
                return render_template("results.html", querystring=querystring, advancesearch=advancesearch, results=results)
        

    
        
        

    