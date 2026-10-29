from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DATABASE = "students.db"


def initialize_database():
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                education TEXT NOT NULL,
                year TEXT NOT NULL,
                subjects TEXT NOT NULL,
                skills TEXT NOT NULL,
                goal TEXT NOT NULL
            )
        """)


def recommend(goal, skills):
    goal = goal.lower()
    skills_lower = skills.lower()

    if "data scientist" in goal or "data analyst" in goal:
        roadmap = [
            ("Python", "https://www.python.org/about/gettingstarted/"),
            ("SQL", "https://sqlbolt.com/"),
            ("Statistics and probability", "https://www.khanacademy.org/math/statistics-probability"),
            ("Pandas and data visualization", "https://pandas.pydata.org/docs/getting_started/"),
            ("Machine learning", "https://scikit-learn.org/stable/tutorial/"),
            ("Project: Sales data analysis", "https://www.kaggle.com/datasets")
        ]

    elif "software developer" in goal:
        roadmap = [
            ("Programming fundamentals", "https://www.w3schools.com/"),
            ("Data structures and algorithms", "https://www.geeksforgeeks.org/"),
            ("Object-oriented programming", "https://docs.python.org/3/tutorial/"),
            ("Databases and SQL", "https://sqlbolt.com/"),
            ("Project: Build a student management app", "https://developer.mozilla.org/")
        ]

    elif "cybersecurity" in goal:
        roadmap = [
            ("Computer networking", "https://www.cisco.com/"),
            ("Linux basics", "https://ubuntu.com/tutorials"),
            ("Cybersecurity fundamentals", "https://www.netacad.com/"),
            ("Security practice labs", "https://tryhackme.com/"),
            ("Project: Basic security awareness analysis", "https://www.cisa.gov/")
        ]

    elif "web developer" in goal:
        roadmap = [
            ("HTML", "https://developer.mozilla.org/en-US/docs/Web/HTML"),
            ("CSS", "https://developer.mozilla.org/en-US/docs/Web/CSS"),
            ("JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
            ("Backend and databases", "https://flask.palletsprojects.com/"),
            ("Project: Create a portfolio website", "https://github.com/")
        ]

    else:
        roadmap = [
            ("Learn programming fundamentals", "https://www.w3schools.com/"),
            ("Improve communication skills", "https://www.britishcouncil.org/"),
            ("Explore courses in your career field", "https://www.coursera.org/"),
            ("Build a practical project", "https://github.com/"),
            ("Prepare a resume and portfolio", "https://www.linkedin.com/")
        ]

    skill_list = [
        item.strip() for item in skills_lower.split(",") if item.strip()
    ]

    missing = []
    if not any("python" in skill for skill in skill_list):
        missing.append("Python")
    if not any("sql" in skill for skill in skill_list):
        missing.append("SQL")
    if not any("communication" in skill for skill in skill_list):
        missing.append("Communication")

    return roadmap, missing


@app.route("/", methods=["GET", "POST"])
def dashboard():
    profile = None
    roadmap = []
    missing = []

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        education = request.form.get("education", "").strip()
        year = request.form.get("year", "").strip()
        subjects = request.form.get("subjects", "").strip()
        skills = request.form.get("skills", "").strip()
        goal = request.form.get("goal", "").strip()

        if all([name, education, year, subjects, skills, goal]):
            with sqlite3.connect(DATABASE) as connection:
                cursor = connection.execute("""
                    INSERT INTO students
                    (name, education, year, subjects, skills, goal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, education, year, subjects, skills, goal))
                student_id = cursor.lastrowid

            profile = {
                "id": student_id,
                "name": name,
                "education": education,
                "year": year,
                "subjects": subjects,
                "skills": skills,
                "goal": goal
            }

            roadmap, missing = recommend(goal, skills)

            return render_template(
                "dashboard.html",
                profile=profile,
                roadmap=roadmap,
                missing=missing
            )

    return render_template(
        "dashboard.html",
        profile=profile,
        roadmap=roadmap,
        missing=missing
    )


@app.route("/profiles")
def profiles():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        students = connection.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    return render_template("dashboard.html", students=students)


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
