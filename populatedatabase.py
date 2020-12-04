import pandas as pd
import sqlite3
from helpers import make_cursor
import math

# Import from a CSV file the data scraped from my.harvard 
data = pd.read_csv(r'static/HarvardCourses-DataMinerMostCompleteSet.csv')

# Reformat the data as a DataFrame object
frame = pd.DataFrame(data, columns=['name','code','professor','school','description','semester','day','time','term'])

# Check dataframe construction
# print(frame)

# Connect to database
conn, db = make_cursor("coursedatabase.db")

# Clear database implemented so that we could move on from our initial population and architecture a little more cleanly
db.execute("DROP TABLE IF EXISTS antirequisites;")
db.execute("DROP TABLE IF EXISTS corequisites;")
db.execute("DROP TABLE IF EXISTS courses;")
db.execute("DROP TABLE IF EXISTS days;")
db.execute("DROP TABLE IF EXISTS favourites;")
db.execute("DROP TABLE IF EXISTS instructors;")
db.execute("DROP TABLE IF EXISTS meets_requirements;")
db.execute("DROP TABLE IF EXISTS offered_courses;")
db.execute("DROP TABLE IF EXISTS prerequisites;")
db.execute("DROP TABLE IF EXISTS requirements;")
db.execute("DROP TABLE IF EXISTS schedule;")
db.execute("DROP TABLE IF EXISTS security;")
db.execute("DROP TABLE IF EXISTS sessions;")
db.execute("DROP TABLE IF EXISTS track_types;")
db.execute("DROP TABLE IF EXISTS tracks;")
db.execute("DROP TABLE IF EXISTS users;")
conn.commit()

# Create most updated database structure
db.execute("""CREATE TABLE courses (
            id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            code TEXT UNIQUE NOT NULL,
            PRIMARY KEY(id)
            );""")

db.execute("""CREATE TABLE sessions (
            id INTEGER,
            year INTEGER NOT NULL,
            term TEXT NOT NULL,
            PRIMARY KEY(id)
            );""")

db.execute("""CREATE TABLE instructors (
            id INTEGER,
            name TEXT NOT NULL,
            PRIMARY KEY(id)
            );""")

db.execute("""CREATE TABLE offered_courses (
            id INTEGER,
            course_id INTEGER,
            instructor_id INTEGER,
            session_id INTEGER,
            PRIMARY KEY(id),
            FOREIGN KEY(course_id) REFERENCES courses(id),
            FOREIGN KEY(instructor_id) REFERENCES instructors(id),
            FOREIGN KEY(session_id) REFERENCES sessions(id)
            );""")

db.execute("""CREATE TABLE prerequisites (
            course_id INTEGER,
            prereq_id INTEGER,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            FOREIGN KEY(prereq_id) REFERENCES courses(id)
            );""")

db.execute("""CREATE TABLE corequisites (
            course_id INTEGER,
            coreq_id INTEGER,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            FOREIGN KEY(coreq_id) REFERENCES courses(id)
            );""")

db.execute("""CREATE TABLE antirequisites (
            course_id INTEGER,
            antireq_id INTEGER,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            FOREIGN KEY(antireq_id) REFERENCES courses(id)
            );""")

db.execute("""CREATE TABLE days (
            id INTEGER,
            day TEXT,
            PRIMARY KEY(id)
            );""")

db.execute("""INSERT INTO days
            (day)
            VALUES
            ("Sunday"),
            ("Monday"),
            ("Tuesday"),
            ("Wednesday"),
            ("Thursday"),
            ("Friday"),
            ("Saturday");""")

db.execute("""CREATE TABLE schedule (
            offering_id INTEGER NOT NULL,
            day_id INTEGER NOT NULL,
            start_time TIME[0] NOT NULL,
            end_time TIME[0] NOT NULL,
            FOREIGN KEY(offering_id) REFERENCES offered_couses(id),
            FOREIGN KEY(day_id) REFERENCES days(id)
            );""")

db.execute("""CREATE TABLE security (
            id INTEGER,
            question TEXT NOT NULL UNIQUE,
            PRIMARY KEY(id)
            );""")

