from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

statistics_blueprint = Blueprint("statistics", __name__)

@statistics_blueprint.route("/statistics", methods=['POST', 'GET'])
def statistics():
    if session.get("role") != "Administrator":
        return redirect(url_for("account.unauthorized"))

    cursor = dbserver.cursor()

    # Gets department name and the number of students in the department
    cursor.execute("""
    SELECT department_name,
        (
            SELECT COUNT(*)
            FROM student
            WHERE student.department_ID = department.department_ID
        ) AS student_count
    FROM department;
    """)
    student_count = cursor.fetchall()

    # Gets lists of classes with and without students
    has_students = []
    no_students  = []
    for student in student_count:
        if student[1] != 0:
            has_students.append([student[0], student[1]])
        else:
            no_students.append(student[0])

    cursor.close()
    
    return render_template(
            'statistics.html',
            student_count=student_count,
            has_students=has_students,
            no_students=no_students
            )

