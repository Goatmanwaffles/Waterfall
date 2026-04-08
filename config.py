
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

# This is the schema used to make the test data
TABLES = {
    "classroom":  {
        "building":    "varchar(15)", 
        "room_number": "varchar(7)",  
        "capacity":    "numeric(4,0)"
    },
    "department": {
        "dept_name": "varchar(20)", 
        "building":  "varchar(15)", 
        "budget":    "numeric(12,2)"
    },
    "time_slot": {
        "time_Slot_ID": "int", 
        "day":          "varchar(1)", 
        "start_hr":     "numeric(2)", 
        "start_min":    "numeric(2)", 
        "end_hr":       "numeric(2)", 
        "end_min":      "numeric(2)", 
    },
    "advisor": {
        "advisor_ID": "int", 
        "first_name": "varchar(20)",
        "last_name":  "varchar(20)",
        "department": "varchar(20)"
    },
    "course": {
        "course_ID": "int",  
        "title":     "varchar(50)", 
        "dept_name": "varchar(20)", 
        "credits":   "numeric(2,0)"
    },
    "prereq": {
        "prereq_ID": "int", 
        "course_ID": "int"
    },
    "instructor": {
        "instructor_ID": "int", 
        "name":          "varchar(20)", 
        "dept_name":     "varchar(20)", 
        "salary":        "numeric(8,2)"
    },
    "section": {
        "section_ID": "int", 
        "course_ID": "int", 
        "semester": "varchar(6)", 
        "year": "numeric(4,0)", 
        "building": "varchar(15)", 
        "room_number": "varchar(7)", 
        "time_slot_ID": "int"
    },
    "student": {
        "student_ID": "int", 
        "first_name": "varchar(20)", 
        "last_name": "varchar(20)", 
        "dept_name": "varchar(20)", 
        "total_cred": "numeric(3,0)",
        "advisor_ID": "int"
    },
    "teaches": {
        "instructor_ID": "int", 
        "course_ID": "int", 
        "section_ID": "int", 
        "semester": "varchar(6)", 
        "year": "numeric(4,0)"
    },
    "takes": {
        "student_ID": "int", 
        "course_ID": "int", 
        "section_ID": "int", 
        "semester": "varchar(6)", 
        "year": "numeric(4,0)", 
        "grade": "varchar(2)"
    },
    "advises": {
        "student_ID": "int", 
        "advisor_ID": "int", 
    },
}