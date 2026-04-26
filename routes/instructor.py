from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

instructor_blueprint = Blueprint("instructor", __name__)

@instructor_blueprint.route("/edit_instructor", methods=["GET", "POST"])
def edit_instructor():
    # Keep this page restricted to administrators.
    if session.get("role") != "Administrator":
        return redirect(url_for("account.unauthorized"))

    cursor = dbserver.cursor()

    if request.method == "POST":
        # handles all form actions
        action = (request.form.get("action") or "").strip().lower()

        if action == "create":
            first_name = (request.form.get("first_name") or "").strip()
            last_name = (request.form.get("last_name") or "").strip()
            department_name = (request.form.get("department_name") or "").strip()
            salary = (request.form.get("salary") or "0").strip()

            cursor.execute("CALL create_instructor(%s, %s, %s, %s)",
                (first_name, last_name, department_name, salary))
            
            dbserver.commit()

        elif action == "update":
            instructor_id = (request.form.get("instructor_id") or "").strip()
            first_name = (request.form.get("first_name") or "").strip()
            last_name = (request.form.get("last_name") or "").strip()
            department_name = (request.form.get("department_name") or "").strip()
            salary = (request.form.get("salary") or "0").strip()

            # update_student uses advisor_ID
            cursor.execute("CALL update_instructor(%s, %s, %s, %s, %s)",
                (instructor_id, first_name, last_name, department_name, salary))
            
            dbserver.commit()

        elif action == "delete":
            instructor_id = (request.form.get("instructor_id") or "").strip()
            cursor.execute("CALL delete_instructor(%s)", (instructor_id,))
            dbserver.commit()

        # Redirect after POST to avoid duplicate form submissions on refresh
        cursor.close()
        return redirect(url_for("instructor.edit_instructor"))

    # Load current data for dropdowns/table rendering.
    cursor.execute(
        """
        SELECT i.instructor_ID, i.first_name, i.last_name, d.department_name, i.salary
        FROM instructor i
        LEFT JOIN department d ON d.department_ID = i.department_ID
        ORDER BY i.instructor_ID
        """
    )
    instructors = cursor.fetchall()

    cursor.execute(
        "SELECT department_ID, department_name FROM department ORDER BY department_name"
    )
    departments = cursor.fetchall()

    cursor.close()

    return render_template("edit_instructor.html", instructors=instructors, departments=departments)

#INSTRUCTOR STUFF
#--------------------------------------------------------------
#Instructor Grade Updating
@instructor_blueprint.route("/instructorGrades", methods=['POST', 'GET'])
def instructorGrades():
    Id = session.get("userID")
    print(Id)
    if request.method == 'GET':
        #Pull all taught sections and grades
        cursor = dbserver.cursor()

        cursor.execute(
            """
            SELECT n.first_name, n.last_name, k.grades, c.title, s.semester, s.year, k.section_ID, k.student_ID
            FROM teaches t
            JOIN section s ON s.section_ID = t.section_ID
            JOIN course c ON s.course_ID = c.course_ID
            LEFT JOIN takes k ON k.section_ID = s.section_ID
            LEFT JOIN student n ON n.student_ID = k.student_ID
            WHERE t.instructor_ID = %s
            """
            , [Id])
        rows = cursor.fetchall()

        sections = {}

        #Formats Data nicely to pass to page
        for first, last, grade, title, semester, year, section_ID, student_ID in rows:
            if section_ID not in sections:
                sections[section_ID] = {
                    "section_ID": section_ID,
                    "course": title,
                    "semester": semester,
                    "year": year,
                    "students": []
                }

            sections[section_ID]["students"].append({
                "student_ID": student_ID,
                "first_name": first,
                "last_name": last,
                "grade": grade
            })
        cursor.close()
        return render_template("instructorGrades.html", sections=sections)

    if request.method =='POST':
        cursor = dbserver.cursor()
        section_ID = request.form['section_ID']
        student_ID = request.form['student_ID']
        newGrade = request.form['newGrade']

        cursor.execute("""
            UPDATE takes t 
            SET t.grades = %s 
            WHERE t.student_ID = %s AND t.section_ID = %s 
""",[newGrade, student_ID, section_ID])
        dbserver.commit()
        cursor.close()
        return redirect(url_for('instructor.instructorGrades'))
