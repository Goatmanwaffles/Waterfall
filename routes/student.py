from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from setup import dbserver
import bcrypt
from routes.semester import getYear, getSemester

student_blueprint = Blueprint("student", __name__)

@student_blueprint.route("/checkCourses", methods=['POST', 'GET'])
def checkCourses():
    student_ID = session.get("userID")

    #Initial Load to fetch semesters student is enrolled in
    if request.method == 'GET':
        cursor = dbserver.cursor()

        cursor.execute("SELECT DISTINCT s.semester, s.year FROM takes t JOIN section s on t.section_ID = s.section_ID WHERE t.student_ID = %s",[student_ID])
        semesters = cursor.fetchall()
        print (semesters)
        cursor.close()
        return render_template("checkCourses.html", semesters=semesters)

    if request.method == 'POST':
        semesterYear = request.form['semester']
        if semesterYear == "":
            return redirect(url_for("student.checkCourses()"))
        semester, year = semesterYear.split(',')

        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, t.grades FROM takes t JOIN section s ON t.section_ID = s.section_ID JOIN course c on c.course_ID = s.course_ID WHERE t.student_ID = %s AND s.semester = %s AND s.year = %s ",[student_ID, semester, year])
        courses = cursor.fetchall()

        cursor.close()
        return render_template("checkCoursesResults.html", courses=courses)
    

# Student Search
@student_blueprint.route("/student_search", methods=["GET", "POST"])
@student_blueprint.route("/student_search/<string:id>", methods=["GET", "POST"])
def student_search(id="", first="", last=""):
    
    if request.method == "POST":
        id    = request.form.get("id")
        first = request.form.get("first")
        last  = request.form.get("last")

    # Gets list of all students
    all_stu = ""
    cursor = dbserver.cursor()
    sql = "SELECT * FROM student"
    cursor.execute(sql)
    all_stu = cursor.fetchall()

    # Converts Department ID into Department Name
    students = []
    sql = "SELECT department_name FROM department WHERE department_ID = %s"
    for y in range(len(all_stu)):
        one_student = []
        
        # All variables used in search
        checks = [
            [ id,    all_stu[y][0] ],
            [ first, all_stu[y][1] ],
            [ last,  all_stu[y][2] ]
        ]

        # Lowercases all variables and turns them into strings
        for c_y in range(len(checks)):
            for c_x in range(len(checks[0])):
                checks[c_y][c_x] = str(checks[c_y][c_x]).lower()
        
        # If the variable isn't empty and the student doesn't have it, skip
        present = True
        for var in checks:
            if var[0] != "" and var[0] not in var[1]:
                present = False
        
        if present == False: 
            continue

        # Iterates through all students
        for x in range(len(all_stu[0])):

            # Gets default data
            data = all_stu[y][x]

            # If we are in the department ID column
            if x == 3:
                # The department ID
                department_ID = all_stu[y][x]
                # Gets name equal to the ID
                cursor.execute(sql, [department_ID])
                # Gets the first result
                data = cursor.fetchone()[0]

            # Removes the Advisor ID column
            elif x == 5:
                continue
            
            # Adds the modified data
            one_student.append(data)
        students.append(one_student)
    cursor.close()
    return render_template(
        "student_search.html",
        students=students,
        id=id,
        first=first,
        last=last
    )

