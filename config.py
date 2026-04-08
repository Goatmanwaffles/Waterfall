
# The DB_NAME of the database and other info
# You need to create the database manually, I could not figure out
#    how to do it for you
DB_NAME = "waterfall"

# Other general configuration stuff
HOST = "localhost"
USER = "root"
PASSWORD = ""

# SQL file names (Must be in sql/ directory)
schema = "schema.sql"
seed = "seed-data.sql"
queries = "queries.sql"

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
    }
    # "time_slot": {
    #     "time_Slot_ID": "int", 
    #     "varchar(1)", 
    #     "numeric(2)", 
    #     "numeric(2)", 
    #     "numeric(2)", 
    #     "numeric(2)", 
    #     "numeric(2)", 
    #     "numeric(2)"
    # },
    # "course": {
    #     "varchar(8)",  
    #     "varchar(50)", 
    #     "varchar(20)", 
    #     "numeric(2,0)"
    # },
    # "instructor": {
    #     "varchar(5)", 
    #     "varchar(20)", 
    #     "varchar(20)", 
    #     "numeric(8,2)"
    # },
    # "section": {
    #     "varchar(8)", 
    #     "varchar(8)", 
    #     "varchar(6)", 
    #     "numeric(4,0)", 
    #     "varchar(15)", 
    #     "varchar(7)", 
    #     "varchar(4)"
    # },
    # "teaches": {
    #     "varchar(5)", 
    #     "varchar(8)", 
    #     "varchar(8)", 
    #     "varchar(6)", 
    #     "numeric(4,0)"
    # },
    # "student": {
    #     "varchar(5)", 
    #     "varchar(20)", 
    #     "varchar(20)", 
    #     "numeric(3,0)"
    # },
    # "takes": {
    #     "varchar(5)", 
    #     "varchar(8)", 
    #     "varchar(8)", 
    #     "varchar(6)", 
    #     "numeric(4,0)", 
    #     "varchar(2)"
    # },
    # "advisor": {
    #     "varchar(5)", 
    #     "varchar(5)"
    # },
    # "prereq": {
    #     "varchar(8)", 
    #     "varchar(8)"
    # }
}