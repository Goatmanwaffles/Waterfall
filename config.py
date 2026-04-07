import pymysql
from setup import makeDatabase, runSQL

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
dbserver = makeDatabase(HOST, USER, PASSWORD, DB_NAME)

# This creates and selects the database if it does not exist
cursor = dbserver.cursor()

# Puts the schema into the database
runSQL(cursor, dbserver, "schema.sql")

# generateSeedData()

# Puts the seed data into the database
runSQL(cursor, dbserver, "seed-data.sql")

