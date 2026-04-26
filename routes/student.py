from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver

student_blueprint = Blueprint("student", __name__)

@student_blueprint.route("/checkCourses", methods=['POST', 'GET'])
def checkStudentCourses():
    student_ID = session.get("userID")

    #Initial Load to fetch semesters student is enrolled in
    if request.method == 'GET':
        cursor = dbserver.cursor()

        cursor.execute("SELECT s.semester, s.year FROM takes t JOIN section s on t.section_ID = s.section_ID WHERE t.student_ID = %s",[student_ID])
        semesters = cursor.fetchall()

        cursor.close()
        return render_template("checkCourses.html", semesters=semesters)

    if request.method == 'POST':
        semesterYear = request.form['semester']
        semester, year = semesterYear.split(',')


        #IDK WHAT THE RUBRIC MEANS BY STATUS

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
        return redirect(url_for("unauthorized"))

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

            advisor_first_name = ""
            advisor_last_name = ""
            advisor_department_name = ""

            # create_student uses advisor name and advisor department
            if advisor_id:
                cursor.execute(
                    """
                    SELECT a.first_name, a.last_name, d.department_name
                    FROM advisor a
                    JOIN department d ON d.department_ID = a.department_ID
                    WHERE a.advisor_ID = %s
                    """,
                    (advisor_id,),
                )
                advisor_row = cursor.fetchone()
                if advisor_row:
                    advisor_first_name = advisor_row[0]
                    advisor_last_name = advisor_row[1]
                    advisor_department_name = advisor_row[2]

            cursor.execute("CALL create_student(%s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, department_name, total_cred, advisor_first_name, advisor_last_name, advisor_department_name))
            
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
            cursor.execute("CALL delete_student(%s)", (student_id,))
            dbserver.commit()

        # Redirect after POST to avoid duplicate form submissions on refresh
        cursor.close()
        return redirect(url_for("edit_student"))

    # Load current data for dropdowns/table rendering.
    cursor.execute(
        """
        SELECT s.student_ID, s.first_name, s.last_name, d.department_name, s.total_cred, a.advisor_ID, CONCAT(a.first_name, ' ', a.last_name)
        FROM student s
        LEFT JOIN department d ON d.department_ID = s.department_ID
        LEFT JOIN advisor a ON a.advisor_ID = s.advisor_ID
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
        SELECT a.advisor_ID, a.first_name, a.last_name, d.department_name
        FROM advisor a
        LEFT JOIN department d ON d.department_ID = a.department_ID
        ORDER BY a.advisor_ID
        """
    )
    advisors = cursor.fetchall()

    cursor.close()

    return render_template("edit_student.html", students=students, departments=departments, advisors=advisors)

