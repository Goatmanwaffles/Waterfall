from flask import Flask, render_template, request, redirect, url_for
from setup import makeDatabase, runSQL, generateSeedData, resetDatabase
import config
import pymysql
import bcrypt

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
        cursor.execute("SELECT username, password, role FROM account WHERE username = %s", (username))
        row = cursor.fetchone()

        #Convert password into bytes for check
        password = password.encode('utf-8')
        hashedPW = row[1].encode('utf-8')
        if not row or not (bcrypt.checkpw(password, hashedPW)):
            print("ERROR")
            return render_template("login.html", error="Invalid Username or Password")
        
        #THIS SHOULD PROB BE A SEPERATE FUNCTION AT SOME POINT AND WE SHOULD MAYBE HASH PASSWORDS IF WE WANT SECURITY
        #Valid Login
        if row and (bcrypt.checkpw(password, hashedPW)):
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
    return render_template("dash.html")

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
