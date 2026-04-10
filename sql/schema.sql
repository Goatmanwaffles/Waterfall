-- Building
CREATE TABLE IF NOT EXISTS building (
    building_ID INT AUTO_INCREMENT PRIMARY KEY,
    building_name VARCHAR(15)
);;

-- Classroom
CREATE TABLE IF NOT EXISTS classroom (
    clasroom_ID     INT AUTO_INCREMENT PRIMARY KEY,    
    building_ID     INT,
    room_number     NUMERIC(3,0),
    capacity        NUMERIC(4,0),
    FOREIGN KEY (building_ID) REFERENCES building(building_ID)
        ON DELETE SET NULL
);;

-- Department
CREATE TABLE IF NOT EXISTS department (
    department_ID   INT AUTO_INCREMENT PRIMARY KEY,
    department_name       VARCHAR(20) UNIQUE, 
    building_ID        INT, 
    budget          NUMERIC(12,2) CHECK (budget > 0),
    FOREIGN KEY (building_ID) REFERENCES building(building_ID)
        ON DELETE SET NULL
);;

-- Time Slot
CREATE TABLE IF NOT EXISTS time_slot (
    time_slot_ID     INT AUTO_INCREMENT PRIMARY KEY,
    day              VARCHAR(1),
    start_hr         NUMERIC(2) CHECK (start_hr >= 0 and start_hr < 24),
    start_min        NUMERIC(2) CHECK (start_min >= 0 and start_min < 60),
    end_hr           NUMERIC(2) CHECK (end_hr >= 0 and end_hr < 24),
    end_min          NUMERIC(2) CHECK (end_min >= 0 and end_min < 60)
);;

-- Account
CREATE TABLE IF NOT EXISTS account (
    account_ID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    password VARCHAR(20),
    UNIQUE(username, password),
    role VARCHAR(20)
        CHECK (role in ('Administrator', 'Instructor', 'Student'))
);;

-- Advisor
CREATE TABLE IF NOT EXISTS advisor (
    advisor_ID      INT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(20),
    last_name       VARCHAR(20),
    department_ID   INT,
    UNIQUE(first_name, last_name, department_ID), -- Makes sure the queries work
    FOREIGN KEY (department_ID) REFERENCES department(department_ID)
        ON DELETE SET NULL
);;

-- Course
CREATE TABLE IF NOT EXISTS course (
    course_ID        INT AUTO_INCREMENT PRIMARY KEY,
    title            VARCHAR(50), 
    department_ID    INT,
    credits          NUMERIC(2,0) CHECK (credits > 0),
    FOREIGN KEY (department_ID) REFERENCES department(department_ID)
        ON DELETE SET NULL
);;

-- Prereq
CREATE TABLE IF NOT EXISTS prereq (
    prereq_ID        INT AUTO_INCREMENT PRIMARY KEY,
    base_course_ID        INT, 
    requires_course_ID INT,
    FOREIGN KEY (base_course_ID) REFERENCES course(course_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (requires_course_ID) REFERENCES course(course_ID)
        ON DELETE CASCADE
);;

-- Instructor 
CREATE TABLE IF NOT EXISTS instructor (
    instructor_ID     INT AUTO_INCREMENT PRIMARY KEY,
    first_name        VARCHAR(20) NOT NULL,
    last_name         VARCHAR(20) NOT NULL, 
    department_ID     INT,
    salary            NUMERIC(8,2) CHECK (salary > 29000),
    FOREIGN KEY (department_ID) REFERENCES department(department_ID)
        ON DELETE SET NULL
);;

-- Section
CREATE TABLE IF NOT EXISTS section (
    section_ID         INT AUTO_INCREMENT PRIMARY KEY,
    course_ID          INT, 
    semester           VARCHAR(6)
        CHECK (semester in ('Fall', 'Winter', 'Spring', 'Summer')), 
    year               NUMERIC(4,0) CHECK (year >= 1701 and year <= 2100), 
    building_ID        INT,
    time_slot_ID       INT,
    FOREIGN KEY (course_ID) REFERENCES course (course_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (building_ID) REFERENCES classroom (building_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (time_slot_ID) REFERENCES time_slot (time_slot_ID)
        ON DELETE SET NULL
);;

-- Student
CREATE TABLE IF NOT EXISTS student (
    student_ID      INT AUTO_INCREMENT PRIMARY KEY, 
    first_name      VARCHAR(20) NOT NULL,
    last_name       VARCHAR(20) NOT NULL, 
    department_ID   INT,
    total_cred        NUMERIC(3,0) CHECK (total_cred >= 0),
    advisor_ID      INT,
    FOREIGN KEY (department_ID) REFERENCES department(department_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (advisor_ID) REFERENCES advisor (advisor_ID)
        ON DELETE SET NULL
);;

-- Teaches
CREATE TABLE IF NOT EXISTS teaches (
    instructor_ID   INT, 
    section_ID       INT,
    PRIMARY KEY (instructor_ID, section_ID),
    FOREIGN KEY (instructor_ID) REFERENCES instructor(instructor_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (section_ID) REFERENCES section(section_ID)
        ON DELETE CASCADE
);;

-- Takes
CREATE TABLE IF NOT EXISTS takes (
    student_ID       INT, 
    section_ID       INT, 
    grades VARCHAR(2),
    PRIMARY KEY (student_ID, section_ID),
    FOREIGN KEY (student_ID) REFERENCES student(student_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (section_ID) REFERENCES section(section_ID)
        ON DELETE CASCADE
);;

-- Advises
CREATE TABLE IF NOT EXISTS advises (
    student_ID            INT,
    advisor_ID            INT,
    PRIMARY KEY (student_ID),
    FOREIGN KEY (advisor_ID) REFERENCES advisor (advisor_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (student_ID) REFERENCES student (student_ID)
        ON DELETE CASCADE
);;
