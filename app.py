from flask import Flask
from setup import makeDatabase, runSQL
import config
import pymysql

app = Flask(__name__)

# Creates the database server object
dbserver = makeDatabase(config.HOST, config.USER, config.PASSWORD, config.DB_NAME)

cursor = dbserver.cursor() # Creates cursor (never recreate)
runSQL(cursor, dbserver, "schema.sql") # Inputs schema
# generateSeedData()
runSQL(cursor, dbserver, "seed-data.sql") # Inputs seed data
runSQL(cursor, dbserver, "queries.sql") # Sets up procedure queries

@app.route("/")
def hello_world():
#    cursor = db.cursor
    return "<h1>Waterfall</h1>"

if __name__ == '__main__':
    app.run(host="localhost", port=4500)
