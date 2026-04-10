
from pathlib import Path
import sys
import config
from setup import makeDatabase, runSQL

# Prints a CALL query
def printQuery(cursor, call):
    cursor.execute(call)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    
if __name__ == "__main__":
    dbserver = makeDatabase(config.HOST, config.USER, config.PASSWORD, config.DB_NAME)
    cursor = dbserver.cursor()

    runSQL(cursor, dbserver, config.SCHEMA)
    runSQL(cursor, dbserver, config.SEED)
    runSQL(cursor, dbserver, config.QUERIES)


    # Student CRUD
    print("\n--- Students Before ---")
    printQuery(cursor, "CALL get_students()")
        
    cursor.execute("CALL create_student('Jane', 'Doe', 'CS', 0, 'TJ', 'Smith', 'BIO')")
    dbserver.commit()

    cursor.execute("Call update_student(1,'Cal','Stanberry','CS',168,1)")
    dbserver.commit()

    cursor.execute("Call delete_student(3)")
    dbserver.commit()

    print("\n--- Students After ---")
    printQuery(cursor, "CALL get_students()")


    # Instructor CRUD
    print("\n--- Instructors Before ---")
    printQuery(cursor, "CALL get_instructors()")
        
    cursor.execute("CALL create_instructor('John', 'Doe', 'CS', 72000)")
    dbserver.commit()

    cursor.execute("Call update_instructor(1,'Mik','Khan','MATH', 900000.00)")
    dbserver.commit()

    cursor.execute("Call delete_instructor(3)")
    dbserver.commit()

    print("\n--- Instructors After ---")
    printQuery(cursor, "CALL get_instructors()")


    # Section CRUD
    print("\n--- Sections Before ---")
    printQuery(cursor, "CALL get_sections()")
        
    cursor.execute("CALL create_section(3, 'Spring', 2026, 2, 1)")
    dbserver.commit()

    cursor.execute("Call update_section(1, 1,'Summer',1764, 1, 2)")
    dbserver.commit()

    cursor.execute("Call delete_section(3, 3, 'Summer', 1923)")
    dbserver.commit()

    print("\n--- Sections After ---")
    printQuery(cursor, "CALL get_sections()")

    # Account CRUD
    print("\n--- Accounts Before ---")
    printQuery(cursor, "CALL get_accounts()")
        
    cursor.execute("CALL create_account('gioGamer99', 'superSecure', 'Instructor')")
    dbserver.commit()

    cursor.execute("Call update_account(11, 'gioGamer98', 'moreSuperSecure', 'Instructor')")
    dbserver.commit()

    cursor.execute("Call delete_account(1)")
    dbserver.commit()

    print("\n--- Accounts After ---")
    printQuery(cursor, "CALL get_accounts()")


    # Major Stored Procedures

    print("\n--- takes Table Before ---")
    printQuery(cursor, "SELECT * FROM takes")
    
    # Enroll in a section
    cursor.execute("CALL enroll_in_section(1, 11, 'A')")
    dbserver.commit()

    # Student Drops Section
    cursor.execute("CALL drop_section(2,2)")
    dbserver.commit()

    # Give grade to section
    cursor.execute("CALL give_grade_to_section(2, 2, 'B')")
    dbserver.commit()

    print("\n--- takes Table After ---")
    printQuery(cursor, "SELECT * FROM takes")

    # Assign Instructor to Section
    print("\n--- teaches Table Before ---")
    printQuery(cursor, "SELECT * FROM teaches")

    cursor.execute("CALL assign_instructor_to_section(1,11)")
    dbserver.commit()

    print("\n--- teaches Table After ---")
    printQuery(cursor, "SELECT * FROM teaches")
        
    
    