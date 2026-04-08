import pymysql
from pathlib import Path
from random import randint, choice
from string import ascii_letters

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

def getRandomized(datatype):
    data = ""
    
    if "int" in datatype:
        data = f"{randint(1,999)}"
    
    elif "varchar" in datatype:
        right = datatype.split("(")[1] 
        length = right.split(")")[0]
        for _ in range(int(length)):
            data += f"{choice(ascii_letters)}"

    elif "numeric" in datatype:
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
        digits = precision - scale
        minMax = pow(10, digits)
        integer = str(randint(0, minMax))
        data = integer
        
        if scale != 0:
            data = integer[:scale] + "." + integer[scale:]
        
    else:
        data = "??????"

    return data

def generateSeedData(tables, schema_filename, seed_filename, rows=5):
    
    schema_path = makePath(schema_filename) # Makes absolute file path
    seed_path = makePath(seed_filename)
    seed = open(file=seed_path, mode="w", encoding="utf-8")
    seed.truncate(0) # Clears the file

    for table, columns in tables.items():
        for _ in range(rows): # Creates that many rows per table

            values = "" # Everything to be inserted

            # Iterate through every column and pull datatype
            for column, datatype in columns.items():
                data = getRandomized(datatype)

                values += f"{data}, " # Actually inserts data
            
            values = values[:-2] # Cuts off extra ', '

            seed.write(f"-- INSERT INTO {table} VALUES ({values});;\n")

    seed.close()
    











