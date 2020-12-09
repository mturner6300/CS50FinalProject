# CS50FinalProject - myharvard2: Electric Boogaloo
Ethan Arellano, Sam Blackman, Meghan Turner
Video online at: https://youtu.be/wwsag9WcAMA

This is a web application built on the python flask library aiming to improve upon the functionality of my.harvard's course and concentration functionalities. We use a number of libraries other than flask, so please bear with us as we guide you through setting these up so that you too can experience myharvard2: Electric Boogaloo. We highly recommend that you download Anaconda (https://www.anaconda.com/products/individual) for its command prompt and python libraries, GitHub Desktop (https://desktop.github.com/) to access the repository containing all of our files, and VS Code (https://code.visualstudio.com/) to interface with and read our code and SQL database. Furthermore, if you want to investigate our SQL further, we recommend this (https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite) add-on for VS Code, though the code will run without it.

Disclaimer: All three of us are Windows users, I do not believe that any one of use have ever used and Apple PC, so this ReadMe will be heavily influenced by that fact. We will try to include resources for Apple users where we can, but do bear in mind that we have no means to host this on any PCs other than our own, least of all an Apple device which likely cost twice as much as my laptop :) Thank you for your time!!!

We won't assume that you already have python installed, so please go to the python site (https://www.python.org/downloads/) to download the most recent version of python (I believe we were all running 3.8 and 3.8). If you get anaconda, this should not be necessary, and nor will many of the library downloads we will go through, which are native to python. Crucial to installing any of these libraries is will be pip, the python installer. In your command prompt of choice run:

py -m pip --version 
(Windows) 

or 

python -m pip --version 
(Unix/macOS)

to check if pip is already installed (as it should be with any recent python build or Anaconda). If pip needs an update you can do so with:

py -m pip install -U pip
(Windows)

or

python -m pip install -U pip
(Unix/macOS)

or if you need to install pip (i.e. you want to run things through your native command prompt) download pip via:

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

then setup with:

py get-pip.py
(Windows)

or

python get-pip.py
(Unix/macOS)

Though beware that this may interefere with other occurences of pip on your computer so don't do this if you already have it (please, run the installation/update checks above!)

Now that you have pip you should be able to begin installing the libraries below through your prompt of choice.
Please run either:

pip install [replace with library]

or 

pip3 install [replace with library]
for all of the following libraries
(Anaconda users especially, you will notice that many of these are already installed! If they are, the command prompt should just tell you so!]):
flask
flask_session
flask_paginate
tempfile
werkzeug.exceptions
werkzeug.security
werkzeug.security
sqlite3
random
string
smtplib
ssl
os
ctypes
requests
urllib.parse
pandas
math

(I would advise pip3, assuming you are using python 3, but either should work. If you use pip and then something breaks later on, there is a good chance you will need to run pip3 install instead)

Please bear in mind, some of these are native to python (os, smtplib, ssl, etc.) so you should find a lot of these responding with already installed, but we would rather give you the full list than have you struggling to run anything because you didn't know to check!

It should also be noted, you may need to download a DLL file for your OS for sqlite3 from (https://www.sqlite.org/download.html) and place it into the DLLs file in your anaconda files at C:\Users\YOURUSER\Anaconda3\DLLs or C:\ProgramData\Anaconda3\DLLs
if you are an anaconda user. This may or may not be necessary to run populatedatabase.py, which leads hopefully nicely into the structure of our project.

Our main project folder, titled "CS50FINALPROJECT" contains a python cache folder "_pycache_" of recent changes to/by python files (you will never need to open this), a folder "static" in which all our static files (i.e. images, backgrounds, csv files) have been placed, a folder "templates" which contains all our html files including "layout.html" which is the file that sets the base layout for all other htmls, a folder "venv" which supports setting up a virtual environment through which to host the website if you are running it through your native command prompt (more on this below), app.py which is the flask application that implements most of our functionality, coursedatabase.db which is the database for our site, DESIGN.md which contains details of our design process, helpers.py which contains a few functions we separated out from app.py for concision, myharvard2.sql which contains sql that designed and reset the original sql database, populatedatabase.py which designs and resets our final iteration of the sql database, and a recording of our video, which can also be found at https://youtu.be/wwsag9WcAMA


