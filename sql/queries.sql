
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
WHERE dept_name = department_name;
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

--CRUDT Section


-- Major transactions e.g. enroll in class, assign instructor to course, drop a section, give a grade to section