@student_blueprint.route("/edit_student", methods=["GET", "POST"])
def edit_student():
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
            total_cred = (request.form.get("total_cred") or "0").strip()
            advisor_id = (request.form.get("advisor_id") or "").strip()
            username = (request.form.get("username") or "").strip()
            password = (request.form.get("password") or "").strip()

            cursor.execute("""
                SELECT username FROM account WHERE username = %s
            """, [username])
           
            userExists = cursor.fetchone()
            if userExists:
                flash("Username already taken", "error")
                return redirect(url_for("student.edit_student"))

            password_bytes = password.encode('utf-8')
            s = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, s)

            advisor_id_value = int(advisor_id) if advisor_id else None

            cursor.execute("CALL create_student(%s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, department_name, total_cred, advisor_id_value, username, hashed))
            
            
            
            dbserver.commit()

        elif action == "update":
            student_id = (request.form.get("student_id") or "").strip()
            first_name = (request.form.get("first_name") or "").strip()
            last_name = (request.form.get("last_name") or "").strip()
            department_name = (request.form.get("department_name") or "").strip()
            total_cred = (request.form.get("total_cred") or "0").strip()
            advisor_id = (request.form.get("advisor_id") or "").strip()

            advisor_id_value = int(advisor_id) if advisor_id else None

            # update_student uses advisor_ID
            cursor.execute("CALL update_student(%s, %s, %s, %s, %s, %s)",
                (student_id, first_name, last_name, department_name, total_cred, advisor_id_value))
            
            dbserver.commit()

        elif action == "delete":
            student_id = (request.form.get("student_id") or "").strip()

            cursor.execute("SELECT COUNT(*) FROM takes t WHERE t.student_ID = %s", [student_id])
            if cursor.fetchone()[0] > 0:
                flash("Cannot delete student - they still has active sections.", "error")
                return redirect(url_for("student.edit_student"))
            
            cursor.execute("CALL delete_student(%s)", (student_id,))
            dbserver.commit()

        # Redirect after POST to avoid duplicate form submissions on refresh
        cursor.close()
        return redirect(url_for("student.edit_student"))

    # Load current data for dropdowns/table rendering.
    cursor.execute(
        """
        SELECT s.student_ID, s.first_name, s.last_name, d.department_name, s.total_cred, i.instructor_ID, CONCAT(i.first_name, ' ', i.last_name)
        FROM student s
        LEFT JOIN department d ON d.department_ID = s.department_ID
        LEFT JOIN advises a ON a.student_ID = s.student_ID
        LEFT JOIN instructor i ON i.instructor_ID = a.instructor_ID
        ORDER BY s.student_ID
        """
    )
    students = cursor.fetchall()

    cursor.execute(
        "SELECT department_ID, department_name FROM department ORDER BY department_name"
    )
    departments = cursor.fetchall()

    cursor.execute(
        """
        SELECT i.instructor_ID, i.first_name, i.last_name, d.department_name
        FROM instructor i
        LEFT JOIN department d ON d.department_ID = i.department_ID
        ORDER BY i.instructor_ID
        """
    )
    advisors = cursor.fetchall()

    cursor.close()

    return render_template("edit_student.html", students=students, departments=departments, advisors=advisors)


#STUDENT CHECK FINAL GRADES
#Probably should filter to only before this semester AKA final grades
@student_blueprint.route("/finalGrades", methods=['GET'])
def getFinalGrades():
    student_ID = session.get("userID")
    cursor = dbserver.cursor()
    year = getYear()
    cursor.execute("SELECT c.title, t.grades, s.semester, s.year FROM takes t JOIN section s ON t.section_ID = s.section_ID JOIN course c on c.course_ID = s.course_ID WHERE t.student_ID = %s AND s.year < %s AND t.grades != ''", [student_ID, year])
    grades = cursor.fetchall()
    cursor.close()
    return render_template("finalGrades.html", grades=grades)


#Check section information
@student_blueprint.route("/currentSchedule", methods=['GET'])
def getSectionInfo():
    student_ID = session.get("userID")
    cursor = dbserver.cursor()
    cursor.execute("SELECT s.section_ID, c.title, s.semester, s.year, i.first_name, i.last_name, b.building_name, ti.day, ti.start_hr, ti.start_min, ti.end_hr, ti.end_min FROM takes t JOIN section s ON s.section_ID = t.section_ID LEFT JOIN building b ON b.building_ID = s.building_ID JOIN course c ON c.course_ID = s.course_ID JOIN teaches th ON th.section_ID = s.section_ID JOIN instructor i ON i.instructor_ID = th.instructor_ID join time_slot ti ON ti.time_slot_ID = s.time_slot_ID WHERE t.student_ID = %s", [student_ID])
    rows = cursor.fetchall()
    classes = {}

    for section_ID, title, semester, year, first, last, building, day, sthr, stmn, endhr, endmin in rows:
        classes[section_ID]={
            "class": title,
            "semester": semester,
            "year": year,
            "name": f"{first} {last}",
            "building": building,
            "timeslot": f"{day} - {sthr}:{stmn} - {endhr}:{endmin}" 
        }
    
    return render_template("schedule.html", classes=classes)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
