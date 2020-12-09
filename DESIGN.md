Hi! Welcome to our design file! Here we'll take you through how we designed our web application, myharvard2: Electric Boogaloo

Let's start by running through the libraries we installed, and what we installed them for:
flask - this is one of python's best-liked and most-used libraries for hosting dynamic web applications. We use flask to host and run our app.
flask_session - this is an extension library for Flask, which enables the storage of simple pieces of information on the user's device. We use this to remember logged-in accounts, previous searches, search result page numbers, and to flash transient messages to the user about actions they have taken 
flask_paginate - this is an extension library for flask, which enables the storage of large amounts of data, such as search results, over multiple pages, to reduce loading times and improve the appearance of our site, which deals with throusands of courses.
tempfile - this is a library making and managing simple, temporary user-side files, which we use to make temporary directories in which to store sessions
werkzeug.exceptions - this is a library that raises standard error messages for non-200 status responses, which we have used to make dealing with exceptions to http requests a little cleaner and clearer to programmers
werkzeug.security - this is a library that enables some basic security functions in an application, which we use to generate and check hashes
sqlite3 - this is a library used to interface with sqlite databases, which we have used to do just that, allowing us to query our database, adding, retrieving, and removing information either transiently or permanently
random - this is a library used to generate pseudorandom numbers/strings, which we use to generate temporary passwords when one is forgotten. This was not our first choice for this functionality, prefering the secrets library, which uses truer randomness, however, we had some issues requiring extensions for this library late in the development, and decided to use the native random to be able focus on other functionality (the emailing platform). This is a flawed design, but given that it was a temporary password and we wanted to add in other functionality, we were willing to acquiesce for the proof of concept
string - this library adds some basic functionality with strings such as constant lists for ASCII characters which we use to generate our temporary password.
smtplib - this is a library which allows generation of a server for sending and reading emails which we use to send the username and temporary password of a user who has forgotten their username or password.
ssl - this is a library which generates secure contexts for email servers such as smtplib, which we use for an encrypted context for our servers, to add security to our sending of emails.
os - ?
ctypes - ?
requests - a library for retrieving information from http requests
urllib.parse - a library for parsing (separating into constituent parts) urls for easier use
pandas - a library for dealing with importing data which we use with sqlite3 to import our data-scraped data from csv files into our sql database
math - a library for adding some extra maths functionality in python