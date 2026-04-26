from flask import Blueprint, render_template, request, redirect, url_for, session
from setup import dbserver
import bcrypt

account_blueprint = Blueprint("account", __name__)

@account_blueprint.route("/", methods=['POST', 'GET'])
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
        cursor.execute("SELECT a.username, a.password, a.role, a.account_ID FROM account a WHERE username = %s", [username])
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
            elif row[2] == "Instructor":
                cursor.execute("SELECT i.instructor_ID FROM instructor i WHERE i.account_ID = %s",[row[3]])
            elif row[2] == "Administrator": #NEEDS IMPLEMENTED DATABASE LEVEL
                cursor.execute("SELECT s.student_ID FROM student s WHERE s.account_ID = %s",[row[3]])
            result = cursor.fetchone()
            Id = result[0] if result else None
            print(Id)
            session["role"] = row[2] #Store role in session
            session["userID"] = Id #Store user ID, Either Student, Instructor, or Admin
            session["accountID"] = row[3]
            cursor.close()
            return redirect(url_for('dashboard.dash'))

@account_blueprint.route("/signup", methods=['POST', 'GET'])
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
        cursor.execute("CALL create_account(%s, %s, 'Student')", (username, h))
        cursor.execute("SELECT account_ID FROM account WHERE username = %s", (username,))
        account_ID = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO student (first_name, last_name, total_cred, account_ID) VALUES (%s, %s, %s, %s)",
            (firstName, lastName, 0, account_ID)
        )
        cursor.close()
        dbserver.commit()

        return redirect(url_for('account.login'))

#MODIFY PERSONAL INFO FOR ALL
#Need to add password and username change function
@account_blueprint.route("/account", methods=['GET', 'POST'])
def account():
    role = session.get("role")
    userID = session.get("userID")
    accountID = session.get("accountID")

    if request.method == 'GET':
        cursor = dbserver.cursor()

        if role == "Student":
            cursor.execute(
                """
                SELECT a.username, s.first_name, s.last_name
                FROM account a
                JOIN student s ON s.account_ID = a.account_ID
                WHERE s.student_ID = %s
                """,
                [userID]
            )
        elif role == "Instructor":
            cursor.execute(
                """
                SELECT a.username, i.first_name, i.last_name
                FROM account a
                JOIN instructor i ON i.account_ID = a.account_ID
                WHERE i.instructor_ID = %s
                """,
                [userID]
            )
        elif role == "Administrator":
            cursor.execute(
                "SELECT username FROM account WHERE account_ID = %s",
                [accountID]
            )

        user = cursor.fetchone()
        cursor.close()
        return render_template("profile.html", user=user, role=role)
    

    if request.method == 'POST':
        username = request.form["username"]
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")

        cursor = dbserver.cursor()

        cursor.execute(
            "UPDATE account SET username = %s WHERE account_ID = %s",
            [username, accountID]
        )

        if role == "Student":
            cursor.execute("UPDATE student SET first_name = %s, last_name = %s WHERE student_ID = %s", [firstName, lastName, userID])
        elif role == "Instructor":
            cursor.execute("UPDATE instructor SET first_name = %s, last_name = %s WHERE instructor_ID = %s", [firstName, lastName, userID])
        
        dbserver.commit()
        cursor.close()
        return redirect(url_for('dashboard.dash'))
 
@account_blueprint.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")
