from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-very-secret-key-123'  # Add this line
DATABASE = 'scheduler.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/add_exam', methods=['GET', 'POST'])
@app.route('/add_exam', methods=['GET', 'POST'])
def add_exam():
    if request.method == 'POST':
        date = request.form['date']
        session = request.form['session']
        rooms = request.form['rooms']  # comma-separated

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO exams (date, session) VALUES (?, ?)", (date, session))
        exam_id = cursor.lastrowid

        for room in rooms.split(','):
            cursor.execute("INSERT INTO rooms (exam_id, room_no) VALUES (?, ?)", (exam_id, room.strip()))
        
        db.commit()
        return redirect('/')
    return render_template('add_exam.html')


@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        db = get_db()
        db.execute("INSERT INTO faculty (name, department) VALUES (?, ?)", (name, department))
        db.commit()
        return "Faculty added successfully!"
    return render_template('add_faculty.html')
@app.route('/reset_schedule')
def reset_schedule():
    db = get_db()
    db.execute("DELETE FROM assignments")
    db.commit()
    return '''
        <p style="color:green;">All assignments have been cleared successfully.</p>
        <a href="/">Back to Home</a>
    '''
from flask import session
import json

@app.route('/assign_duties')
def assign_duties():
    db = get_db()
    exams = db.execute("SELECT * FROM exams").fetchall()
    faculty = db.execute("SELECT * FROM faculty").fetchall()
    faculty_cycle = iter(faculty * 100)

    db.execute("DELETE FROM assignments")
    unassigned_rooms = []

    for exam in exams:
        exam_id = exam[0]
        exam_date = exam[1]
        session_name = exam[2]
        rooms = db.execute("SELECT * FROM rooms WHERE exam_id = ?", (exam_id,)).fetchall()

        for room in rooms:
            assigned = False
            attempts = 0

            while not assigned and attempts < len(faculty) * 2:
                fac = next(faculty_cycle)
                attempts += 1
                existing = db.execute('''
                    SELECT 1 FROM assignments a
                    JOIN exams e ON e.id = a.exam_id
                    WHERE a.faculty_id = ? AND e.date = ? AND e.session = ?
                ''', (fac[0], exam_date, session_name)).fetchone()

                if not existing:
                    db.execute("INSERT INTO assignments (exam_id, room_id, faculty_id) VALUES (?, ?, ?)",
                               (exam_id, room[0], fac[0]))
                    assigned = True

            if not assigned:
                unassigned_rooms.append((exam_date, session_name, room[2]))  # room[2] is room_no

    db.commit()
    # Save to session as JSON
    session['unassigned_rooms'] = json.dumps(unassigned_rooms)
    return render_template("unassigned.html", rooms=unassigned_rooms)

import csv
from flask import Response

@app.route('/export_unassigned')
def export_unassigned():
    unassigned = json.loads(session.get('unassigned_rooms', '[]'))

    if not unassigned:
        return "No unassigned rooms to export."

    def generate():
        yield 'Date,Session,Room\n'
        for row in unassigned:
            yield f"{row[0]},{row[1]},{row[2]}\n"

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=unassigned_rooms.csv"})


@app.route('/view_schedule')
def view_schedule():
    db = get_db()
    rows = db.execute('''
        SELECT exams.date, exams.session, rooms.room_no, faculty.name, faculty.department
        FROM assignments
        JOIN exams ON assignments.exam_id = exams.id
        JOIN rooms ON assignments.room_id = rooms.id
        JOIN faculty ON assignments.faculty_id = faculty.id
        ORDER BY exams.date, exams.session
    ''').fetchall()
    return render_template('view_schedule.html', rows=rows)


import csv
from flask import Response

@app.route('/export_schedule')
def export_schedule():
    db = get_db()
    query = '''
        SELECT exams.date, exams.session, faculty.name, faculty.department
        FROM assignments
        JOIN exams ON assignments.exam_id = exams.id
        JOIN faculty ON assignments.faculty_id = faculty.id
        ORDER BY exams.date, exams.session
    '''
    rows = db.execute(query).fetchall()

    def generate():
        data = [['Date', 'Session', 'Faculty Name', 'Department']]
        data += rows
        for row in data:
            yield ','.join(map(str, row)) + '\n'

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=invigilation_schedule.csv"})

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
