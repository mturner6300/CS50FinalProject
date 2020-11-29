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
    