import pymysql

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

def buildSchema(cursor, dbserver, sql_files):
    # Builds schema
    for sql_file in sql_files:
        with sql_file.open(encoding="utf-8") as file:
            sql = file.read()
            for command in sql.split(";"):
                command = command.strip()
                if command:
                    # print(f"Executed: {command}")
                    x = cursor.execute(command)
    dbserver.commit()
