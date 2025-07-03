
# 🗂️ Invigilation Duty Scheduler

A Flask-based web application that automates invigilation duty scheduling for academic institutions. It helps administrators assign faculty members to exam rooms fairly and efficiently, with CSV export and schedule management features.

---

## ✅ Features

- 👨‍🏫 Add Faculty (Name & Department)
- 📝 Add Exams (with date, session, and multiple rooms)
- ⚖️ Auto Assign Duties (ensures no faculty is assigned more than once per session)
- 📅 View Invigilation Schedule
- ⚠️ View Unassigned Rooms (if faculty are insufficient)
- 📤 Export Schedule and Unassigned Rooms to CSV
- ♻️ Reset/Delete All Assignments
- 🎨 Simple and responsive UI (CSS integrated)

---

## 💻 Tech Stack

| Layer         | Tech        |
|---------------|-------------|
| Backend       | Python, Flask |
| Frontend      | HTML, CSS (Jinja2 Templates) |
| Database      | SQLite      |
| Export        | CSV         |

---

## 📁 Folder Structure

```
invigilation_scheduler/
├── app.py                   # Main Flask app logic
├── init_db.py               # Script to initialize the SQLite database
├── scheduler.db             # Database (auto-created)
│
├── templates/               # HTML pages
│   ├── index.html
│   ├── add_faculty.html
│   ├── add_exam.html
│   ├── view_schedule.html
│   └── unassigned.html
│
├── static/
│   └── style.css            # Stylesheet
│
└── README.md                # Project description
```

---

## 🚀 How to Run

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/invigilation_scheduler.git
cd invigilation_scheduler
```

2. **Create a Virtual Environment (optional but recommended)**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
```

3. **Install Dependencies**

```bash
pip install flask
```

4. **Initialize the Database**

```bash
python init_db.py
```

5. **Run the App**

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 📤 Exports

- `Export Schedule` – Full CSV of faculty-duty assignments
- `Export Unassigned` – Rooms not assigned due to insufficient faculty

---

## 🧠 Future Improvements

- Admin login authentication
- Faculty unavailability tracking
- Improved conflict checking (e.g. back-to-back sessions)
- Deployment on platforms like Heroku or Render

---

## 📜 License

This project is free to use under the MIT License.

---

## 🙌 Acknowledgments

Thanks to Flask, SQLite, and the open-source Python ecosystem ❤️
