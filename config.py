from pathlib import Path
import pymysql
from setup import makeDatabase, buildSchema

# The DB_NAME of the database and other info
# You need to create the database manually, I could not figure out
#    how to do it for you
DB_NAME = "waterfall"

# Other general configuration stuff
HOST = "localhost"
USER = "root"
PASSWORD = ""

#######################
# Builds the database
########

# Creates the database server object
dbserver = makeDatabase(
    hostname = HOST,
    username = USER,
    password = PASSWORD,
    database_name = DB_NAME
)

# This creates and selects the database if it does not exist
cursor = dbserver.cursor()

# Prints the selected database
# print(f"Selected database: {dbserver.db}")

# SQL files to run (in order)
# use pathlib for compatibility on Mac
PROJECT_ROOT = Path(__file__).resolve().parent
sql_files = [
    PROJECT_ROOT / "sql" / "schema.sql",
    PROJECT_ROOT / "sql" / "seed-data.sql",
]

buildSchema(cursor, dbserver, sql_files)
# generateSeedData()
# insertSeedData()

