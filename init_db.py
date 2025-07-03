import sqlite3
conn = sqlite3.connect('scheduler.db')
c = conn.cursor()

# Faculty table
c.execute('''
CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL
)
''')

# Exams table
c.execute('''
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    session TEXT NOT NULL
)
''')

# Rooms table (linked to exams)
c.execute('''
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER NOT NULL,
    room_no TEXT NOT NULL,
    FOREIGN KEY (exam_id) REFERENCES exams(id)
)
''')

# Assignments table
c.execute('''
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER,
    room_id INTEGER,
    faculty_id INTEGER,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(id)
)
''')

conn.commit()
conn.close()
print("Database with separate rooms initialized.")
