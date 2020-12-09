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

(You may need to run these same lines with either "py3" or "python3" if you have multiple versions of Python installed)

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

pip3 install library
for all of the following libraries (replace "library" with each of the library names below)
(Anaconda users especially, you will notice that many of these are already installed! If they are, the command prompt should just tell you so!]):
flask
flask_session
flask_paginate
tempfile
werkzeug.exceptions
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
functools

(I would advise pip3, assuming you are using python 3, but either should work. If you use pip and then something breaks later on, there is a good chance you will need to run pip3 install instead)

Please bear in mind, some of these are native to python (os, smtplib, ssl, etc.) so you should find a lot of these responding with already installed, but we would rather give you the full list than have you struggling to run anything because you didn't know to check!

It should also be noted, you may need to download a DLL file for your OS for sqlite3 from (https://www.sqlite.org/download.html) and place it into the DLLs file in your anaconda files at C:\Users\YOURUSER\Anaconda3\DLLs or C:\ProgramData\Anaconda3\DLLs
if you are an anaconda user. This may or may not be necessary to run populatedatabase.py, which leads hopefully nicely into the structure of our project.

Our main project folder, titled "CS50FINALPROJECT" contains a python cache folder "_pycache_" of recent changes to/by python files (you will never need to open this), a folder "static" in which all our static files (i.e. images, backgrounds, csv files) have been placed, a folder "templates" which contains all our html files including "layout.html" which is the file that sets the base layout for all other htmls, a folder "venv" which supports setting up a virtual environment through which to host the website if you are running it through your native command prompt (more on this below), app.py which is the flask application that implements most of our functionality, coursedatabase.db which is the database for our site, DESIGN.md which contains details of our design process, helpers.py which contains a few functions we separated out from app.py for concision, myharvard2.sql which contains sql that designed and reset the original sql database, populatedatabase.py which designs and resets our final iteration of the sql database, and a recording of our video, which can also be found at https://youtu.be/wwsag9WcAMA

If you are missing any of these files, then you may want to repeat whatever you did in order to collect them, view/clone our public github repo at(https://github.com/mturner6300/CS50FinalProject), or reach out to us to let us know that we are missing something (god-willing, we won't be).

You should now be able to change directory in yor command prompt into the folder in which our program is downloaded on your device with a line of code like:
cd route\CS50FinalProject

On my computer, this line is:
cd OneDrive\Documents\GitHub\CS50FinalProject

BE AWARE: If you, like us, have a computer that automatically connects to the cloud via a service such as OneDrive, then the files you downloaded may not be local to your disk, and might in fact be in a route such as OneDrive as above. 

Now you should be able to run the command:
run flask

which should return to you:

* Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://123.0.0.4:5678/ (Press CTRL+C to quit)

from which you can copy the returned url e.g. http://123.0.0.4:5678/ into your web browser of choice, to access our web app. 

You should be welcomed with the index page, which will allow you to register via a button in the center of the screen. This will redirect you to fill in your information, including a REAL EMAIL ADDRESS, which will enable our functionality for forgotten usernames/passwords. We implemented a cursory check for real email addresses (see design for more information) but we are aware that this is not 100% sufficient for somebody trying to fool the site. Be aware, if you fool the site and do not enter an email address that is a. real and b. accessible by you, you will not be able to retrieve your account. You don't need to register immediately, you can take a look at the about us page.

Once you register (confirming your information correctly, unique username, an email address), the site will automatically log you in, giving you free reign to try out the site. For more information on the rest of the site, see DESIGN.md

Virtual Environment Usage:

Because we have used different versions of Python and its libraries in other classes, we created a virtual environment (venv folder) as to not conflict with any other versions of Python/libraries we may already have installed in our computers.

If you also have possible conflicting versions of Python and want to use our virtual environemnt (which should have all libraries and dependencies installed), you can do so by doing the following:

1) Enter the CS50FinalProject directory.

2) Run the following line of code:

venv\Scripts\activate

which should return: (venv) ***YOUR CURRENT PATHWAY*** 

for example: (venv) C:\Users\Meghan\Documents\GitHub\CS50FinalProject> 

Now you can run: flask run

and receive the similar to message to the one above:

* Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Disclaimer on Virtual Environment:

We have installed libraries for features we had planned to implement at one point but have now decided against adding. We have tried to remove these files from the virtual environment but may have overlooked a few due to the number of packages installed. These should not impact the functionality of the website. 

Lastly, as only one member of the group was using the virtual environment and installing packages to that location, an installation may have been overlooked for a feature added by the other members. If you find a package is not installed, you may run the "pip install **library**" commands referenced earlier in this document in the venv directory to add the necessary files. 