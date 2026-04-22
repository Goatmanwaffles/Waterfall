from flask import Flask, render_template, request, redirect, url_for, session
from setup import makeDatabase, runSQL, generateSeedData, resetDatabase
from flask_session import Session
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
        cursor.execute("SELECT username, password, role FROM account WHERE username = %s", (username))
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
