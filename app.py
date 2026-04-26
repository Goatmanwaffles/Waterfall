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
        
@app.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")


@app.route("/edit_section", methods=["GET", "POST"])
def edit_section():
    if session.get("role") != "Administrator":
        return redirect(url_for("unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            course_id = (request.form.get("course_id") or "").strip()
            semester = (request.form.get("semester") or "").strip()
            year = (request.form.get("year") or "0").strip()
            building_id = (request.form.get("building_id") or "").strip()
            time_slot_id = (request.form.get("time_slot_id") or "").strip()

            cursor.execute(
                "CALL create_section(%s, %s, %s, %s, %s)",
                (course_id, semester, year, building_id, time_slot_id),
            )
            dbserver.commit()

        elif action == "update":
            section_id = (request.form.get("section_id") or "").strip()
            course_id = (request.form.get("course_id") or "").strip()
            semester = (request.form.get("semester") or "").strip()
            year = (request.form.get("year") or "0").strip()
            building_id = (request.form.get("building_id") or "").strip()
            time_slot_id = (request.form.get("time_slot_id") or "").strip()

            cursor.execute(
                "CALL update_section(%s, %s, %s, %s, %s, %s)",
                (section_id, course_id, semester, year, building_id, time_slot_id),
            )
            dbserver.commit()

        elif action == "delete":
            section_id = (request.form.get("section_id") or "").strip()
            course_id = (request.form.get("course_id") or "").strip()
            semester = (request.form.get("semester") or "").strip()
            year = (request.form.get("year") or "0").strip()

            cursor.execute(
                "CALL delete_section(%s, %s, %s, %s)",
                (course_id, section_id, semester, year),
            )
            dbserver.commit()

        cursor.close()
        return redirect(url_for("edit_section"))

    cursor.execute(
        """
        SELECT
            s.section_ID,
            s.course_ID,
            c.title,
            s.semester,
            s.year,
            s.building_ID,
            b.building_name,
            s.time_slot_ID
        FROM section s
        LEFT JOIN course c ON c.course_ID = s.course_ID
        LEFT JOIN building b ON b.building_ID = s.building_ID
        ORDER BY s.section_ID
        """
    )
    sections = cursor.fetchall()

    cursor.execute("SELECT course_ID, title FROM course ORDER BY course_ID")
    courses = cursor.fetchall()

    cursor.execute("SELECT building_ID, building_name FROM building ORDER BY building_ID")
    buildings = cursor.fetchall()

    cursor.execute(
        """
        SELECT time_slot_ID, day, start_hr, start_min, end_hr, end_min
        FROM time_slot
        ORDER BY time_slot_ID
        """
    )
    time_slots = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_section.html",
        sections=sections,
        courses=courses,
        buildings=buildings,
        time_slots=time_slots,
    )

@app.route("/edit_course", methods=["GET", "POST"])
def edit_course():
    if session.get("role") != "Administrator":
        return redirect(url_for("unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            title = (request.form.get("title") or "").strip()
            department_id = (request.form.get("department_id") or "").strip()
            credits = (request.form.get("credits") or "0").strip()

            cursor.execute(
                "INSERT INTO course (title, department_ID, credits) VALUES (%s, %s, %s)",
                (title, department_id, credits),
            )
            dbserver.commit()

        elif action == "update":
            course_id = (request.form.get("course_id") or "").strip()
            title = (request.form.get("title") or "").strip()
            department_id = (request.form.get("department_id") or "").strip()
            credits = (request.form.get("credits") or "0").strip()

            cursor.execute(
                """
                UPDATE course
                SET title = %s,
                    department_ID = %s,
                    credits = %s
                WHERE course_ID = %s
                """,
                (title, department_id, credits, course_id),
            )
            dbserver.commit()

        elif action == "delete":
            course_id = (request.form.get("course_id") or "").strip()
            cursor.execute("DELETE FROM course WHERE course_ID = %s", (course_id,))
            dbserver.commit()

        cursor.close()
        return redirect(url_for("edit_course"))

    cursor.execute(
        """
        SELECT
            c.course_ID,
            c.title,
            d.department_name,
            c.credits
        FROM course c
        LEFT JOIN department d ON d.department_ID = c.department_ID
        ORDER BY c.course_ID
        """
    )
    courses = cursor.fetchall()

    cursor.execute(
        "SELECT department_ID, department_name FROM department ORDER BY department_name"
    )
    departments = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_course.html",
        courses=courses,
        departments=departments,
    )

@app.route("/edit_classroom", methods=["GET", "POST"])
def edit_classroom():
    if session.get("role") != "Administrator":
        return redirect(url_for("unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            building_id = (request.form.get("building_id") or "").strip()
            room_number = (request.form.get("room_number") or "0").strip()
            capacity = (request.form.get("capacity") or "0").strip()

            cursor.execute(
                "INSERT INTO classroom (building_ID, room_number, capacity) VALUES (%s, %s, %s)",
                (building_id, room_number, capacity),
            )
            dbserver.commit()

        elif action == "update":
            classroom_id = (request.form.get("classroom_id") or "").strip()
            building_id = (request.form.get("building_id") or "").strip()
            room_number = (request.form.get("room_number") or "0").strip()
            capacity = (request.form.get("capacity") or "0").strip()

            cursor.execute(
                """
                UPDATE classroom
                SET building_ID = %s,
                    room_number = %s,
                    capacity = %s
                WHERE classroom_ID = %s
                """,
                (building_id, room_number, capacity, classroom_id),
            )
            dbserver.commit()

        elif action == "delete":
            classroom_id = (request.form.get("classroom_id") or "").strip()
            cursor.execute("DELETE FROM classroom WHERE classroom_ID = %s", (classroom_id,))
            dbserver.commit()

        cursor.close()
        return redirect(url_for("edit_classroom"))

    cursor.execute(
        """
        SELECT
            c.classroom_ID,
            c.building_ID,
            b.building_name,
            c.room_number,
            c.capacity
        FROM classroom c
        LEFT JOIN building b ON b.building_ID = c.building_ID
        ORDER BY c.classroom_ID
        """
    )
    classrooms = cursor.fetchall()

    cursor.execute("SELECT building_ID, building_name FROM building ORDER BY building_ID")
    buildings = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_classroom.html",
        classrooms=classrooms,
        buildings=buildings,
    )

@app.route("/edit_time_slot", methods=["GET", "POST"])
def edit_time_slot():
    if session.get("role") != "Administrator":
        return redirect(url_for("unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            day = (request.form.get("day") or "").strip()
            start_hr = (request.form.get("start_hr") or "0").strip()
            start_min = (request.form.get("start_min") or "0").strip()
            end_hr = (request.form.get("end_hr") or "0").strip()
            end_min = (request.form.get("end_min") or "0").strip()

            cursor.execute(
                """
                INSERT INTO time_slot (day, start_hr, start_min, end_hr, end_min)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (day, start_hr, start_min, end_hr, end_min),
            )
            dbserver.commit()

        elif action == "update":
            time_slot_id = (request.form.get("time_slot_id") or "").strip()
            day = (request.form.get("day") or "").strip()
            start_hr = (request.form.get("start_hr") or "0").strip()
            start_min = (request.form.get("start_min") or "0").strip()
            end_hr = (request.form.get("end_hr") or "0").strip()
            end_min = (request.form.get("end_min") or "0").strip()

            cursor.execute(
                """
                UPDATE time_slot
                SET day = %s,
                    start_hr = %s,
                    start_min = %s,
                    end_hr = %s,
                    end_min = %s
                WHERE time_slot_ID = %s
                """,
                (day, start_hr, start_min, end_hr, end_min, time_slot_id),
            )
            dbserver.commit()

        elif action == "delete":
            time_slot_id = (request.form.get("time_slot_id") or "").strip()
            cursor.execute("DELETE FROM time_slot WHERE time_slot_ID = %s", (time_slot_id,))
            dbserver.commit()

        cursor.close()
        return redirect(url_for("edit_time_slot"))

    cursor.execute(
        """
        SELECT
            time_slot_ID,
            day,
            start_hr,
            start_min,
            end_hr,
            end_min
        FROM time_slot
        ORDER BY time_slot_ID
        """
    )
    time_slots = cursor.fetchall()

    cursor.close()

    return render_template(
        "edit_time_slot.html",
        time_slots=time_slots,
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
