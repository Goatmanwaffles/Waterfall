
-- CRUD operations for all major tables (Stored procedures)
-- CRUD Instructor
DROP PROCEDURE IF EXISTS create_instructor;;
CREATE PROCEDURE create_instructor (
    IN id VARCHAR(5),
    IN instructor_name VARCHAR(20),
    IN department_name VARCHAR(20),
    IN salary NUMERIC(8,2)
)
BEGIN
    INSERT INTO INSTRUCTOR
    VALUES (id, instructor_name, department_name, salary);
END;;

DROP PROCEDURE IF EXISTS get_instructors;;
CREATE PROCEDURE get_instructors()
BEGIN
SELECT * FROM INSTRUCTOR;
END;;

DROP PROCEDURE IF EXISTS update_instructor;;
CREATE PROCEDURE update_instructor(
IN instructor_id varchar(5),
IN instructor_name varchar(20),
IN department_name VARCHAR(20),
IN instructor_salary NUMERIC (8,2)
)
BEGIN
UPDATE INSTRUCTOR
SET name = instructor_name,
    dept_name = department_name, 
    salary = instructor_salary
WHERE id = instructor_id;
END;;

DROP PROCEDURE IF EXISTS delete_instructor;;
CREATE PROCEDURE delete_instructor(
IN instructor_id varchar(5)
)
BEGIN
DELETE FROM INSTRUCTOR
WHERE  id = instructor_id;
END;;

-- CRUD Student
DROP PROCEDURE IF EXISTS create_student;;
CREATE PROCEDURE create_student(
    IN id varchar(5),
    IN student_name varchar(20),
    IN department_name VARCHAR(20),
    IN total_credits NUMERIC (3,0)
)
BEGIN
INSERT INTO STUDENT
VALUES (id, student_name, department_name, total_credits);
END;;

DROP PROCEDURE IF EXISTS get_students;;
CREATE PROCEDURE get_students()
BEGIN
SELECT * FROM STUDENT;
END;;

DROP PROCEDURE IF EXISTS update_student;;
CREATE PROCEDURE update_student(
    IN student_id varchar(5),
    IN student_name varchar(20),
    IN department_name VARCHAR(20),
    IN total_credits NUMERIC (3,0)
)
BEGIN
UPDATE STUDENT
SET name = student_name,
    dept_name = department_name, 
    tot_cred = total_credits
WHERE id = student_id;
END;;

DROP PROCEDURE IF EXISTS delete_student;;
CREATE PROCEDURE delete_student(
IN student_id varchar(5)
)
BEGIN
DELETE FROM STUDENT
WHERE  id = student_id;
END;;


DROP PROCEDURE IF EXISTS create_section;;
CREATE PROCEDURE create_section(
    IN section_course_id VARCHAR(8),
    IN section_sec_id VARCHAR(8),
    IN section_semester VARCHAR(6),
    IN section_year NUMERIC(4,0),
    IN section_building VARCHAR(15),
    IN section_room_number VARCHAR(7),
    IN section_time_slot_id VARCHAR(4)
)
BEGIN
INSERT INTO SECTION (
    course_id,
    sec_id,
    semester,
    year,
    building,
    room_number,
    time_slot_id
)
VALUES (
    section_course_id,
    section_sec_id,
    section_semester,
    section_year,
    section_building,
    section_room_number,
    section_time_slot_id
);
END;;

DROP PROCEDURE IF EXISTS get_sections;;
CREATE PROCEDURE get_sections()
BEGIN
SELECT * FROM SECTION;
END;;

DROP PROCEDURE IF EXISTS update_section;;
CREATE PROCEDURE update_section(
    IN section_course_id VARCHAR(8),
    IN section_sec_id VARCHAR(8),
    IN section_semester VARCHAR(6),
    IN section_year NUMERIC(4,0),
    IN new_building VARCHAR(15),
    IN new_room_number VARCHAR(7),
    IN new_time_slot_id VARCHAR(4)
)
BEGIN
UPDATE SECTION
SET building = new_building,
    room_number = new_room_number,
    time_slot_id = new_time_slot_id
WHERE course_id = section_course_id
  AND sec_id = section_sec_id
  AND semester = section_semester
  AND year = section_year;
END;;

DROP PROCEDURE IF EXISTS delete_section;;
CREATE PROCEDURE delete_section(
    IN section_course_id VARCHAR(8),
    IN section_sec_id VARCHAR(8),
    IN section_semester VARCHAR(6),
    IN section_year NUMERIC(4,0)
)
BEGIN
DELETE FROM SECTION
WHERE course_id = section_course_id
  AND sec_id = section_sec_id
  AND semester = section_semester
  AND year = section_year;
END;;

-- Major transactions e.g. enroll in class, assign instructor to course, drop a section, give a grade to section

DROP PROCEDURE IF EXISTS enroll_in_section;;
CREATE PROCEDURE enroll_in_section(
    IN student_id VARCHAR(5),
    IN p_course_id INT,
    IN section_id VARCHAR(8),
    IN section_semester VARCHAR(6),
    IN section_year NUMERIC(4,0)
)
BEGIN
INSERT INTO TAKES(ID, course_id, sec_id, semester, year)
VALUES (student_id, p_course_id, section_id, section_semester, section_year);
END;;