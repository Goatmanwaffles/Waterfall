CREATE TABLE IF NOT EXISTS classroom (
    building        VARCHAR(15),
    room_number     VARCHAR(7),
    capacity        NUMERIC(4,0),
    PRIMARY KEY (building, room_number)
);;

CREATE TABLE IF NOT EXISTS department (
    dept_name       VARCHAR(20), 
    building        VARCHAR(15), 
    budget          NUMERIC(12,2) CHECK (budget > 0),
    PRIMARY KEY (dept_name)
);;

CREATE TABLE IF NOT EXISTS time_slot (
    time_slot_ID     INT AUTO_INCREMENT,
    day              VARCHAR(1),
    start_hr         NUMERIC(2) CHECK (start_hr >= 0 and start_hr < 24),
    start_min        NUMERIC(2) CHECK (start_min >= 0 and start_min < 60),
    end_hr           NUMERIC(2) CHECK (end_hr >= 0 and end_hr < 24),
    end_min          NUMERIC(2) CHECK (end_min >= 0 and end_min < 60),
    PRIMARY KEY (time_slot_ID, day, start_hr, start_min)
);;

CREATE TABLE IF NOT EXISTS advisor (
    advisor_ID      INT AUTO_INCREMENT,
    first_name      VARCHAR(20),
    last_name       VARCHAR(20),
    department      VARCHAR(20),
    PRIMARY KEY (advisor_ID),
    FOREIGN KEY (department) REFERENCES department (dept_name)
        ON DELETE SET NULL
);;

CREATE TABLE IF NOT EXISTS course (
    course_ID        INT AUTO_INCREMENT, 
    title            VARCHAR(50), 
    dept_name        VARCHAR(20),
    credits          NUMERIC(2,0) CHECK (credits > 0),
    PRIMARY KEY (course_ID),
    FOREIGN KEY (dept_name) REFERENCES department (dept_name)
        ON DELETE SET NULL
);;

CREATE TABLE IF NOT EXISTS prereq (
    prereq_ID        INT AUTO_INCREMENT,
    course_ID        INT, 
    PRIMARY KEY (prereq_ID, course_ID),
    FOREIGN KEY (course_ID) REFERENCES course (course_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (prereq_ID) REFERENCES course (course_ID)
);;

CREATE TABLE IF NOT EXISTS instructor (
    instructor_ID     INT AUTO_INCREMENT, 
    name              VARCHAR(20) NOT NULL, 
    dept_name         VARCHAR(20), 
    salary            NUMERIC(8,2) CHECK (salary > 29000),
    PRIMARY KEY (instructor_ID),
    FOREIGN KEY (dept_name) REFERENCES department (dept_name)
        ON DELETE SET NULL
);;

CREATE TABLE IF NOT EXISTS section (
    section_ID         INT AUTO_INCREMENT,
    course_ID          INT, 
    semester           VARCHAR(6)
        CHECK (semester in ('Fall', 'Winter', 'Spring', 'Summer')), 
    year               NUMERIC(4,0) CHECK (year > 1701 and year < 2100), 
    building           VARCHAR(15),
    room_number        VARCHAR(7),
    time_slot_ID       INT,
    PRIMARY KEY (section_ID, course_ID, semester, year),
    FOREIGN KEY (course_ID) REFERENCES course (course_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (building, room_number) REFERENCES classroom (building, room_number)
        ON DELETE SET NULL,
    FOREIGN KEY (time_slot_ID) REFERENCES time_slot (time_slot_ID)
        ON DELETE SET NULL
);;

CREATE TABLE IF NOT EXISTS student (
    student_ID      INT AUTO_INCREMENT, 
    first_name      VARCHAR(20) NOT NULL,
    last_name       VARCHAR(20) NOT NULL, 
    dept_name       VARCHAR(20), 
    tot_cred        NUMERIC(3,0) CHECK (tot_cred >= 0),
    advisor_ID      INT,
    PRIMARY KEY (student_ID),
    FOREIGN KEY (dept_name) REFERENCES department (dept_name)
        ON DELETE SET NULL,
    FOREIGN KEY (advisor_ID) REFERENCES advisor (advisor_ID)
        ON DELETE SET NULL
);;

CREATE TABLE IF NOT EXISTS teaches (
    instructor_ID   INT, 
    course_ID       INT,
    section_ID      INT, 
    semester        VARCHAR(6),
    year            NUMERIC(4,0),
    PRIMARY KEY (instructor_ID, course_ID, section_ID, semester, year),
    FOREIGN KEY (course_ID, section_ID, semester, year) REFERENCES section (course_ID, section_ID, semester, year)
        ON DELETE CASCADE,
    FOREIGN KEY (instructor_ID) REFERENCES instructor (instructor_ID)
        ON DELETE CASCADE
);;

CREATE TABLE IF NOT EXISTS takes (
    student_ID       INT, 
    course_ID        INT,
    section_ID       INT, 
    semester         VARCHAR(6),
    year             NUMERIC(4,0),
    grade            VARCHAR(2),
    PRIMARY KEY (student_ID, course_ID, section_ID, semester, year),
    FOREIGN KEY (course_ID, section_ID, semester, year) REFERENCES section (course_ID, section_ID, semester, year)
        ON DELETE CASCADE,
    FOREIGN KEY (student_ID) REFERENCES student (student_ID)
        ON DELETE CASCADE
);;

CREATE TABLE IF NOT EXISTS advises (
    student_ID            INT,
    advisor_ID            INT,
    PRIMARY KEY (student_ID),
    FOREIGN KEY (advisor_ID) REFERENCES advisor (advisor_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (student_ID) REFERENCES student (student_ID)
        ON DELETE CASCADE
);;