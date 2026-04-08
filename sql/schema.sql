CREATE TABLE IF NOT EXISTS classroom (
    building        varchar(15),
    room_number     varchar(7),
    capacity        numeric(4,0),
    primary key (building, room_number)
);;

CREATE TABLE IF NOT EXISTS department (
    dept_name        varchar(20), 
    building         varchar(15), 
    budget           numeric(12,2) check (budget > 0),
    primary key (dept_name)
);;

CREATE TABLE IF NOT EXISTS time_slot (
    time_slot_ID        int AUTO_INCREMENT,
    day            varchar(1),
    start_hr        numeric(2) check (start_hr >= 0 and start_hr < 24),
    start_min        numeric(2) check (start_min >= 0 and start_min < 60),
    end_hr            numeric(2) check (end_hr >= 0 and end_hr < 24),
    end_min           numeric(2) check (end_min >= 0 and end_min < 60),
    primary key (time_slot_ID, day, start_hr, start_min)
);;

CREATE TABLE IF NOT EXISTS advisor (
    advisor_ID              int AUTO_INCREMENT,
    first_name      varchar(20),
    last_name       varchar(20),
    department      varchar(20),
    primary key (advisor_ID),
    foreign key (department) references department (dept_name)
        on delete set null
);;

CREATE TABLE IF NOT EXISTS course (
    course_ID        int AUTO_INCREMENT, 
    title            varchar(50), 
    dept_name        varchar(20),
    credits          numeric(2,0) check (credits > 0),
    primary key (course_ID),
    foreign key (dept_name) references department (dept_name)
        on delete set null
);;

CREATE TABLE IF NOT EXISTS prereq (
    prereq_ID        int AUTO_INCREMENT,
    course_ID        int, 
    primary key (prereq_ID, course_ID),
    foreign key (course_ID) references course (course_ID)
    on delete cascade,
    foreign key (prereq_ID) references course (course_ID)
);;

ALTER TABLE course ADD COLUMN prereq_ID int;;
ALTER TABLE course ADD FOREIGN KEY (prereq_ID) REFERENCES prereq(prereq_ID);;

CREATE TABLE IF NOT EXISTS instructor (
    instructor_ID                int AUTO_INCREMENT, 
    name              varchar(20) not null, 
    dept_name         varchar(20), 
    salary            numeric(8,2) check (salary > 29000),
    primary key (instructor_ID),
    foreign key (dept_name) references department (dept_name)
    on delete set null
);;

CREATE TABLE IF NOT EXISTS section (
    section_ID             int AUTO_INCREMENT,
    course_ID          int, 
    semester           varchar(6)
    check (semester in ('Fall', 'Winter', 'Spring', 'Summer')), 
    year               numeric(4,0) check (year > 1701 and year < 2100), 
    building           varchar(15),
    room_number        varchar(7),
    time_slot_ID       int,
    primary key (section_ID, course_ID, semester, year),
    foreign key (course_ID) references course (course_ID)
    on delete cascade,
    foreign key (building, room_number) references classroom (building, room_number)
    on delete set null,
    foreign key (time_slot_ID) references time_slot (time_slot_ID)
    on delete set null
);;

CREATE TABLE IF NOT EXISTS student (
    student_ID              int AUTO_INCREMENT, 
    first_name      varchar(20) not null,
    last_name       varchar(20) not null, 
    dept_name       varchar(20), 
    tot_cred        numeric(3,0) check (tot_cred >= 0),
    advisor_ID      int,
    primary key (student_ID),
    foreign key (dept_name) references department (dept_name)
    on delete set null,
    foreign key (advisor_ID) references advisor (advisor_ID)
    on delete set null
);;

CREATE TABLE IF NOT EXISTS teaches (
    instructor_ID   int, 
    course_ID       int,
    section_ID          int, 
    semester        varchar(6),
    year            numeric(4,0),
    primary key (instructor_ID, course_ID, section_ID, semester, year),
    foreign key (course_ID, section_ID, semester, year) references section (course_ID, section_ID, semester, year)
    on delete cascade,
    foreign key (instructor_ID) references instructor (instructor_ID)
    on delete cascade
);;

CREATE TABLE IF NOT EXISTS takes (
    student_ID            int, 
    course_ID        int,
    section_ID            int, 
    semester        varchar(6),
    year            numeric(4,0),
    grade                varchar(2),
    primary key (student_ID, course_ID, section_ID, semester, year),
    foreign key (course_ID, section_ID, semester, year) references section (course_ID, section_ID, semester, year)
    on delete cascade,
    foreign key (student_ID) references student (student_ID)
    on delete cascade
);;

CREATE TABLE IF NOT EXISTS advises (
    student_ID            int,
    advisor_ID            int,
    primary key (student_ID),
    foreign key (advisor_ID) references advisor (advisor_ID)
    on delete set null,
    foreign key (student_ID) references student (student_ID)
    on delete cascade
);;