
-- CRUD operations for all major tables

-- -- -- 
-- INSTRUCTOR CRUD
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
    INSERT INTO INSTRUCTOR (first_name, last_name, department_ID, salary)
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
    SELECT * FROM INSTRUCTOR;
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
    UPDATE INSTRUCTOR
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
    DELETE FROM INSTRUCTOR
    WHERE  instructor_ID = temp_instructor_ID;
END;;

-- -- -- 
-- STUDENT CRUD
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
    INSERT INTO STUDENT (
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
    SELECT * FROM STUDENT;
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
    UPDATE STUDENT
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
    DELETE FROM STUDENT
    WHERE  student_ID = temp_student_ID;
END;;

-- -- -- 
-- SECTION CRUD
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
INSERT INTO SECTION (
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
    SELECT * FROM SECTION;
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
UPDATE SECTION
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
    DELETE FROM SECTION
    WHERE course_id = temp_course_ID
        AND section_ID = temp_section_ID
        AND semester = temp_semester
        AND year = temp_year;
END;;

-- Enroll In Section
DROP PROCEDURE IF EXISTS enroll_in_section;;
CREATE PROCEDURE enroll_in_section(
    IN temp_student_ID INT,
    IN temp_section_ID INT,
    IN temp_grades VARCHAR(2)
)
BEGIN
    INSERT INTO TAKES(student_ID, section_ID, grades)
    VALUES (temp_student_ID, temp_section_ID, temp_grades);
END;;

-- Assign Instructor to Section
DROP PROCEDURE IF EXISTS assign_instructor_to_section;;
CREATE PROCEDURE assign_instructor_to_section(
    IN temp_instructor_ID int,
    IN temp_section_ID int
)
BEGIN
    INSERT INTO TEACHES(instructor_ID, section_ID)
    VALUES (temp_instructor_ID, temp_section_ID);
END;;

-- Drop Section Transaction
DROP PROCEDURE IF EXISTS drop_section;;
CREATE PROCEDURE drop_section(
    IN temp_student_ID int,
    IN temp_section_ID int
)
BEGIN
    DELETE FROM TAKES
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
    UPDATE TAKES
    SET grades = temp_grades
    WHERE student_ID = temp_student_ID
        AND section_ID = temp_section_ID;
END;;
