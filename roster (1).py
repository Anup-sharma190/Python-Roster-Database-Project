"""
=====================================================
 Project: Roster Database Builder using JSON + SQLite
 Author: Anup Sharma
 Skills: Python, JSON, SQLite, Data Normalization, SQL Joins
 Tools: Python3, SQLite3

 Description:
 ------------
 This project demonstrates how to:
   - Read data from a JSON file
   - Create normalized database tables (User, Course, Member)
   - Insert and relate data using foreign keys
   - Execute SQL queries with JOIN operations
   - Generate a unique hash-based answer for verification

 This is part of Dr. Chuck's "Python for Everybody" specialization.
 It is useful for showcasing **Database Handling + Python + SQL integration**.
=====================================================
"""

import json
import sqlite3

# -------------------- Step 1: Connect to SQLite DB --------------------
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# -------------------- Step 2: Drop old tables --------------------
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;
''')

# -------------------- Step 3: Create new tables --------------------
cur.executescript('''
CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

# -------------------- Step 4: Load data from JSON file --------------------
fname = 'roster_data.json'   # JSON file with [name, course, role]
str_data = open(fname).read()
json_data = json.loads(str_data)

# -------------------- Step 5: Insert data into tables --------------------
for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    cur.execute('INSERT OR IGNORE INTO User (name) VALUES ( ? )', (name,))
    cur.execute('SELECT id FROM User WHERE name = ? ', (name,))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES ( ? )', (title,))
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title,))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role)
        VALUES ( ?, ?, ? )''',
        (user_id, course_id, role))

conn.commit()

# -------------------- Step 6: Verification Query --------------------
print("\nFirst verification query:")
cur.execute('''
SELECT User.name, Course.title, Member.role FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;
''')

for row in cur:
    print(f"{row[0]} | {row[1]} | {row[2]}")

# -------------------- Step 7: Final Assignment Answer --------------------
print("\nFinal code (verification hash):")
cur.execute('''
SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1;
''')

row = cur.fetchone()
print(row[0])

cur.close()
