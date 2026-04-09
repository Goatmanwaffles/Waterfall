
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import config
from setup import makeDatabase, runSQL

    
if __name__ == "__main__":
    dbserver = makeDatabase(config.HOST, config.USER, config.PASSWORD, config.DB_NAME)
    cursor = dbserver.cursor()

    runSQL(cursor, dbserver, config.SCHEMA)
    runSQL(cursor, dbserver, config.SEED)
    runSQL(cursor, dbserver, config.QUERIES)

    # Student CRUD

    cursor.execute("CALL create_student('Jane', 'Doe', 'CS', 0, 'TJ', 'Smith', 'BIO')")
    dbserver.commit()

    cursor.execute("Call update_student(1,'Cal','Stanberry','CS',168,1)")
    dbserver.commit()

    cursor.execute("Call delete_student(3)")
    dbserver.commit()

    cursor.execute("CALL get_students()")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    