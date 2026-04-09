
-- CRUD operations for all major tables (Stored procedures)
-- CRUD Instructor
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

DROP PROCEDURE IF EXISTS get_instructors;;
CREATE PROCEDURE get_instructors()
BEGIN
    SELECT * FROM INSTRUCTOR;
END;;

-- DROP PROCEDURE IF EXISTS update_instructor;;
-- CREATE PROCEDURE update_instructor(
--     IN instructor_id int,
--     IN instructor_name varchar(20),
--     IN department_name VARCHAR(20),
--     IN instructor_salary NUMERIC (8,2)
-- )
-- BEGIN
-- UPDATE INSTRUCTOR
-- SET name = instructor_name,
--     dept_name = department_name, 
--     salary = instructor_salary
-- WHERE instructor_ID = instructor_id;
-- END;;

-- DROP PROCEDURE IF EXISTS delete_instructor;;
-- CREATE PROCEDURE delete_instructor(
-- IN instructor_id int
-- )
-- BEGIN
-- DELETE FROM INSTRUCTOR
-- WHERE  instructor_ID = instructor_id;
-- END;;

-- -- CRUD Student
-- DROP PROCEDURE IF EXISTS create_student;;
-- CREATE PROCEDURE create_student(
--     IN id int,
--     IN student_first_name varchar(20),
--     IN student_last_name varchar(20),
--     IN department_name VARCHAR(20),
--     IN total_credits NUMERIC (3,0)
-- )
-- BEGIN
-- INSERT INTO STUDENT (student_ID, first_name, last_name, dept_name, tot_cred)
-- VALUES (id, student_first_name, student_last_name, department_name, total_credits);
-- END;;

-- DROP PROCEDURE IF EXISTS get_students;;
-- CREATE PROCEDURE get_students()
-- BEGIN
-- SELECT * FROM STUDENT;
-- END;;

-- DROP PROCEDURE IF EXISTS update_student;;
-- CREATE PROCEDURE update_student(
--     IN student_id int,
--     IN student_first_name varchar(20),
--     IN student_last_name varchar(20),
--     IN department_name VARCHAR(20),
--     IN total_credits NUMERIC (3,0)
-- )
-- BEGIN
-- UPDATE STUDENT
-- SET first_name = student_first_name,
--     last_name = student_last_name,
--     dept_name = department_name,
--     tot_cred = total_credits
-- WHERE student_ID = student_id;
-- END;;

-- DROP PROCEDURE IF EXISTS delete_student;;
-- CREATE PROCEDURE delete_student(
--     IN student_id int
-- )
-- BEGIN
-- DELETE FROM STUDENT
-- WHERE  student_ID = student_id;
-- END;;


-- DROP PROCEDURE IF EXISTS create_section;;
-- CREATE PROCEDURE create_section(
--     IN section_course_id int,
--     IN section_section_ID int,
--     IN section_semester VARCHAR(6),
--     IN section_year NUMERIC(4,0),
--     IN section_building VARCHAR(15),
--     IN section_room_number VARCHAR(7),
--     IN section_time_slot_id int
-- )
-- BEGIN
-- INSERT INTO SECTION (
--     course_id,
--     section_ID,
--     semester,
--     year,
--     building,
--     room_number,
--     time_slot_id
-- )
-- VALUES (
--     section_course_id,
--     section_section_ID,
--     section_semester,
--     section_year,
--     section_building,
--     section_room_number,
--     section_time_slot_id
-- );
-- END;;

-- DROP PROCEDURE IF EXISTS get_sections;;
-- CREATE PROCEDURE get_sections()
-- BEGIN
-- SELECT * FROM SECTION;
-- END;;

-- DROP PROCEDURE IF EXISTS update_section;;
-- CREATE PROCEDURE update_section(
--     IN section_course_id int,
--     IN section_section_ID int,
--     IN section_semester VARCHAR(6),
--     IN section_year NUMERIC(4,0),
--     IN new_building VARCHAR(15),
--     IN new_room_number VARCHAR(7),
--     IN new_time_slot_id int
-- )
-- BEGIN
-- UPDATE SECTION
-- SET building = new_building,
--     room_number = new_room_number,
--     time_slot_id = new_time_slot_id
-- WHERE course_id = section_course_id
--   AND section_ID = section_section_ID
--   AND semester = section_semester
--   AND year = section_year;
-- END;;

-- DROP PROCEDURE IF EXISTS delete_section;;
-- CREATE PROCEDURE delete_section(
--     IN section_course_id int,
--     IN section_section_ID int,
--     IN section_semester VARCHAR(6),
--     IN section_year NUMERIC(4,0)
-- )
-- BEGIN
-- DELETE FROM SECTION
-- WHERE course_id = section_course_id
--   AND section_ID = section_section_ID
--   AND semester = section_semester
--   AND year = section_year;
-- END;;

-- -- Major transactions e.g. enroll in class, assign instructor to course, drop a section, give a grade to section

-- DROP PROCEDURE IF EXISTS enroll_in_section;;
-- CREATE PROCEDURE enroll_in_section(
--     IN student_id int,
--     IN p_course_id int,
--     IN section_id int,
--     IN section_semester VARCHAR(6),
--     IN section_year NUMERIC(4,0)
-- )
-- BEGIN
-- INSERT INTO TAKES(student_ID, course_ID, section_ID, semester, year, grade)
-- VALUES (student_id, p_course_id, section_id, section_semester, section_year, NULL);
-- END;;

-- DROP PROCEDURE IF EXISTS assign_instructor_to_section;;
-- CREATE PROCEDURE assign_instructor_to_section(
--     IN instructor_id int,
--     IN p_course_id int,
--     IN section_id int,
--     IN section_semester VARCHAR(6),
--     IN section_year NUMERIC(4,0)
-- )
-- BEGIN
-- INSERT INTO TEACHES(instructor_ID, course_ID, section_ID, semester, year)
-- VALUES (instructor_id, p_course_id, section_id, section_semester, section_year);
-- END;;

-- DROP PROCEDURE IF EXISTS drop_section_transaction;;
-- CREATE PROCEDURE drop_section_transaction(
--     IN p_course_id int,
--     IN section_id int,
--     IN section_semester VARCHAR(6),
--     IN section_year NUMERIC(4,0)
-- )
-- BEGIN
-- DELETE FROM SECTION
-- WHERE course_id = p_course_id
--   AND section_ID = section_id
--   AND semester = section_semester
--   AND year = section_year;
-- END;;

-- DROP PROCEDURE IF EXISTS give_grade_to_section;;
-- CREATE PROCEDURE give_grade_to_section(
--     IN student_id int,
--     IN p_course_id int,
--     IN section_id int,
--     IN section_semester VARCHAR(6),
--     IN section_year NUMERIC(4,0),
--     IN section_grade VARCHAR(2)
-- )
-- BEGIN
-- UPDATE TAKES
-- SET grade = section_grade
-- WHERE student_ID = student_id
--   AND course_id = p_course_id
--   AND section_ID = section_id
--   AND semester = section_semester
--   AND year = section_year;
-- END;;
