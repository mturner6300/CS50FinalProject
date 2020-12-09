# CS50FinalProject - myharvard2: Electric Boogaloo
Ethan Arellano, Sam Blackman, Meghan Turner

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

Though beware that this may interefere with other 

from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from helpers import login_required, make_cursor, refresh_placements
from flask_session import Session
from flask_paginate import Pagination, get_page_parameter
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import random
import string
import smtplib, ssl
import os
import ctypes
import requests
import urllib.parse
import pandas as pd
import math