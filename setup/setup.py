import pymysql
from pathlib import Path
from random import randint, choice
from string import ascii_letters
import config

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

def randomInteger(table, column, datatype, max):
    data = f"{randint(1,max)}"
    return data

def randomVarchar(table, column, datatype):
    # Starts the string
    data = "\""

    #STUDENT FIRST NAME HANDLER
    if column == "first_name" and table == "student":
        data += f"{choice(config.student_first_names)}"

    #STUDENT FIRST NAME HANDLER
    if column == "last_name" and table == "student":
        data += f"{choice(config.student_last_names)}"
    
    #INSTRUCTOR FIRST NAME HANDLER
    if column == "first_name" and table == "instructor":
        data += f"{choice(config.instructor_first_names)}"

    #INSTRUCTOR LAST NAME HANDLER
    if column == "last_name" and table == "instructor":
        data += f"{choice(config.instructor_last_names)}"

    #DEPT NAME HANDLER
    if column == "department_name" and table == "department":
        data += f"{choice(config.dept_names)}"

    #DEPT NAME HANDLER
    if column == "building" and table == "department":
        data += f"{choice(config.buildings)}"

    if table == "classroom":
        if column == "building_name":
            data += f"{choice(config.buildings)}"

    #SECTION SEMESTER HANDLER
    if table == "section":
        if column == "semester":
            data += f"{choice(config.semesters)}"

    #GRADES HANDLER
    if table == "takes":
        if column == "grades":
            data += f"{choice(config.grades)}"

    #ADVISOR HANDLER
    if table == "advisor":
        if column == "first_name":
            data += f"{choice(config.advisor_first_names)}"
        if column == "last_name":
            data += f"{choice(config.advisor_last_names)}"

    #COURSE HANDLER
    if table == "course":
        if column == "title":
            data += f"{choice(config.course_titles)}"

    #DAY HANDLER
    if table == "time_slot":
        if column == "day":
            data += f"{choice(config.days)}"


    # Random character fallback
    right = datatype.split("(")[1] 
    length = right.split(")")[0]
    if data == "\"":
        for _ in range(int(length)):
            data += choice(ascii_letters)

    # Closes off the string
    data += "\""

    return data

def randomNumeric(table, column, datatype):
    right = datatype.split("(")[1] 
    commas = right.split(")")[0]

    # Gets the precision and scale
    if "," in commas:
        length = commas.split(",")
        precision = int(length[0])
        scale = int(length[1])
    else: # No scale defaults to zero
        precision = int(commas)
        scale = 0

    # Gets the randomization 
    minimum = 0
    maximum = pow(10, precision)

    # Handling tables
    if (table == "department" and column == "budget"):
        minimum = 1
    elif (table == "time_slot"):
        if (column == "start_hr" or column == "end_hr"):
            maximum = 23
        elif (column == "start_min" or column == "end_min"):
            maximum = 59
    elif (table == "course" and column == "credits"):
        minimum = 1
        maximum = 99
    elif (table == "instructor" and column == "salary"):
        minimum = 29001
    elif (table == "section" and column == "year"):
        minimum = 1701
        maximum = 2100
    elif (table == "student" and column == "total_cred"):
        minimum = 0
        maximum = 240
    elif (table == "classroom" and column == "room_number"):
        minimum = 0
        maximum = 999
    
    
    integer = str(randint(minimum, maximum))
    data = integer

    beforeDecimal = precision - scale
    if scale != 0:
        data = integer[:beforeDecimal] + "." + integer[:scale]
    
    return data

def generateSeedData(tables, schema_filename, seed_filename):
    
    schema_path = makePath(schema_filename) # Makes absolute file path
    seed_path = makePath(seed_filename)
    seed = open(file=seed_path, mode="w", encoding="utf-8")
    seed.truncate(0) # Clears the file

    for table, columns in tables.items():
        for i in range(10): # Creates that many rows per table

            values = "" # Everything to be inserted
            col_names = "" # Collumns to insert into

            # Iterate through every column and pull datatype
            for column, datatype in columns.items():

                if "PRIMARY KEY" in datatype:
                    continue
    
                if "int" in datatype:
                    #DEPRECEATED FUNCTIONALITY
                    #data = randomInteger(table, column, datatype, i+1)
                    data = i+1
                elif "varchar" in datatype:
                    data = randomVarchar(table, column, datatype)
                elif "numeric" in datatype:
                    data = randomNumeric(table, column, datatype)
                else:
                    data = "??????"
                
                values += f"{data}, " # Actually inserts data
                col_names += f"{column}, "
            
            values = values[:-2] # Cuts off extra ', '
            col_names = col_names[:-2]


            insert = ""
            #if (table != "classroom"):
            #    insert += "-- "
            insert += f"INSERT INTO {table} ({col_names}) VALUES ({values});;\n"
            # print(insert)
            seed.write(insert)

    seed.close()
