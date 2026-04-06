import pymysql

# This connects for local host
dbserver = pymysql.connect(
    host="localhost",
    user="root",
    password=""
)

# This creates and selects the database if it does not exist
cursor = dbserver.cursor()
# sql = "IF NOT EXISTS CREATE DATABASE waterfall; USE waterfall;"
sql = "CREATE DATABASE IF NOT EXISTS waterfall;"
cursor.execute(sql)
cursor.close()

# dbserver = pymysql.connect(
#     host="localhost",
#     user="root",
#    password="",
#    database="waterfall"
#)