from flask import Flask, flash, redirect, render_template, request, session
from helpers import login_required
from flask_session import Session
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

    # Post is submission
    if request.method == "POST":
        # Ensure username and password were submitted
        if not request.form.get("username"):
            return render_template("login.html", message="You must enter your username")
        elif not request.form.get("password"):
            return render_template("login.html", message="You must enter your password")
        
        # Check for correct username and password
        db.execute("SELECT id, hashedpass FROM users WHERE username=?", [request.form.get("username")])
        rows = db.fetchall()
        if len(rows) != 1:
            return render_template("login.html", message="Username does not exist")
        
        user_id, hashed_pass = rows[0]
        if not check_password_hash(hashed_pass,request.form.get("password")):
            return render_template("login.html", message="Wrong password")
        

        # Store username and return to home
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("login.html")


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

""" Course Search """
@app.route("/search", methods=(["GET","POST"]))
def search():
    conn, db = make_cursor("coursedatabase.db")
    """ Get accesses the in-depth search page with GET"""
    """ Search Courses with POST from any page """
    search = "currentpage"
    if request.method == "GET":
        return render_template("search.html", search=search)
    else:
        querystring = request.form.get("q")
        if not querystring:
            db.execute("SELECT * FROM courses")
            results = db.fetchall()
            
            return render_template("results.html", querystring=querystring, search=search, results=results)
        else:
            db.execute("SELECT * FROM courses WHERE INSTR(LOWER(name),LOWER(?))", [querystring])
            results = db.fetchall()
            
            if not results:
                return render_template("search.html", querystring=querystring, search=search)
            else:
                return render_template("results.html", querystring=querystring, search=search, results=results)
        
""" My Courses """



@app.route("/favourite", methods=(["GET","POST"]))
@login_required
def favourite():
    if request.method == "GET":
        conn, db = make_cursor("coursedatabase.db")
        user_id = session["user_id"]
        db.execute("SELECT courses.name FROM favourites JOIN courses ON favourites.course_id = courses.id WHERE favourites.user_id = ?", user_id)
        results = db.fetchall()
        if not results:
            return render_template("search.html", querystring="your favourites", search=search)
        else:
            return render_template("results.html", search=search, results=results)
    else:
        conn, db = make_cursor("coursedatabase.db")
        course_id = request.form.get("id")
        user_id = session["user_id"]
        db.execute("INSERT INTO favourites VALUES(?,?)", user_id, course_id)
        conn.commit()
        return redirect(request.referrer)

""" Schedule """

""" My Tracks """
    
        
        

    