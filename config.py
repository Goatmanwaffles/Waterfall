import pymysql

# The DB_NAME of the database and other info
# You need to create the database manually, I could not figure out
#    how to do it for you
DB_NAME = "waterfall"
host = "localhost"
user = "root"
password = ""

#######################
# Builds the database
########

# Makes the database if it does not exist
make_db = pymysql.connect(
    host=host,
    user=user,
    password=password,
)
cursor = make_db.cursor()

# DROPS THE ENTIRE DATABASE
# THIS IS ONLY FOR TESTING PURPOSES!!!!!
cursor.execute(f"DROP DATABASE {DB_NAME};")

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
make_db.commit()


# This connects to the local host
dbserver = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=DB_NAME
)

# This creates and selects the database if it does not exist
cursor = dbserver.cursor()

# Prints the selected database
print(f"Selected database: {dbserver.db}")

# SQL files to run (in order)
# Using a raw string to ignore \s warning
sql_files = [
    r"sql\schema.sql",
    r"sql\seed-data.sql"
]

# Builds schema
for file_DB_NAME in sql_files:
    with open(file_DB_NAME, encoding="utf-8") as file:
        sql = file.read()
        for command in sql.split(";"):
            command = command.strip()
            if command:
                print(f"Executed: {command}")
                x = cursor.execute(command)
dbserver.commit()
