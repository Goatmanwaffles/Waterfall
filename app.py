from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from setup import makeDatabase, runSQL, generateSeedData, resetDatabase, dbserver
from flask_session import Session
import config
import pymysql
import bcrypt
import json
from routes import loadBlueprints

app = Flask(__name__)

# This code will reset the database on run
resetDatabase()

dbserver.select_db(config.DB_NAME)

cursor = dbserver.cursor()

app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files

# Initialize Flask-Session
Session(app)

loadBlueprints(app)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
