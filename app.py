from flask import Flask, render_template, request, redirect, url_for, session
from setup import makeDatabase, runSQL, generateSeedData, resetDatabase
from flask_session import Session
import config
import pymysql
import bcrypt
import json

app = Flask(__name__)

# This code will reset the database on run
resetDatabase()

dbserver = pymysql.connect(
    host     = config.HOST,
    user     = config.USER,
    password = config.PASSWORD,
    database = config.DB_NAME
)

cursor = dbserver.cursor()

app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files

# Initialize Flask-Session
Session(app)


@app.route("/", methods=['POST', 'GET'])
def login():
    #Handle getting page
    if request.method == "GET":
        return render_template("login.html")
    #Handle Login
    if request.method == "POST":
        #Get username and password
        username = request.form['username']
        password= request.form['password']
        cursor = dbserver.cursor()
        cursor.execute("SELECT username, password, role, account_ID FROM account WHERE username = %s", (username))
        row = cursor.fetchone()

        #Convert password into bytes for check
        password = password.encode('utf-8')
        hashedPW = row[1].encode('utf-8')
        if not row or not (bcrypt.checkpw(password, hashedPW)):
            print("ERROR")
            return render_template("login.html", error="Invalid Username or Password")
        
        #Valid Login
        if row and (bcrypt.checkpw(password, hashedPW)):
            session["role"] = row[2] #Store role in session
            session["ID"] = row[3] #Store account ID
            return redirect(url_for('dash'))

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    #Handle Signup
    if request.method =="POST":
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if not username or not password or not confirmPassword:
            return render_template("signup.html", error="Missing Field")
        
        if password != confirmPassword:
            return render_template("signup.html", error="Passwords do not match")
        
        #Salt and Hash password
        password_bytes = password.encode('utf-8')
        s = bcrypt.gensalt()
        h = bcrypt.hashpw(password_bytes, s)

        cursor = dbserver.cursor()
        cursor.execute(f"CALL create_account(%s, %s, 'Student')", (username, h))
        cursor.close()
        dbserver.commit()

        return redirect(url_for('login'))

@app.route("/dashboard")
def dash():
    #Get User auth level
    role = session.get("role")
    print(role)
    return render_template("dash.html", role=role)

# Student Search
@app.route("/student_search", methods=["GET", "POST"])
@app.route("/student_search/<string:id>", methods=["GET", "POST"])
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

    return render_template(
        "student_search.html",
        students=students,
        id=id,
        first=first,
        last=last
    )

@app.route("/profile", methods=['POST', 'GET'])
def profile():
    return render_template(
        "profile.html",
        first_name="bob",
        last_name="LSbob"
    )


#Okay so this works, besides for matching the ID and cleaning it up, in concept it works though
#It creates a row in takes with no grade
#TO DO:
#More precise filtering on what classes it shows (Shold probobaly only show like next 2 or 3 semesters IDK)
#Get User ID working so we can get actual users to use this and not whoever student ID 1 is
@app.route("/register", methods=['POST', 'GET'])
def register():
    student_ID = "1"
    
    if request.method == 'GET':
        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, c.credits, s.semester, s.year, s.section_ID FROM section s JOIN course c on s.course_ID = c.course_ID WHERE s.year > 2025 AND NOT EXISTS (SELECT 1 FROM takes t WHERE t.section_ID = s.section_ID AND t.student_ID = %s)",[student_ID])
        sections = cursor.fetchall()
        cursor.close()
        return render_template("register.html", sections=sections)
    if request.method == 'POST':
        #WE NEED TO RELATE ACCOUNTS AND STUDENTS/OTHER PEOPLE FOR THIS TO WORK, RIGHT NOW THIS WHOLE THING IS A PROOF OF CONECPT THAT I CAN GET THIS TO WORK
        #-Logan
        #student_ID = session.get("ID")
        
        sec_ID = request.form['section_ID']
        cursor = dbserver.cursor()
        if sec_ID and student_ID:
            print("Executing")
            cursor.execute("INSERT INTO takes (student_ID, section_ID) VALUES (%s, %s)", [student_ID, sec_ID])
        cursor.close()
        dbserver.commit()

        #Gets Updated Courses List to filter out course just signed up for
        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, c.credits, s.semester, s.year, s.section_ID FROM section s JOIN course c on s.course_ID = c.course_ID WHERE s.year > 2025 AND NOT EXISTS (SELECT 1 FROM takes t WHERE t.section_ID = s.section_ID AND t.student_ID = %s)",[student_ID])
        sections = cursor.fetchall()
        cursor.close()
        return render_template("register.html", sections=sections)


#Allows Dropping of classes
#Also works just need real user ID and some polish like better year
#There is a bug here with the redirect back to dash, is not a proper redirect
@app.route("/drop", methods=['POST', 'GET'])
def dropClass():
    student_ID = "1"
    
    if request.method == 'GET':
        #Gets all classes student is registered for
        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, s.semester, s.year, s.section_ID FROM takes t JOIN section s on t.section_ID = s.section_ID JOIN course c on c.course_ID = s.course_ID WHERE t.student_ID = %s AND s.year = 2026",[student_ID])
        enrolled = cursor.fetchall()
        cursor.close()
        return render_template("drop.html", enrolled=enrolled)
    
    if request.method == 'POST':
        #Drops section entry from takes
        sec_ID = request.form['section_ID']
        cursor = dbserver.cursor()
        if sec_ID and student_ID:
            cursor.execute("DELETE FROM takes WHERE section_ID = %s and student_ID = %s",[sec_ID,student_ID])
            dbserver.commit()
        cursor.close()
        return render_template("dash.html")
        
@app.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")

@app.route("/edit_student", methods=["GET", "POST"])
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

@app.route("/edit_instructor", methods=["GET", "POST"])
def edit_instructor():
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
        return redirect(url_for("edit_instructor"))

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

@app.route("/checkCourses", methods=['POST', 'GET'])
def checkStudentCourses():
    #NEED TO CHANGE ONCE WE LINK ACCOUNTS AND ID'S
    student_ID = "1"

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

        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, t.grades FROM takes t JOIN section s ON t.section_ID = s.section_ID JOIN course c on c.course_ID = s.course_ID WHERE t.student_ID = %s AND s.semester = %s AND s.year = %s",[student_ID, semester, year])
        courses = cursor.fetchall()

        cursor.close()
        return render_template("checkCoursesResults.html", courses=courses)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
