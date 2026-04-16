
-- CRUD operations for all major tables

-- -- -- 
-- instructor CRUD
-- -- --

-- Create Instructor
DROP PROCEDURE IF EXISTS create_instructor;;
CREATE PROCEDURE create_instructor (
    IN temp_first_name VARCHAR(20),
    IN temp_last_name VARCHAR(20),
    IN temp_dept_name VARCHAR(20),
    IN temp_salary NUMERIC(8,2)
)
BEGIN
    INSERT INTO instructor (first_name, last_name, department_ID, salary)
    VALUES (
        temp_first_name,
        temp_last_name,
        (SELECT department_ID FROM department WHERE department_name = temp_dept_name), 
        temp_salary
    );
END;;

-- Read Instructors
DROP PROCEDURE IF EXISTS get_instructors;;
CREATE PROCEDURE get_instructors()
BEGIN
    SELECT * FROM instructor;
END;;

-- Update Instructor
DROP PROCEDURE IF EXISTS update_instructor;;
CREATE PROCEDURE update_instructor(
    IN temp_instructor_ID int,
    IN temp_first_name varchar(20),
    IN temp_last_name varchar(20),
    IN temp_department_name VARCHAR(20),
    IN temp_salary NUMERIC (8,2)
)
BEGIN
    UPDATE instructor
    SET first_name = temp_first_name,
        last_name = temp_last_name,
        department_ID = (SELECT department_ID FROM department WHERE department_name = temp_department_name),
        salary = temp_salary
    WHERE instructor_ID = temp_instructor_ID;
END;;

-- Delete Instructor
DROP PROCEDURE IF EXISTS delete_instructor;;
CREATE PROCEDURE delete_instructor(
    IN temp_instructor_ID int
)
BEGIN
    DELETE FROM instructor
    WHERE  instructor_ID = temp_instructor_ID;
END;;

-- -- -- 
-- student CRUD
-- -- --

-- Create student
DROP PROCEDURE IF EXISTS create_student;;
CREATE PROCEDURE create_student(
    IN temp_first_name varchar(20),
    IN temp_last_name varchar(20),
    IN temp_department_name VARCHAR(20),
    IN temp_total_credits NUMERIC (3,0),
    IN temp_advisor_first_name varchar(20),
    IN temp_advisor_last_name varchar(20),
    IN temp_advisor_department_name varchar(20)
)
BEGIN
    INSERT INTO student (
        first_name, 
        last_name, 
        department_ID, 
        total_cred, 
        advisor_ID
    )
    VALUES (
        temp_first_name,
        temp_last_name,
        (SELECT department_ID FROM department WHERE department_name = temp_department_name), 
        temp_total_credits,
        (
            SELECT advisor_ID FROM advisor
            WHERE first_name = temp_advisor_first_name
                AND last_name = temp_advisor_last_name
                AND department_ID = (
                    SELECT department_ID FROM department 
                    WHERE department_name = temp_advisor_department_name
                )
        )
    );
END;;

-- Read Students
DROP PROCEDURE IF EXISTS get_students;;
CREATE PROCEDURE get_students()
BEGIN
    SELECT * FROM student;
END;;

-- Update Student
DROP PROCEDURE IF EXISTS update_student;;
CREATE PROCEDURE update_student(
    IN temp_student_ID int,
    IN temp_first_name varchar(20),
    IN temp_last_name varchar(20),
    IN temp_department_name VARCHAR(20),
    IN temp_total_credits NUMERIC (3,0),
    IN temp_advisor_ID int
)
BEGIN
    UPDATE student
    SET first_name = temp_first_name,
        last_name = temp_last_name,
        department_ID = (SELECT department_ID FROM department WHERE department_name = temp_department_name),
        total_cred = temp_total_credits,
        advisor_ID = temp_advisor_ID
    WHERE student_ID = temp_student_ID;
END;;

-- Delete Student
DROP PROCEDURE IF EXISTS delete_student;;
    CREATE PROCEDURE delete_student(
    IN temp_student_ID int
)
BEGIN
    DELETE FROM student
    WHERE  student_ID = temp_student_ID;
END;;

-- -- -- 
-- section CRUD
-- -- --

-- Create Section
DROP PROCEDURE IF EXISTS create_section;;
CREATE PROCEDURE create_section(
    IN temp_course_ID int,
    IN temp_semester VARCHAR(6),
    IN temp_year NUMERIC(4,0),
    IN temp_building_ID int,
    IN temp_time_slot_ID int
)
BEGIN
INSERT INTO section (
    course_ID,
    semester,
    year,
    building_ID,
    time_slot_ID
)
VALUES (
    temp_course_ID,
    temp_semester,
    temp_year,
    temp_building_ID,
    temp_time_slot_ID
);
END;;

