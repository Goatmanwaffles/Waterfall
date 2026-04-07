
-- CRUD operations for all major tables (Stored procedures)

--CRUD Instructor

DELIMITER //
CREATE PROCEDURE create_instructor(
IN id varchar(5),
IN instructor_name varchar(20),
IN department_name VARCHAR(20),
IN salary NUMERIC (8,2)
)
BEGIN
INSERT INTO INSTRUCTOR
VALUES (id, instructor_name, department_name, salary);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_instructors()
BEGIN
SELECT * FROM INSTRUCTOR;
END //
DELIMITER ;

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
END //
DELIMITER ;

CREATE PROCEDURE delete_instructor(
IN instructor_id varchar(5)
)
BEGIN
DELETE FROM INSTRUCTOR
WHERE  id = instructor_id;
END //
DELIMITER ;

--CRUD Student

DELIMITER //
CREATE PROCEDURE create_student(
IN id varchar(5),
IN student_name varchar(20),
IN department_name VARCHAR(20),
IN total_credits NUMERIC (3,0)
)
BEGIN
INSERT INTO STUDENT
VALUES (id, student_name, department_name, total_credits);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_students()
BEGIN
SELECT * FROM STUDENT;
END //
DELIMITER ;

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
END //
DELIMITER ;

CREATE PROCEDURE delete_student(
IN student_id varchar(5)
)
BEGIN
DELETE FROM STUDENT
WHERE  id = student_id;
END //
DELIMITER ;

--CRUDT Section


-- Major transactions e.g. enroll in class, assign instructor to course, drop a section, give a grade to section

