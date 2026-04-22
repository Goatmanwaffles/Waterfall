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
        cursor.execute("SELECT a.username, a.password, a.role, a.account_ID FROM account a WHERE username = %s", (username))
        row = cursor.fetchone()

        #Convert password into bytes for check
        password = password.encode('utf-8')
        hashedPW = row[1].encode('utf-8')
        if not row or not (bcrypt.checkpw(password, hashedPW)):
            print("ERROR")
            return render_template("login.html", error="Invalid Username or Password")
        
        #Valid Login
        if row and (bcrypt.checkpw(password, hashedPW)):
            if row[2] == "Student":
                cursor.execute("SELECT s.student_ID FROM student s WHERE s.account_ID = %s",[row[3]])
            elif row[2] == "Instructor": #NEEDS IMPLEMENTED DATABASE LEVEL
                cursor.execute("SELECT s.student_ID FROM student s WHERE s.account_ID = %s",[row[3]])
            elif row[2] == "Administrator": #NEEDS IMPLEMENTED DATABASE LEVEL
                cursor.execute("SELECT s.student_ID FROM student s WHERE s.account_ID = %s",[row[3]])
            Id = cursor.fetchone()
            print(Id)
            session["role"] = row[2] #Store role in session
            session["userID"] = Id #Store user ID, Either Student, Instructor, or Admin
            session["accountID"] = row[3]
            cursor.close()
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
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        if not username or not password or not confirmPassword or not firstName or not lastName:
            return render_template("signup.html", error="Missing Field")
        
        if password != confirmPassword:
            return render_template("signup.html", error="Passwords do not match")
        
        #Salt and Hash password
        password_bytes = password.encode('utf-8')
        s = bcrypt.gensalt()
        h = bcrypt.hashpw(password_bytes, s)

        cursor = dbserver.cursor()
        cursor.execute(f"CALL create_account(%s, %s, 'Student')", (username, h))
        cursor.execute("INSERT INTO student s(s.first_name, s.last_name)")
        cursor.close()
        dbserver.commit()

        return redirect(url_for('login'))

@app.route("/dashboard")
def dash():
    #Get User auth level
    role = session.get("role")
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
    student_ID = session.get("userID")
    
    if request.method == 'GET':
        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, c.credits, s.semester, s.year, s.section_ID FROM section s JOIN course c on s.course_ID = c.course_ID WHERE s.year > 2025 AND NOT EXISTS (SELECT 1 FROM takes t WHERE t.section_ID = s.section_ID AND t.student_ID = %s)",[student_ID])
        sections = cursor.fetchall()
        cursor.close()
        return render_template("register.html", sections=sections)
    if request.method == 'POST':
        
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
    student_ID = session.get("userID")
    
    if request.method == 'GET':
        #Gets all classes student is registered for
        cursor = dbserver.cursor()
        cursor.execute("SELECT c.title, s.semester, s.year, s.section_ID FROM takes t JOIN section s on t.section_ID = s.section_ID JOIN course c on c.course_ID = s.course_ID WHERE t.student_ID = %s AND s.year >= 2026",[student_ID])
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

@app.route("/checkCourses", methods=['POST', 'GET'])
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

#MODIFY PERSONAL INFO FOR ALL
@app.route("/account", methods=['GET', 'POST'])
def account():
    role = session.get("role")
    userID = session.get("userID")
    if request.method == 'GET':
        cursor = dbserver.cursor()
        if role == "Student":
            cursor.execute("SELECT s.first_name, s.last_name FROM account a JOIN student s on s.account_ID = a.account_ID WHERE s.student_ID = %s", [userID])
        user = cursor.fetchone()
        cursor.close()
        return render_template("profile.html", user=user)
    

    if request.method == 'POST':
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        cursor = dbserver.cursor()
        if role == "Student":
            cursor.execute("UPDATE student SET first_name = %s, last_name = %s WHERE student_ID = %s", [firstName, lastName, userID])
        
        dbserver.commit()
        cursor.close()
        return redirect(url_for('dash'))
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
