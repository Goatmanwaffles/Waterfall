from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from setup import makeDatabase, runSQL, generateSeedData, resetDatabase, dbserver
from flask_session import Session
import config
import pymysql
import bcrypt
import json
from routes import loadBlueprints

app = Flask(__name__)

# This code will reset the database on run
resetDatabase()
dbserver.select_db(config.DB_NAME)

cursor = dbserver.cursor()

app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files

# Initialize Flask-Session
Session(app)

loadBlueprints(app)

@app.route("/dashboard")
def dash():
    #Get User auth level
    role = session.get("role")
    return render_template("dash.html", role=role)

@app.route("/profile", methods=['POST', 'GET'])
def profile():
    return render_template(
        "profile.html",
        first_name="bob",
        last_name="LSbob"
    )

@app.route("/edit_teaches", methods=["GET", "POST"])
def edit_teaches():
    if session.get("role") != "Administrator":
        return redirect(url_for("unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            instructor_id = (request.form.get("instructor_id") or "").strip()
            section_id = (request.form.get("section_id") or "").strip()

            cursor.execute(
                "INSERT INTO teaches (instructor_ID, section_ID) VALUES (%s, %s)",
                (instructor_id, section_id),
            )
            dbserver.commit()

        elif action == "update":
            old_instructor_id = (request.form.get("old_instructor_id") or "").strip()
            old_section_id = (request.form.get("old_section_id") or "").strip()
            instructor_id = (request.form.get("instructor_id") or "").strip()
            section_id = (request.form.get("section_id") or "").strip()

            cursor.execute(
                """
                UPDATE teaches
                SET instructor_ID = %s,
                    section_ID = %s
                WHERE instructor_ID = %s
                    AND section_ID = %s
                """,
                (instructor_id, section_id, old_instructor_id, old_section_id),
            )
            dbserver.commit()

        elif action == "delete":
            instructor_id = (request.form.get("instructor_id") or "").strip()
            section_id = (request.form.get("section_id") or "").strip()

            cursor.execute(
                "DELETE FROM teaches WHERE instructor_ID = %s AND section_ID = %s",
                (instructor_id, section_id),
            )
            dbserver.commit()

        cursor.close()
        return redirect(url_for("edit_teaches"))

    cursor.execute(
        """
        SELECT
            t.instructor_ID,
            i.first_name,
            i.last_name,
            t.section_ID,
            s.course_ID,
            c.title,
            s.semester,
            s.year
        FROM teaches t
        LEFT JOIN instructor i ON i.instructor_ID = t.instructor_ID
        LEFT JOIN section s ON s.section_ID = t.section_ID
        LEFT JOIN course c ON c.course_ID = s.course_ID
        ORDER BY t.instructor_ID, t.section_ID
        """
    )
    teaches_rows = cursor.fetchall()

    cursor.execute(
        """
        SELECT instructor_ID, first_name, last_name
        FROM instructor
        ORDER BY instructor_ID
        """
    )
    instructors = cursor.fetchall()

    cursor.execute(
        """
        SELECT s.section_ID, s.course_ID, c.title, s.semester, s.year
        FROM section s
        LEFT JOIN course c ON c.course_ID = s.course_ID
        ORDER BY s.section_ID
        """
    )
    sections = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_teaches.html",
        teaches_rows=teaches_rows,
        instructors=instructors,
        sections=sections,
    )

#STUDENT CHECK FINAL GRADES
#Probably should filter to only before this semester AKA final grades
@app.route("/finalGrades", methods=['GET'])
def getFinalGrades():
    student_ID = session.get("userID")
    cursor = dbserver.cursor()
    cursor.execute("SELECT c.title, t.grades FROM takes t JOIN section s ON t.section_ID = s.section_ID JOIN course c on c.course_ID = s.course_ID WHERE t.student_ID = %s AND s.year < 2026 AND t.grades != ''", [student_ID])
    grades = cursor.fetchall()
    cursor.close()
    return render_template("finalGrades.html", grades=grades)

#STUDENT CHECK ADVISOR
@app.route("/advisorInfo", methods=['GET'])
def getAdvisorInfo():
    student_ID = session.get("userID")
    print(student_ID)
    cursor = dbserver.cursor()
    cursor.execute("SELECT a2.first_name, a2.last_name, d.department_name FROM advises a JOIN advisor a2 ON a.advisor_ID = a2.advisor_ID JOIN department d ON d.department_ID = a2.department_ID WHERE a.student_ID = %s",[student_ID])
    advisor = cursor.fetchone()
    cursor.close()
    return render_template("studentAdvisor.html", advisor=advisor)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
