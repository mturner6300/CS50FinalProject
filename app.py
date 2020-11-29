from flask import Flask, flash, redirect, render_template, request, session
app = Flask(__name__)

@app.route('/')
def index():
    home = "currentpage"
    return render_template("index.html", home=home)

@app.route("/about", methods=(["GET","POST"]))
def about():
    about = "currentpage"
    return render_template("about.html", about=about)

@app.route("/explore", methods=(["GET","POST"]))
def explore():
    explore = "currentpage"
    return render_template("explore.html", explore=explore)

@app.route("/tracks", methods=(["GET","POST"]))
def tracks():
    tracks = "currentpage"
    return render_template("tracks.html", tracks=tracks)

@app.route("/myaccount", methods=(["GET","POST"]))
def myaccount():
    myaccount = "currentpage"
    return render_template("myaccount.html", myaccount=myaccount)

@app.route("/contactus", methods=(["GET","POST"]))
def contactus():
    contactus = "currentpage"
    return render_template("contactus.html", contactus=contactus)


    