/* Create database and start sql client */
sqlite3 coursedatabase.db

/* Create course table according to the architecture in our design */
CREATE TABLE courses (
id INTEGER,
name TEXT NOT NULL UNIQUE,
description TEXT NOT NULL,
code TEXT UNIQUE NOT NULL,
PRIMARY KEY(id)
);

/* Create sessions table according to the architecture in our design */
CREATE TABLE sessions (
id INTEGER,
year INTEGER NOT NULL,
term TEXT NOT NULL,
PRIMARY KEY(id)
);

/* Create instructors table according to the architecture in our design */
CREATE TABLE instructors (
id INTEGER,
name TEXT NOT NULL,
PRIMARY KEY(id)
);

/* Create offered courses table according to the architecture in our design */
CREATE TABLE offered_courses (
id INTEGER,
course_id INTEGER,
instructor_id INTEGER,
session_id INTEGER,
PRIMARY KEY(id),
FOREIGN KEY(course_id) REFERENCES courses(id),
FOREIGN KEY(instructor_id) REFERENCES instructors(id),
FOREIGN KEY(session_id) REFERENCES sessions(id)
);

/* Create prereq courses table according to the architecture in our design */
CREATE TABLE prerequisites (
course_id INTEGER,
prereq_id INTEGER,
FOREIGN KEY(course_id) REFERENCES courses(id),
FOREIGN KEY(prereq_id) REFERENCES courses(id)
);

/* Create prereq courses table according to the architecture in our design */
CREATE TABLE corequisites (
course_id INTEGER,
coreq_id INTEGER,
FOREIGN KEY(course_id) REFERENCES courses(id),
FOREIGN KEY(coreq_id) REFERENCES courses(id)
);

/* Create antireq courses table according to the architecture in our design */
CREATE TABLE antirequisites (
course_id INTEGER,
antireq_id INTEGER,
FOREIGN KEY(course_id) REFERENCES courses(id),
FOREIGN KEY(antireq_id) REFERENCES courses(id)
);

/* Add a test course into the courses table */
INSERT INTO courses
(name, description, code) VALUES
("Building a Human Body: From Gene to Cell to Organism", "Through a series of lectures, application exercises and laboratory experiments, we will explore how the human body develops on a molecular level from gene to cell to organ. Ever wonder how you can make heart cells beat in a dish? Why can axolotls regenerate their limbs but humans cannot? How do neurites grow? Can we grow a brain in a cell culture dish? Come join us to discover the answers to these questions and more.","SCRB 50");

/* And its prereq */
INSERT INTO courses
(name, description, code) VALUES
("An Integrated Introduction to the Life Sciences: Chemistry, Molecular Biology, and Cell Biology", "What are the fundamental features of living systems? What are the molecules imparting them and how do their chemical properties explain their biological roles? The answers form a basis for understanding the molecules of life, the cell, diseases, and medicines. In contrast with traditional presentations of relevant scientific disciplines in separate courses, we take an integrated approach, presenting chemistry, molecular biology, biochemistry, and cell biology framed within central problems such as the biology of HIV and cancer.","LIFESCI 1A");

/* Now let's link them in the prereqs table */
INSERT INTO prerequisites
(course_id, prereq_id)
VALUES ((SELECT id FROM courses WHERE code="SCRB 50"), (SELECT id FROM courses WHERE code="LIFESCI 1A"));

/* Create and then populate days table accoriding to the architecture in our design */
CREATE TABLE days (
id INTEGER,
day TEXT,
PRIMARY KEY(id)
);

INSERT INTO days
(day)
VALUES
("Sunday"),
("Monday"),
("Tuesday"),
("Wednesday"),
("Thursday"),
("Friday"),
("Saturday");

/* Create schedule table accoriding to the architecture in our design */
CREATE TABLE schedule (
offering_id INTEGER NOT NULL,
day_id INTEGER NOT NULL,
start_time TIME[0] NOT NULL,
end_time TIME[0] NOT NULL,
FOREIGN KEY(offering_id) REFERENCES offered_couses(id),
FOREIGN KEY(day_id) REFERENCES days(id)
);