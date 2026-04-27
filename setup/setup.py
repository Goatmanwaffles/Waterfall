import pymysql
from pathlib import Path
from random import randint, choice
from string import ascii_letters
import config
from setup import seed_data
import bcrypt

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
    make_db.close()

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
        data += f"{choice(seed_data.student_first_names)}"

    #STUDENT FIRST NAME HANDLER
    if column == "last_name" and table == "student":
        data += f"{choice(seed_data.student_last_names)}"
    
    #INSTRUCTOR FIRST NAME HANDLER
    if column == "first_name" and table == "instructor":
        data += f"{choice(seed_data.instructor_first_names)}"

    #INSTRUCTOR LAST NAME HANDLER
    if column == "last_name" and table == "instructor":
        data += f"{choice(seed_data.instructor_last_names)}"

    #DEPT NAME HANDLER
    if column == "department_name" and table == "department":
        used = []
        dept = seed_data.dept_names[seed_data.count];
        if dept not in used:
            data += f"{dept}"
            used.append(dept)
        else:
            dept = seed_data.dept_names[seed_data.count];
            data += f"{dept}"
            used.append(dept)
        seed_data.count += 1

    #Building NAME HANDLER
    if table == "building":
        if column == "building_name":
            data += f"{choice(seed_data.buildings)}"

    #SECTION SEMESTER HANDLER
    if table == "section":
        if column == "semester":
            data += f"{choice(seed_data.semesters)}"

    #GRADES HANDLER
    if table == "takes":
        if column == "grades":
            data += f"{choice(seed_data.grades)}"

    #ADVISOR HANDLER
    if table == "advisor":
        if column == "first_name":
            data += f"{choice(seed_data.advisor_first_names)}"
        if column == "last_name":
            data += f"{choice(seed_data.advisor_last_names)}"

    #COURSE HANDLER
    if table == "course":
        if column == "title":
            data += f"{choice(seed_data.course_titles)}"

    #DAY HANDLER
    if table == "time_slot":
        if column == "day":
            data += f"{choice(seed_data.days)}"

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
        minimum = 2015
        maximum = 2029
    elif (table == "student" and column == "total_cred"):
        minimum = 0
        maximum = 240
    elif (table == "classroom"):
        if column == "room_number":
            minimum = 0
            maximum = 999
        elif column == "capacity":
            minimum = 1 
            maximum = 999 
    
    
    integer = str(randint(minimum, maximum))
    data = integer

    beforeDecimal = precision - scale
    if scale != 0:
        data = integer[:beforeDecimal] + "." + integer[:scale]
    
    return data