-- Read Sections
DROP PROCEDURE IF EXISTS get_sections;;
CREATE PROCEDURE get_sections()
BEGIN
    SELECT * FROM section;
END;;

-- Update Section
DROP PROCEDURE IF EXISTS update_section;;
CREATE PROCEDURE update_section(
    IN temp_section_ID int,
    IN temp_course_ID int,
    IN temp_semester VARCHAR(6),
    IN temp_year NUMERIC(4,0),
    IN temp_building_ID int,
    IN temp_time_slot_ID int
)
BEGIN
UPDATE section
SET building_ID = temp_building_ID,
    time_slot_ID = temp_time_slot_ID
    WHERE course_ID = temp_course_ID
        AND section_ID = temp_section_ID
        AND semester = temp_semester
        AND year = temp_year;
END;;

-- Delete Section
DROP PROCEDURE IF EXISTS delete_section;;
CREATE PROCEDURE delete_section(
    IN temp_course_ID int,
    IN temp_section_ID int,
    IN temp_semester VARCHAR(6),
    IN temp_year NUMERIC(4,0)
)
BEGIN
    DELETE FROM section
    WHERE course_id = temp_course_ID
        AND section_ID = temp_section_ID
        AND semester = temp_semester
        AND year = temp_year;
END;;

-- -- -- 
-- account CRUD
-- -- --

-- Create Account
DROP PROCEDURE IF EXISTS create_account;;
CREATE PROCEDURE create_account(
    IN temp_username varchar(20),
    IN temp_password varchar(200),
    IN temp_role varchar(20)    
)
BEGIN
    INSERT INTO account (username, password, role)
    VALUES (
        temp_username,
        temp_password,
        temp_role
    );
END;;

-- Read Accounts
DROP PROCEDURE IF EXISTS get_accounts;;
CREATE PROCEDURE get_accounts()
BEGIN
    SELECT * FROM account;
END;;   

-- Update Account
DROP PROCEDURE IF EXISTS update_account;;
CREATE PROCEDURE update_account(
    IN temp_account_ID int,
    IN temp_username varchar(20),
    IN temp_password varchar(20),
    IN temp_role varchar(20)
)
BEGIN
UPDATE account
SET username = temp_username,
    password = temp_password,
    role = temp_role
    WHERE account_ID = temp_account_ID;
END;;

-- Delete Account
DROP PROCEDURE IF EXISTS delete_account;;
CREATE PROCEDURE delete_account(
    IN temp_account_ID int
)
BEGIN
    DELETE FROM account
    WHERE account_ID = temp_account_ID;
END;;

-- -- -- 
-- OTHER MAJOR STUFF
-- -- --

-- Enroll In Section
DROP PROCEDURE IF EXISTS enroll_in_section;;
CREATE PROCEDURE enroll_in_section(
    IN temp_student_ID INT,
    IN temp_section_ID INT,
    IN temp_grades VARCHAR(2)
)
BEGIN
    INSERT INTO takes(student_ID, section_ID, grades)
    VALUES (temp_student_ID, temp_section_ID, temp_grades);
END;;

-- Assign Instructor to Section
DROP PROCEDURE IF EXISTS assign_instructor_to_section;;
CREATE PROCEDURE assign_instructor_to_section(
    IN temp_instructor_ID int,
    IN temp_section_ID int
)
BEGIN
    INSERT INTO teaches(instructor_ID, section_ID)
    VALUES (temp_instructor_ID, temp_section_ID);
END;;

-- Drop Section Transaction
DROP PROCEDURE IF EXISTS drop_section;;
CREATE PROCEDURE drop_section(
    IN temp_student_ID int,
    IN temp_section_ID int
)
BEGIN
    DELETE FROM takes
    WHERE section_ID = temp_section_ID
        AND student_ID = temp_student_ID;
END;;

-- Give Grade to Section
DROP PROCEDURE IF EXISTS give_grade_to_section;;
CREATE PROCEDURE give_grade_to_section(
    IN temp_student_ID int,
    IN temp_section_ID int,
    IN temp_grades VARCHAR(2)
)
BEGIN
    UPDATE takes
    SET grades = temp_grades
    WHERE student_ID = temp_student_ID
        AND section_ID = temp_section_ID;
END;;
