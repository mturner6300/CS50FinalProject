import os
import requests
import urllib.parse
import sqlite3

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    # Ensures following function is included in this function f
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If there is no user logged in
        if session.get("user_id") is None:
            # End function before wrapped function's functionality begins
            return redirect("/login")
        # Otherwise there is a user logged in, so continue with function f
        return f(*args, **kwargs)
    # Return the result - either the function flask/user was trying, or redirect login.
    return decorated_function

# Define function to intialise database
def make_cursor(database):
    # Connect to the database
    connection = sqlite3.connect(database)
    # Return connection and a cursor to commit permanently to the database and to interact transiently with the database respectively
    return connection, connection.cursor()

# Define function to refresh placements on account page
def refresh_placements(user_id, cursor):
    # Retrieve the (general) names and placement ids of the expos placement courses (see populatedatabase.py for more on why this was out structure)
    expos_placements = cursor.execute("""SELECT placement_courses.id, placement_courses.name FROM placement_courses
                                        JOIN placement_types ON placement_types.id = placement_courses.placement_type_id
                                        WHERE placement_type = "Expos";
                                        """).fetchall()

    # Retrieve the (general) names and placement ids of the maths placement courses
    maths_placements = cursor.execute("""SELECT placement_courses.id, placement_courses.name FROM placement_courses
                                    JOIN placement_types ON placement_types.id = placement_courses.placement_type_id
                                    WHERE placement_type = "Math";
                                    """).fetchall()

    # Retrieve the (general) names and placement ids of the lifesci placement courses
    lifesci_placements = cursor.execute("""SELECT placement_courses.id, placement_courses.name FROM placement_courses
                                    JOIN placement_types ON placement_types.id = placement_courses.placement_type_id
                                    WHERE placement_type = "Lifesci";
                                    """).fetchall()

    # Retrieve the user's previously submitted maths placement 
    my_maths_placement = cursor.execute(""" SELECT placements.placement_id, placement_courses.name FROM placements
                                        JOIN placement_courses ON placement_courses.id = placement_id
                                        JOIN placement_types ON placement_types.id = placement_courses.placement_type_id
                                        WHERE user_id = ? AND placement_type = "Math";
                                        """, [user_id]).fetchall()

    # Retrieve the user's previously submitted expos placement 
    my_expos_placement = cursor.execute(""" SELECT placements.placement_id, placement_courses.name FROM placements
                                    JOIN placement_courses ON placement_courses.id = placement_id
                                    JOIN placement_types ON placement_types.id = placement_courses.placement_type_id
                                    WHERE user_id = ? AND placement_type = "Expos";
                                    """, [user_id]).fetchall()

    # Retrieve the user's previously submitted lifesci placement 
    my_lifesci_placement = cursor.execute(""" SELECT placements.placement_id, placement_courses.name FROM placements
                                    JOIN placement_courses ON placement_courses.id = placement_id
                                    JOIN placement_types ON placement_types.id = placement_courses.placement_type_id
                                    WHERE user_id = ? AND placement_type = "Lifesci";
                                    """, [user_id]).fetchall()

    # Return results
    return expos_placements, maths_placements, lifesci_placements, my_expos_placement, my_maths_placement, my_lifesci_placement