from flask import Blueprint, render_template, request, redirect, url_for
from setup import dbserver

admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/signup", methods=['POST', 'GET'])
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