db.execute("""INSERT INTO security
            (question)
            VALUES
            ("First pet's name"),
            ("Town you grew up in"),
            ("Childhood best friend"),
            ("Father's middle name"),
            ("Mother's maiden name"),
            ("Name of your highschool"),
            ("Favourite sports team"),
            ("Surname of your favourite teacher");""")

db.execute("""CREATE TABLE users (
            id INTEGER,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            hashedpass TEXT NOT NULL,
            security_id INTEGER NOT NULL,
            security_hash TEXT NOT NULL,
            exposplacement INTEGER,
            mathsplacement INTEGER,
            PRIMARY KEY(id),
            FOREIGN KEY(security_id) REFERENCES security(id)
            FOREIGN KEY(exposplacement) REFERENCES courses(id)
            FOREIGN KEY(mathsplacement) REFERENCES courses(id)
            );""")

db.execute("""CREATE TABLE favourites (
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
            );""")

db.execute("""CREATE TABLE track_types (
            id INTEGER,
            type TEXT,
            PRIMARY KEY(id)
            );""")

db.execute("""INSERT INTO track_types
            (type)
            VALUES
            ("Citation"),
            ("Secondary"),
            ("Concentration"),
            ("General Ed");""")

db.execute("""CREATE TABLE tracks (
            id INTEGER,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            length TEXT,
            type_id INTEGER,
            PRIMARY KEY(id),
            FOREIGN KEY(type_id) REFERENCES track_types(id)
            );""")

db.execute("""CREATE TABLE requirements (
            id INTEGER,
            track_id INTEGER,
            name TEXT,
            description TEXT,
            length TEXT,
            PRIMARY KEY(id),
            FOREIGN KEY(track_id) REFERENCES tracks(id)
            );""")

db.execute("""CREATE TABLE meets_requirements (
            requirement_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY(requirement_id) REFERENCES requirements(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
            );""")

conn.commit()

# Insert data into the relevant tables
for row in frame.itertuples():
    db.execute(""" SELECT * FROM courses WHERE courses.code = ?""", [row.code])
    checkrow = db.fetchall()
    if len(checkrow) == 0:
        db.execute("""INSERT INTO courses
                (name, description, code)
                VALUES
                (?, ?, ?)
                """, (row.name, row.description, row.code))
    # Full disclosure, this is going to delete professors with the same name and store them as single instructors,
    # because we only have two surnames, giving us two options - make redundant rows with professor's names who teach 
    # multiple classes (most professors), essentially making the point of this table to remove redundancies moot, or to do
    # what we have done. As the professors tables do not link to anything prof-specific and only provides a name, saving
    # makes the most sense to me
    db.execute(""" SELECT * FROM instructors WHERE instructors.name = ?""", [row.professor])
    checkrow = db.fetchall()
    if len(checkrow) == 0:
        db.execute("""INSERT INTO instructors
                (name)
                VALUES
                (?);
                """, [row.professor])

    semester = row.semester.split(' ')
    db.execute(""" SELECT * FROM sessions WHERE sessions.year = ? AND sessions.term = ?""", (semester[1],semester[0]))
    checkrow = db.fetchall()
    if len(checkrow) == 0:
        db.execute("""INSERT INTO sessions
                (term, year)
                VALUES
                (?, ?);
                """, (semester[0],semester[1]))
    
    db.execute(""" SELECT id FROM courses WHERE courses.code = ?""", [row.code])
    course_id = db.fetchone()
    db.execute(""" SELECT id FROM instructors WHERE instructors.name = ?""", [row.professor])
    instructor_id = db.fetchone()
    db.execute(""" SELECT id FROM sessions WHERE sessions.year = ? AND sessions.term = ?""", (semester[1],semester[0]))
    session_id = db.fetchone()

    db.execute("""INSERT INTO offered_courses
    (course_id, instructor_id, session_id)
    VALUES
    (?, ?, ?);
    """, (course_id + instructor_id + session_id))

    db.execute(""" SELECT offered_courses.id FROM offered_courses JOIN courses ON offered_courses.course_id = courses.id WHERE courses.code = ?""", [row.code])
    offering_id = db.fetchone()

conn.commit()