from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from helpers import login_required, make_cursor
from flask_session import Session
from flask_paginate import Pagination, get_page_parameter
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define function to intialise database
def make_cursor(database):
    connection = sqlite3.connect(database)
    return connection, connection.cursor()

# Global constant to limit search results to 25 per page
perpage = 25


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
    # Forget any user ids
    session.clear()
    # Enter database
    conn, db = make_cursor("coursedatabase.db")

    login = "currentpage"
    # Post is submission
    if request.method == "POST":
        # Ensure username and password were submitted
        if not request.form.get("username"):
            return render_template("login.html", message="You must enter your username", login=login)
        elif not request.form.get("password"):
            return render_template("login.html", message="You must enter your password", login=login)
        
        # Check for correct username and password
        db.execute("SELECT id, hashedpass FROM users WHERE username=?", [request.form.get("username")])
        rows = db.fetchall()
        if len(rows) != 1:
            return render_template("login.html", message="Username does not exist", login=login)
        
        user_id, hashed_pass = rows[0]
        if not check_password_hash(hashed_pass,request.form.get("password")):
            return render_template("login.html", message="Wrong password", login=login)
        

        # Store username and return to home
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("login.html", login=login)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn, db = make_cursor("coursedatabase.db")
        db.execute("SELECT * FROM security")
        questions = db.fetchall()

        # Collect info from form
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_password")
        email = request.form.get("email")
        security_id = request.form.get("security_question")
        security_answer = request.form.get("security_answer")
        confirm_answer = request.form.get("confirm_answer")

        if not username or not password or not confirm_pass or not email or not security_id or not security_answer or not confirm_answer:
            error = "Please fill in all fields!"
            return render_template("register.html", error=error, questions=questions)
        elif password != confirm_pass:
            #return passwords don't match error
            error = "Passwords do not match!"
            return render_template("register.html", error=error,questions=questions)
        elif security_answer != confirm_answer:
            #return security answers don't match error
            error = "Security answers do not match!"
            return render_template("register.html", error=error,questions=questions)
        elif len(db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")]).fetchall()) != 0:
            #return username taken error
            error = "Username is taken!"
            return render_template("register.html", error=error, questions=questions)
        elif len(db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")]).fetchall()) != 0:
            #return email error
            error = "Email already has an account!"
            return render_template("register.html", error=error, questions=questions)

        else:
            error = "Registration Successful!"
            db.execute("INSERT INTO users (username, email, hashedpass, security_id, security_hash) VALUES (?, ?, ?, ?, ?)", (username, email, generate_password_hash(password),security_id, generate_password_hash(security_answer)))
            conn.commit()
            return render_template("register.html", error=error, questions=questions)


    else:
        conn, db = make_cursor("coursedatabase.db")
        db.execute("SELECT * FROM security")
        questions = db.fetchall()
        return render_template("register.html", questions=questions)

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

""" Course Search"""
@app.route("/search")
def search():
    search = "currentpage"
    return render_template("search.html", search=search)


""" Course Search Results """
@app.route("/searchresults", methods=(["GET","POST"]))
def searchresults():
    conn, db = make_cursor("coursedatabase.db")
    search = "currentpage"
    querystring = request.args.get("q")
    page = request.args.get(get_page_parameter(), type=int, default=1) 
    session["page"] = page
    offset = (page - 1) * perpage

    session["last_search"] = querystring
    if not querystring:
        db.execute("SELECT * FROM courses LIMIT ? OFFSET ?", (perpage, offset))
        results = db.fetchall()
        total = db.execute("SELECT * FROM courses").fetchall()
        pagination = Pagination(page=page, total=len(total), search=False, record_name='courses', per_page=perpage, css_framework='bootstrap4')
        return render_template("results.html", querystring=querystring, search=search, results=results, pagination=pagination)
                
    else:
        db.execute("SELECT * FROM courses WHERE INSTR(LOWER(name),LOWER(?))", [querystring])
        results = db.fetchall()
        total = results
        if not results:
            return render_template("search.html", querystring=querystring, search=search)
        else:
            db.execute("SELECT * FROM courses WHERE INSTR(LOWER(name),LOWER(?)) LIMIT ? OFFSET ?", (querystring, perpage, offset))
            results = db.fetchall()
            pagination = Pagination(page=page, total=len(total), search=False, record_name='courses', per_page=perpage, css_framework='bootstrap4')
            return render_template("results.html", querystring=querystring, search=search, results=results, pagination=pagination)
        
""" My Courses """
@app.route('/mycourses')
@login_required
def mycourses():
    mycourses = "currentpage"
    conn, db = make_cursor("coursedatabase.db")
    user_id = session["user_id"]
    db.execute("SELECT courses.id, courses.name, courses.description, courses.code FROM courses JOIN favourites ON favourites.course_id = courses.id WHERE favourites.user_id = ?", [user_id])
    favourites = db.fetchall()
    completed = db.execute("SELECT courses.id, courses.name, courses.description, courses.code FROM courses JOIN completed ON completed.course_id = courses.id WHERE completed.user_id = ?", [user_id]).fetchall()
    return render_template("mycourses.html", mycourses=mycourses, favourites=favourites, completed=completed)


@app.route("/favourite", methods=(["GET","POST"]))
@login_required
def favourite():
    pagenum = session["page"]
    mycourses = "currentpage"
    if request.method == "GET":
        conn, db = make_cursor("coursedatabase.db")
        user_id = session["user_id"]
        db.execute("SELECT courses.id, courses.name, courses.description, courses.code FROM courses JOIN favourites ON favourites.course_id = courses.id WHERE favourites.user_id = ?", [user_id])
        results = db.fetchall()
        if not results:
            return render_template("search.html", querystring="your favourites", search=search)
        else:
            page = request.args.get(get_page_parameter(), type=int, default=1) 
            pagination = Pagination(page=page, total=len(results), search=False, record_name='courses')
            return render_template("results.html", mycourses=mycourses, results=results, pagination=pagination)
    else:
        conn, db = make_cursor("coursedatabase.db")
        course_id = request.form.get("id")
        user_id = session["user_id"]
        querystring = session["last_search"]
        db.execute("SELECT * FROM favourites WHERE user_id = ? AND course_id = ?", (user_id, course_id))
        rows = db.fetchall()
        flash('Added to favourites!')
        if len(rows) == 0:
            db.execute("INSERT INTO favourites VALUES(?,?)", (user_id, course_id))
            conn.commit()
        else:
            session.pop('_flashes', None)
            flash('Already in your favourites!')
        
        return redirect(url_for("searchresults",q=querystring, page=pagenum))

""" Remove Favourite"""
@app.route("/removefavourite", methods=(["GET","POST"]))
@login_required
def removefavourite():
    conn, db = make_cursor("coursedatabase.db")
    course_id = request.form.get("id")
    user_id = session["user_id"]
    db.execute("SELECT * FROM favourites WHERE user_id = ? AND course_id = ?", (user_id, course_id))
    rows = db.fetchall()
    if len(rows) != 0:
        coursecode =  db.execute("SELECT courses.code FROM courses JOIN favourites ON favourites.course_id = courses.id WHERE favourites.user_id = ? AND favourites.course_id = ?", (user_id, course_id)).fetchall()
        db.execute("DELETE FROM favourites WHERE user_id = ? AND course_id = ?", (user_id, course_id))
        conn.commit()
        message = str(coursecode[0][0]) + " removed from favourites!"
    
    db.execute("SELECT courses.id, courses.name, courses.description, courses.code FROM courses JOIN favourites ON favourites.course_id = courses.id WHERE favourites.user_id = ?", [user_id])
    favourites = db.fetchall()
    mycourses = "currentpage"
    return render_template("mycourses.html",message=message, mycourses=mycourses, favourites=favourites)

""" Completed Courses"""
@app.route("/completed", methods=(["GET","POST"]))
@login_required
def completed():
    pagenum = session["page"]
    mycourses = "currentpage"
    if request.method == "GET":
        conn, db = make_cursor("coursedatabase.db")
        user_id = session["user_id"]
        db.execute("SELECT courses.id, courses.name, courses.description, courses.code FROM courses JOIN completed ON completed.course_id = courses.id WHERE completed.user_id = ?", [user_id])
        results = db.fetchall()
        if not results:
            return render_template("search.html", querystring="your favourites", search=search)
        else:
            page = request.args.get(get_page_parameter(), type=int, default=1) 
            pagination = Pagination(page=page, total=len(results), search=False, record_name='courses')
            return render_template("results.html", mycourses=mycourses, results=results, pagination=pagination)
    else:
        conn, db = make_cursor("coursedatabase.db")
        course_id = request.form.get("check")
        user_id = session["user_id"]
        querystring = session["last_search"]
        db.execute("SELECT * FROM completed WHERE user_id = ? AND course_id = ?", (user_id, course_id))
        rows = db.fetchall()
        flash('Added to completed courses!')
        if len(rows) == 0:
            db.execute("INSERT INTO completed VALUES(?,?)", (user_id, course_id))
            conn.commit()
        else:
            session.pop('_flashes', None)
            flash('Already in your completed courses!')
        
        return redirect(url_for("searchresults",q=querystring, page=pagenum))



""" Schedule """
@app.route("/schedule", methods=(["GET","POST"]))
@login_required
def schedule():
    schedule = "currentpage"
    return render_template("schedule.html", schedule=schedule)

""" My Tracks """

@app.route("/mytracks", methods=(["GET","POST"]))
@login_required
def mytracks():
    tracks = "currentpage"
    mytracks = "currentpage1"
    return render_template("mytracks.html", tracks=tracks, mytracks=mytracks)

        
""" Track Planner """
@app.route("/trackplanner", methods=(["GET","POST"]))
@login_required
def trackplanner():
    tracks = "currentpage"
    trackplanner = "currentpage1"
    return render_template("trackplanner.html", tracks=tracks, trackplanner=trackplanner)

""" Account """
@app.route("/account", methods=(["GET","POST"]))
@login_required
def account():
    account = "currentpage"
    return render_template("account.html", account=account)

