import pymysql
from pathlib import Path

# Returns the pymysql.connect object
def makeDatabase(hostname, username, password, database_name):
    # Makes the database if it does not exist
    make_db = pymysql.connect(
        host=hostname,
        user=username,
        password=password,
    )

    cursor = make_db.cursor()

    # DROPS THE ENTIRE DATABASE
    # THIS IS ONLY FOR TESTING PURPOSES!!!!!
    cursor.execute(f"DROP DATABASE IF EXISTS {database_name};")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
    make_db.commit()

    # This connects to the local host
    dbserver = pymysql.connect(
        host=hostname,
        user=username,
        password=password,
        database=database_name
    )
    
    return dbserver

def makePath(sql_filename):
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    sql_path = f"{PROJECT_ROOT / "sql" / sql_filename}"
    return sql_path

# Runs any sql file input into it
def runSQL(cursor, dbserver, sql_filename):
    p = makePath(sql_filename)

    # Runs the SQL file
    with open(file=p, encoding="utf-8") as file:
        sql = file.read()
        for command in sql.split(";;"):
            command = command.strip()
            if command:
                # print(f"Executed: {command}")
                x = cursor.execute(command)
    
    dbserver.commit()

def generateSeedData(schema_filename, seed_filename):
    tables = {
        "classroom":  ["varchar(15)", "varchar(7)",  "numeric(4,0)"],
        "department": ["varchar(20)", "varchar(15)", "numeric(12,2)"],
        "course":     ["varchar(8)",  "varchar(50)", "varchar(20)", "numeric(2,0)"],
        "instructor": ["varchar(5)", "varchar(20)", "varchar(20)", "numeric(8,2)"],
        "section":    ["varchar(8)", "varchar(8)", "varchar(6)", "numeric(4,0)", "varchar(15)", "varchar(7)", "varchar(4)"],
        "teaches":    ["varchar(5)", "varchar(8)", "varchar(8)", "varchar(6)", "numeric(4,0)"],
        "student":    ["varchar(5)", "varchar(20)", "varchar(20)", "numeric(3,0)"],
        "takes":      ["varchar(5)", "varchar(8)", "varchar(8)", "varchar(6)", "numeric(4,0)", "varchar(2)"],
        "advisor":    ["varchar(5)", "varchar(5)"],
        "time_slot":  ["varchar(4)", "varchar(1)", "numeric(2)", "numeric(2)", "numeric(2)", "numeric(2)", "numeric(2)", "numeric(2)"],
        "prereq":     ["varchar(8)", "varchar(8)"]
    }

    schema_path = makePath(schema_filename) # Makes absolute file path
    seed_path = makePath(seed_filename)
 #   seed = open(file=seed_path, mode="w", encoding="utf-8")
 #   seed.truncate(0) # Clears the file

#    for table in tables:
 #       values = "'Packard', '101', '500'"
  #      seed.write(f"INSERT INTO {table} VALUES ({values});;\n")

#    seed.close()
    











