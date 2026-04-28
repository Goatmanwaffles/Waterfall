from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

advisor_blueprint = Blueprint("advisor", __name__)

#INSTRUCTOR ADVISING MODIFIER
@advisor_blueprint.route("/advisingRoster", methods=['POST','GET'])
def modifyAdvisingRoster():
    if (
            session.get("role") != "Instructor" and
            session.get("role") != "Administrator"
        ):
        return redirect(url_for("account.unauthorized"))

    if request.method == 'GET':
        cursor = dbserver.cursor()
        cursor.execute("SELECT s.student_ID, s.first_name, s.last_name, d.first_name, d.last_name, d.instructor_ID from student s LEFT JOIN advises a ON s.student_ID = a.student_ID LEFT JOIN instructor d ON d.instructor_ID = a.instructor_ID")
        studentsRows = cursor.fetchall()
        cursor.execute("SELECT instructor_ID, first_name, last_name, department_ID from instructor")
        advisorsRows = cursor.fetchall()

        students = {}
        advisors = {}
        for studentID, first, last, advisorFirst, advisorLast, advisorID in studentsRows:
            if studentID not in students:
                students[studentID] = {
                    "studentID": studentID,
                    "firstName": first,
                    "lastName": last,
                    "advisorFirst": advisorFirst,
                    "advisorLast": advisorLast,
                    "advisorID": advisorID
                }

        for advisorID, first, last, dept in advisorsRows:
            if advisorID not in advisors:
                advisors[advisorID] = {
                    "advisorID": advisorID,
                    "firstName": first,
                    "lastName": last,
                    "department": dept
                }
        cursor.close()
        return render_template("editAdvisingRoster.html", students=students, advisors=advisors)

    if request.method == 'POST':
        action = (request.form.get("action") or "").strip().lower()

        if action == "reassign":
            #Update Advisor
            student = request.form['student']
            newAdvisor = request.form['newAdvisor']
            cursor = dbserver.cursor()
            cursor.execute("INSERT INTO advises (student_ID, instructor_ID) VALUES (%s, %s) ON DUPLICATE KEY UPDATE instructor_ID = %s;", [student, newAdvisor, newAdvisor])
            cursor.execute("UPDATE student SET advisor_ID = %s WHERE student_ID = %s", [newAdvisor, student])
            dbserver.commit()
            cursor.close()
            return redirect(url_for("advisor.modifyAdvisingRoster"))
        
        elif action == "delete":
            advisorToDelete = request.form['advisorToRemove']
            student = request.form['student']
            cursor = dbserver.cursor()
            cursor.execute("UPDATE student set advisor_ID = NULL WHERE student_ID = %s",[student])
            cursor.execute("DELETE FROM advises WHERE student_ID = %s AND instructor_ID = %s", [student, advisorToDelete])
            dbserver.commit()
            cursor.close()
            return redirect(url_for("advisor.modifyAdvisingRoster"))

#STUDENT CHECK ADVISOR
@advisor_blueprint.route("/advisorInfo", methods=['GET'])
def getAdvisorInfo():
    student_ID = session.get("userID")
    print(student_ID)
    cursor = dbserver.cursor()
    cursor.execute("SELECT a2.first_name, a2.last_name, d.department_name FROM advises a JOIN instructor a2 ON a.instructor_ID = a2.instructor_ID JOIN department d ON d.department_ID = a2.department_ID WHERE a.student_ID = %s",[student_ID])
    advisor = cursor.fetchone()
    cursor.close()
    return render_template("studentAdvisor.html", advisor=advisor)

