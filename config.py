from pathlib import Path
import pymysql

# The DB_NAME of the database and other info
# You need to create the database manually, I could not figure out
#    how to do it for you
DB_NAME = "waterfall"
HOST = "localhost"
USER = "root"
PASSWORD = ""

#######################
# Builds the database
########
# Makes the database if it does not exist
make_db = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
)
cursor = make_db.cursor()

# DROPS THE ENTIRE DATABASE
# THIS IS ONLY FOR TESTING PURPOSES!!!!!
cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
make_db.commit()


# This connects to the local host
dbserver = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DB_NAME
)

# This creates and selects the database if it does not exist
cursor = dbserver.cursor()

# Prints the selected database
print(f"Selected database: {dbserver.db}")

# SQL files to run (in order)
# use pathlib for compatibility on Mac
PROJECT_ROOT = Path(__file__).resolve().parent
sql_files = [
    PROJECT_ROOT / "sql" / "schema.sql",
    PROJECT_ROOT / "sql" / "seed-data.sql",
]

# Builds schema
for sql_file in sql_files:
    with sql_file.open(encoding="utf-8") as file:
        sql = file.read()
        for command in sql.split(";"):
            command = command.strip()
            if command:
                print(f"Executed: {command}")
                x = cursor.execute(command)
dbserver.commit()
