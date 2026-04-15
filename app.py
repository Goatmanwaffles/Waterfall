from flask import Flask, render_template, request, redirect, url_for
from setup import makeDatabase, runSQL, generateSeedData
import config
import pymysql

app = Flask(__name__)

# Creates the database server object
dbserver = makeDatabase(config.HOST, config.USER, config.PASSWORD, config.DB_NAME)
cursor = dbserver.cursor()
# I moved it here so it only runs once bc that was giving me trouble
generateSeedData(config.TABLES, config.SCHEMA, config.SEED) # Generates seed data

runSQL(cursor, dbserver, config.SCHEMA ) # Inputs schema
runSQL(cursor, dbserver, config.SEED   ) # Inputs seed data
runSQL(cursor, dbserver, config.QUERIES) # Sets up procedure queries
cursor.close()
dbserver.commit()

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
        print(row)

        if not row or not (password == row[1]):
            print("ERROR")
            return render_template("login.html", error="Invalid Username or Password")
        
        #Valid Login
        if row and (password == row[1]):
            return redirect(url_for('dash'))

@app.route("/dashboard")
def dash():
    return render_template("dash.html")

if __name__ == '__main__':
    app.run(host="localhost", port=4500, debug=True)
