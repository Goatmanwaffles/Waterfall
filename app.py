from flask import Flask
from setup import makeDatabase, runSQL, generateSeedData
import config
import pymysql

app = Flask(__name__)

# Creates the database server object
dbserver = makeDatabase(config.HOST, config.USER, config.PASSWORD, config.DB_NAME)
cursor = dbserver.cursor() # Creates cursor (never recreate)

@app.route("/")
def hello_world():
#    cursor = db.cursor
    return "<h1>Waterfall</h1>"

if __name__ == '__main__':

    # I moved it here so it only runs once bc that was giving me trouble
    generateSeedData(config.TABLES, config.SCHEMA, config.SEED) # Generates seed data

    runSQL(cursor, dbserver, config.SCHEMA ) # Inputs schema
    runSQL(cursor, dbserver, config.SEED   ) # Inputs seed data
    #runSQL(cursor, dbserver, config.QUERIES) # Sets up procedure queries

    app.run(host="localhost", port=4500)
