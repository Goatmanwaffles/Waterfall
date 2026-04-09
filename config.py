
# The DB_NAME of the database and other info
# You need to create the database manually, I could not figure out
#    how to do it for you
DB_NAME = "waterfall"

# Other general configuration stuff
HOST     = "localhost"
USER     = "root"
PASSWORD = ""

# SQL file names (Must be in sql/ directory)
SCHEMA  = "schema.sql"
SEED    = "seed-data.sql"
QUERIES = "queries.sql"

# Seed data generator for testing
student_first_names = ["Logan", "Andrew", "Caleb"]
student_last_names = ["Senol", "Roddy", "Stanberry"]
instructor_first_names = ["Javed", "Giovanni", "Mikhail"]
instructor_last_names = ["Kahn", "Phares", "Nesterenko"]
dept_names = ["CS", "BIO", "MATH", "CHEM"]
buildings = ["Smith", "MSB", "DI", "White"]

# This is the schema used to make the test data
TABLES = {
    "classroom":  {
        "building_ID": "int AUTO_INCREMENT PRIMARY KEY",
        "building":    "varchar(15)", 
        "room_number": "numeric(3,0)",  
        "capacity":    "numeric(4,0)"
    },
    "department": {
        "department_ID": "int AUTO_INCREMENT PRIMARY KEY",
        "department_name": "varchar(20)", 
        "building":  "varchar(15)", 
        "budget":    "numeric(12,2)"
    },
    "time_slot": {
        "time_slot_ID": "int AUTO_INCREMENT PRIMARY KEY", 
        "day":          "varchar(1)", 
        "start_hr":     "numeric(2)", 
        "start_min":    "numeric(2)", 
        "end_hr":       "numeric(2)", 
        "end_min":      "numeric(2)", 
    },
    "advisor": {
        "advisor_ID": "int AUTO_INCREMENT PRIMARY KEY", 
        "first_name": "varchar(20)",
        "last_name":  "varchar(20)",
        "department_ID": "int"
    },
    "course": {
        "course_ID": "int AUTO_INCREMENT PRIMARY KEY",  
        "title":     "varchar(50)", 
        "department_ID": "int", 
        "credits":   "numeric(2,0)"
    },
    "instructor": {
        "instructor_ID": "int AUTO_INCREMENT PRIMARY KEY", 
        "first_name":          "varchar(20)",
        "last_name":     "varchar(20)",
        "department_ID":     "int", 
        "salary":        "numeric(8,2)"
    },
    "section": {
        "section_ID": "int AUTO_INCREMENT PRIMARY KEY", 
        "course_ID": "int", 
        "semester": "varchar(6)", 
        "year": "numeric(4,0)", 
        "building_ID": "int", 
        "time_slot_ID": "int"
    },
    "student": {
        "student_ID": "int AUTO_INCREMENT PRIMARY KEY", 
        "first_name": "varchar(20)", 
        "last_name": "varchar(20)", 
        "department_ID": "int", 
        "total_cred": "numeric(3,0)",
        "advisor_ID": "int"
    },
    "teaches": {
        "instructor_ID": "int", 
        "section_ID": "int",
    },
    "takes": {
        "student_ID": "int",
        "section_ID": "int", 
        "grades": "varchar(2)"
    },
    "advises": {
        "student_ID": "int", 
        "advisor_ID": "int", 
    },
    "prereq": {
        "prereq_ID": "int AUTO_INCREMENT PRIMARY KEY", 
        "base_course_ID": "int",
        "requires_course_ID" : "int"
    },
}