def generateSeedData(tables, schema_filename, seed_filename):
    teaches = []
    schema_path = makePath(schema_filename) # Makes absolute file path
    seed_path = makePath(seed_filename)
    seed = open(file=seed_path, mode="w", encoding="utf-8")
    seed.truncate(0) # Clears the file

    #Creates teaches logic
    instructor_ids = list(range(1, len(seed_data.instructors) + 1))
    section_ids = list(range(1, 101))

    seed_data.teaches = []

    section_index = 0

    for instructor_id in instructor_ids:
        for _ in range(100 // len(instructor_ids)):  # distribute sections evenly across all instructors
            if section_index >= len(section_ids):
                break

            seed_data.teaches.append({
                "instructor_ID": instructor_id,
                "section_ID": section_ids[section_index]
            })

            section_index += 1

    #CREATES TAKES LOGIC
    seed_data.takes = []

    student_ids = list(range(1, len(seed_data.students) + 1))
    section_ids = list(range(1, 101))

    used = set()

    # guarantee: each section has at least 1 student
    for section_id in section_ids:
        student_id = choice(student_ids)

        pair = (student_id, section_id)
        used.add(pair)

        seed_data.takes.append({
            "student_ID": student_id,
            "section_ID": section_id,
            "grade": choice(seed_data.grades)
        })

    # add extra randomness
    for _ in range(len(student_ids) * 3):
        student_id = choice(student_ids)
        section_id = choice(section_ids)

        pair = (student_id, section_id)

        if pair in used:
            continue

        used.add(pair)

        seed_data.takes.append({
            "student_ID": student_id,
            "section_ID": section_id,
            "grade": choice(seed_data.grades)
        })

    for table, columns in tables.items():
        if table == "account":
            row_count = len(seed_data.accounts)  
        elif table == "advisor":
            row_count = len(seed_data.advisors)
        elif table == "advises":
            row_count = len(seed_data.advises)
        elif table == "student":
            row_count = len(seed_data.students)
        elif table == "takes":
            row_count = len(seed_data.takes)
        elif table == "instructor":
            row_count = len(seed_data.instructors)
        elif table == "teaches":
            row_count = len(seed_data.teaches)
        else:
            row_count = 100
        for i in range(row_count): # Creates that many rows per table

            values = "" # Everything to be inserted
            col_names = "" # Collumns to insert into

            # Iterate through every column and pull datatype
            for column, datatype in columns.items():

                if "PRIMARY KEY" in datatype:
                    continue

                if table == "account":
                    account = seed_data.accounts[i]
                    if column == "username":
                        data = f'"{account["username"]}"'
                    elif column == "password":
                        h = bcrypt.hashpw(account["password"].encode('utf-8'), bcrypt.gensalt())
                        data = f'"{h.decode("utf-8")}"'
                    elif column == "role":
                        data = f'"{account["role"]}"'

                elif table == "advisor":
                    advisor = seed_data.advisors[i]
                    if column == "first_name":
                        data = f'"{advisor["first_name"]}"'
                    elif column == "last_name":
                        data = f'"{advisor["last_name"]}"'
                    elif column == "department_ID":
                        data = advisor["department_ID"]

                elif table == "student":
                    student = seed_data.students[i]
                    if column == "first_name":
                        data = f'"{student["first_name"]}"'
                    elif column == "last_name":
                        data = f'"{student["last_name"]}"'
                    elif column == "department_ID":
                        data = student["department_ID"]
                    elif column == "total_cred":
                        data = student["total_cred"]
                    elif column == "advisor_ID":
                        data = student["advisor_ID"]
                    elif column == "account_ID":
                        data = student["account_ID"]
                
                elif table == "instructor":
                    instructor = seed_data.instructors[i]

                    if column == "first_name":
                        data = f'"{instructor["first_name"]}"'
                    elif column == "last_name":
                        data = f'"{instructor["last_name"]}"'
                    elif column == "department_ID":
                        data = instructor["department_ID"]
                    elif column == "salary":
                        data = instructor["salary"]
                    elif column == "account_ID":
                        data = instructor["account_ID"]

                elif table == "teaches":
                    teach = seed_data.teaches[i]

                    if column == "instructor_ID":
                        data = teach["instructor_ID"]
                    elif column == "section_ID":
                        data = teach["section_ID"]

                elif table == "takes":
                    take = seed_data.takes[i]

                    if column == "student_ID":
                        data = take["student_ID"]
                    elif column == "section_ID":
                        data = take["section_ID"]
                    elif column == "grades":
                        data = f'"{take["grade"]}"'

                elif table == "advises":
                    advises = seed_data.advises[i]

                    if column == "student_ID":
                        data = advises["student_ID"]
                    elif column == "instructor_ID":
                        data = advises["instructor_ID"]

                elif table == "prereq":
                    if column == "base_course_ID":
                        data = i+1
                    elif column == "requires_course_ID":
                        reqID = randint(1, 50)
                        if reqID == i and not 100:
                            reqID += 1
                        data = reqID

                elif "int" in datatype:
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

def resetDatabase():
    # Creates the database server object
    dbserver = makeDatabase(
        config.HOST, 
        config.USER, 
        config.PASSWORD, 
        config.DB_NAME
    )

    cursor = dbserver.cursor() # Creates cursor (never recreate)
    # I moved it here so it only runs once bc that was giving me trouble
    generateSeedData(config.TABLES, config.SCHEMA, config.SEED) # Generates seed data

    runSQL(cursor, dbserver, config.SCHEMA ) # Inputs schema
    runSQL(cursor, dbserver, config.SEED   ) # Inputs seed data
    runSQL(cursor, dbserver, config.QUERIES) # Sets up procedure queries
