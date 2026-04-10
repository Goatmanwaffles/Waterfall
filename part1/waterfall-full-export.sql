-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 10, 2026 at 05:45 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `waterfall`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `assign_instructor_to_section` (IN `temp_instructor_ID` INT, IN `temp_section_ID` INT)   BEGIN
    INSERT INTO teaches(instructor_ID, section_ID)
    VALUES (temp_instructor_ID, temp_section_ID);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_account` (IN `temp_username` VARCHAR(20), IN `temp_password` VARCHAR(20), IN `temp_role` VARCHAR(20))   BEGIN
    INSERT INTO account (username, password, role)
    VALUES (
        temp_username,
        temp_password,
        temp_role
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_instructor` (IN `temp_first_name` VARCHAR(20), IN `temp_last_name` VARCHAR(20), IN `temp_dept_name` VARCHAR(20), IN `temp_salary` NUMERIC(8,2))   BEGIN
    INSERT INTO instructor (first_name, last_name, department_ID, salary)
    VALUES (
        temp_first_name,
        temp_last_name,
        (SELECT department_ID FROM department WHERE department_name = temp_dept_name), 
        temp_salary
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_section` (IN `temp_course_ID` INT, IN `temp_semester` VARCHAR(6), IN `temp_year` NUMERIC(4,0), IN `temp_building_ID` INT, IN `temp_time_slot_ID` INT)   BEGIN
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
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_student` (IN `temp_first_name` VARCHAR(20), IN `temp_last_name` VARCHAR(20), IN `temp_department_name` VARCHAR(20), IN `temp_total_credits` NUMERIC(3,0), IN `temp_advisor_first_name` VARCHAR(20), IN `temp_advisor_last_name` VARCHAR(20), IN `temp_advisor_department_name` VARCHAR(20))   BEGIN
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
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_account` (IN `temp_account_ID` INT)   BEGIN
    DELETE FROM account
    WHERE account_ID = temp_account_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_instructor` (IN `temp_instructor_ID` INT)   BEGIN
    DELETE FROM instructor
    WHERE  instructor_ID = temp_instructor_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_section` (IN `temp_course_ID` INT, IN `temp_section_ID` INT, IN `temp_semester` VARCHAR(6), IN `temp_year` NUMERIC(4,0))   BEGIN
    DELETE FROM section
    WHERE course_id = temp_course_ID
        AND section_ID = temp_section_ID
        AND semester = temp_semester
        AND year = temp_year;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_student` (IN `temp_student_ID` INT)   BEGIN
    DELETE FROM student
    WHERE  student_ID = temp_student_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `drop_section` (IN `temp_student_ID` INT, IN `temp_section_ID` INT)   BEGIN
    DELETE FROM takes
    WHERE section_ID = temp_section_ID
        AND student_ID = temp_student_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `enroll_in_section` (IN `temp_student_ID` INT, IN `temp_section_ID` INT, IN `temp_grades` VARCHAR(2))   BEGIN
    INSERT INTO takes(student_ID, section_ID, grades)
    VALUES (temp_student_ID, temp_section_ID, temp_grades);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_accounts` ()   BEGIN
    SELECT * FROM account;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_instructors` ()   BEGIN
    SELECT * FROM instructor;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_sections` ()   BEGIN
    SELECT * FROM section;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_students` ()   BEGIN
    SELECT * FROM student;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `give_grade_to_section` (IN `temp_student_ID` INT, IN `temp_section_ID` INT, IN `temp_grades` VARCHAR(2))   BEGIN
    UPDATE takes
    SET grades = temp_grades
    WHERE student_ID = temp_student_ID
        AND section_ID = temp_section_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_account` (IN `temp_account_ID` INT, IN `temp_username` VARCHAR(20), IN `temp_password` VARCHAR(20), IN `temp_role` VARCHAR(20))   BEGIN
UPDATE account
SET username = temp_username,
    password = temp_password,
    role = temp_role
    WHERE account_ID = temp_account_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_instructor` (IN `temp_instructor_ID` INT, IN `temp_first_name` VARCHAR(20), IN `temp_last_name` VARCHAR(20), IN `temp_department_name` VARCHAR(20), IN `temp_salary` NUMERIC(8,2))   BEGIN
    UPDATE instructor
    SET first_name = temp_first_name,
        last_name = temp_last_name,
        department_ID = (SELECT department_ID FROM department WHERE department_name = temp_department_name),
        salary = temp_salary
    WHERE instructor_ID = temp_instructor_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_section` (IN `temp_section_ID` INT, IN `temp_course_ID` INT, IN `temp_semester` VARCHAR(6), IN `temp_year` NUMERIC(4,0), IN `temp_building_ID` INT, IN `temp_time_slot_ID` INT)   BEGIN
UPDATE section
SET building_ID = temp_building_ID,
    time_slot_ID = temp_time_slot_ID
    WHERE course_ID = temp_course_ID
        AND section_ID = temp_section_ID
        AND semester = temp_semester
        AND year = temp_year;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_student` (IN `temp_student_ID` INT, IN `temp_first_name` VARCHAR(20), IN `temp_last_name` VARCHAR(20), IN `temp_department_name` VARCHAR(20), IN `temp_total_credits` NUMERIC(3,0), IN `temp_advisor_ID` INT)   BEGIN
    UPDATE student
    SET first_name = temp_first_name,
        last_name = temp_last_name,
        department_ID = (SELECT department_ID FROM department WHERE department_name = temp_department_name),
        total_cred = temp_total_credits,
        advisor_ID = temp_advisor_ID
    WHERE student_ID = temp_student_ID;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `account_ID` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL CHECK (`role` in ('Administrator','Instructor','Student'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`account_ID`, `username`, `password`, `role`) VALUES
(1, 'Link', 'Coolest!', 'Instructor'),
(2, 'coolGuy77', 'FavoriteColor', 'Instructor'),
(3, 'aroddy', 'DrewPass99', 'Instructor'),
(4, 'Drew2000', 'RealDoctor3626', 'Student'),
(5, 'SuperCool', 'Drop73Drop12!', 'Student'),
(6, 'Ganondworf', 'GannonGannon88', 'Student'),
(7, 'Caleb999', 'CalebCalebCaleb', 'Instructor'),
(8, 'dropKick2000', '123892138', 'Student'),
(9, 'OrangeMan', 'TrulyCool2003', 'Instructor'),
(10, 'DrMario', 'Linkus', 'Instructor');

-- --------------------------------------------------------

--
-- Table structure for table `advises`
--

CREATE TABLE `advises` (
  `student_ID` int(11) NOT NULL,
  `advisor_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `advises`
--

INSERT INTO `advises` (`student_ID`, `advisor_ID`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- --------------------------------------------------------

--
-- Table structure for table `advisor`
--

CREATE TABLE `advisor` (
  `advisor_ID` int(11) NOT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `department_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `advisor`
--

INSERT INTO `advisor` (`advisor_ID`, `first_name`, `last_name`, `department_ID`) VALUES
(7, 'Craig', 'Morneweck', 7),
(9, 'Craig', 'Morneweck', 9),
(6, 'Craig', 'Raklovits', 6),
(8, 'Thomas', 'Johnson', 8),
(5, 'Thomas', 'Redy', 5),
(4, 'Thomas', 'So', 4),
(2, 'TJ', 'Raklovits', 2),
(1, 'Tommy', 'Morneweck', 1),
(3, 'Tommy', 'Morneweck', 3),
(10, 'Tommy', 'So', 10);

-- --------------------------------------------------------

--
-- Table structure for table `building`
--

CREATE TABLE `building` (
  `building_ID` int(11) NOT NULL,
  `building_name` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `building`
--

INSERT INTO `building` (`building_ID`, `building_name`) VALUES
(1, 'MSB'),
(2, 'DI'),
(3, 'Smith'),
(4, 'DI'),
(5, 'DI'),
(6, 'MSB'),
(7, 'MSB'),
(8, 'DI'),
(9, 'MSB'),
(10, 'MSB');

-- --------------------------------------------------------

--
-- Table structure for table `classroom`
--

CREATE TABLE `classroom` (
  `classroom_ID` int(11) NOT NULL,
  `building_ID` int(11) DEFAULT NULL,
  `room_number` decimal(3,0) DEFAULT NULL,
  `capacity` decimal(4,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `classroom`
--

INSERT INTO `classroom` (`classroom_ID`, `building_ID`, `room_number`, `capacity`) VALUES
(1, 1, 452, 4449),
(2, 2, 376, 1038),
(3, 3, 7, 8215),
(4, 4, 183, 2498),
(5, 5, 262, 4400),
(6, 6, 51, 4899),
(7, 7, 887, 9607),
(8, 8, 941, 4465),
(9, 9, 881, 890),
(10, 10, 791, 6108);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `course_ID` int(11) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `department_ID` int(11) DEFAULT NULL,
  `credits` decimal(2,0) DEFAULT NULL CHECK (`credits` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`course_ID`, `title`, `department_ID`, `credits`) VALUES
(1, 'Discrete Structures', 1, 59),
(2, 'Discrete Structures', 2, 29),
(3, 'CS1', 3, 92),
(4, 'CS4', 4, 45),
(5, 'Elementary Japanese 1', 5, 84),
(6, 'CS1', 6, 77),
(7, 'CS3', 7, 30),
(8, 'Discrete Structures', 8, 4),
(9, 'Elementary Japanese 1', 9, 42),
(10, 'CS2', 10, 94);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `department_ID` int(11) NOT NULL,
  `department_name` varchar(20) DEFAULT NULL,
  `building_ID` int(11) DEFAULT NULL,
  `budget` decimal(12,2) DEFAULT NULL CHECK (`budget` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`department_ID`, `department_name`, `building_ID`, `budget`) VALUES
(1, 'CS', 1, 2054361050.20),
(2, 'BIO', 2, 1749280865.17),
(3, 'MATH', 3, 7591906070.75),
(4, 'CHEM', 4, 650046354.65),
(5, 'NURS', 5, 5215156452.52),
(6, 'PHYS', 6, 1942310204.19),
(7, 'ENGL', 7, 7041512423.70),
(8, 'FRNC', 8, 8438776297.84),
(9, 'JAPN', 9, 3036567662.30),
(10, 'BOTN', 10, 3625575837.36);

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `instructor_ID` int(11) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `department_ID` int(11) DEFAULT NULL,
  `salary` decimal(8,2) DEFAULT NULL CHECK (`salary` > 29000)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`instructor_ID`, `first_name`, `last_name`, `department_ID`, `salary`) VALUES
(1, 'Javed', 'Nesterenko', 1, 306689.30),
(2, 'Giovanni', 'Kahn', 2, 817203.81),
(3, 'Mikhail', 'Kahn', 3, 661799.66),
(4, 'Javed', 'Nesterenko', 4, 192660.19),
(5, 'Javed', 'Kahn', 5, 830632.83),
(6, 'Javed', 'Nesterenko', 6, 496002.49),
(7, 'Giovanni', 'Kahn', 7, 860395.86),
(8, 'Javed', 'Nesterenko', 8, 394589.39),
(9, 'Javed', 'Phares', 9, 584583.58),
(10, 'Javed', 'Kahn', 10, 199672.19);

-- --------------------------------------------------------

--
-- Table structure for table `prereq`
--

CREATE TABLE `prereq` (
  `prereq_ID` int(11) NOT NULL,
  `base_course_ID` int(11) DEFAULT NULL,
  `requires_course_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prereq`
--

INSERT INTO `prereq` (`prereq_ID`, `base_course_ID`, `requires_course_ID`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6),
(7, 7, 7),
(8, 8, 8),
(9, 9, 9),
(10, 10, 10);

-- --------------------------------------------------------

--
-- Table structure for table `section`
--

CREATE TABLE `section` (
  `section_ID` int(11) NOT NULL,
  `course_ID` int(11) DEFAULT NULL,
  `semester` varchar(6) DEFAULT NULL CHECK (`semester` in ('Fall','Winter','Spring','Summer')),
  `year` decimal(4,0) DEFAULT NULL CHECK (`year` >= 1701 and `year` <= 2100),
  `building_ID` int(11) DEFAULT NULL,
  `time_slot_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section`
--

INSERT INTO `section` (`section_ID`, `course_ID`, `semester`, `year`, `building_ID`, `time_slot_ID`) VALUES
(1, 1, 'Fall', 1966, 1, 1),
(2, 2, 'Winter', 1892, 2, 2),
(3, 3, 'Summer', 2098, 3, 3),
(4, 4, 'Summer', 1993, 4, 4),
(5, 5, 'Winter', 1869, 5, 5),
(6, 6, 'Summer', 2070, 6, 6),
(7, 7, 'Winter', 1719, 7, 7),
(8, 8, 'Summer', 2000, 8, 8),
(9, 9, 'Spring', 1904, 9, 9),
(10, 10, 'Spring', 1967, 10, 10);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `student_ID` int(11) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `department_ID` int(11) DEFAULT NULL,
  `total_cred` decimal(3,0) DEFAULT NULL CHECK (`total_cred` >= 0),
  `advisor_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`student_ID`, `first_name`, `last_name`, `department_ID`, `total_cred`, `advisor_ID`) VALUES
(1, 'Caleb', 'Roddy', 1, 127, 1),
(2, 'Logan', 'Senol', 2, 25, 2),
(3, 'Logan', 'Stanberry', 3, 148, 3),
(4, 'Caleb', 'Senol', 4, 82, 4),
(5, 'Caleb', 'Senol', 5, 105, 5),
(6, 'Logan', 'Senol', 6, 160, 6),
(7, 'Andrew', 'Senol', 7, 217, 7),
(8, 'Logan', 'Stanberry', 8, 161, 8),
(9, 'Caleb', 'Stanberry', 9, 46, 9),
(10, 'Caleb', 'Roddy', 10, 11, 10);

-- --------------------------------------------------------

--
-- Table structure for table `takes`
--

CREATE TABLE `takes` (
  `student_ID` int(11) NOT NULL,
  `section_ID` int(11) NOT NULL,
  `grades` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `takes`
--

INSERT INTO `takes` (`student_ID`, `section_ID`, `grades`) VALUES
(1, 1, 'D-'),
(2, 2, 'D'),
(3, 3, 'B-'),
(4, 4, 'C+'),
(5, 5, 'D+'),
(6, 6, 'B-'),
(7, 7, 'D+'),
(8, 8, 'A'),
(9, 9, 'D+'),
(10, 10, 'C+');

-- --------------------------------------------------------

--
-- Table structure for table `teaches`
--

CREATE TABLE `teaches` (
  `instructor_ID` int(11) NOT NULL,
  `section_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teaches`
--

INSERT INTO `teaches` (`instructor_ID`, `section_ID`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- --------------------------------------------------------

--
-- Table structure for table `time_slot`
--

CREATE TABLE `time_slot` (
  `time_slot_ID` int(11) NOT NULL,
  `day` varchar(1) DEFAULT NULL,
  `start_hr` decimal(2,0) DEFAULT NULL CHECK (`start_hr` >= 0 and `start_hr` < 24),
  `start_min` decimal(2,0) DEFAULT NULL CHECK (`start_min` >= 0 and `start_min` < 60),
  `end_hr` decimal(2,0) DEFAULT NULL CHECK (`end_hr` >= 0 and `end_hr` < 24),
  `end_min` decimal(2,0) DEFAULT NULL CHECK (`end_min` >= 0 and `end_min` < 60)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `time_slot`
--

INSERT INTO `time_slot` (`time_slot_ID`, `day`, `start_hr`, `start_min`, `end_hr`, `end_min`) VALUES
(1, 'T', 8, 56, 14, 56),
(2, 'T', 12, 13, 17, 50),
(3, 'H', 16, 52, 15, 16),
(4, 'M', 13, 46, 11, 54),
(5, 'T', 18, 12, 11, 25),
(6, 'T', 13, 14, 18, 44),
(7, 'H', 10, 13, 13, 36),
(8, 'H', 14, 52, 4, 35),
(9, 'F', 18, 51, 1, 28),
(10, 'W', 23, 42, 20, 28);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`account_ID`),
  ADD UNIQUE KEY `username` (`username`,`password`);

--
-- Indexes for table `advises`
--
ALTER TABLE `advises`
  ADD PRIMARY KEY (`student_ID`),
  ADD KEY `advisor_ID` (`advisor_ID`);

--
-- Indexes for table `advisor`
--
ALTER TABLE `advisor`
  ADD PRIMARY KEY (`advisor_ID`),
  ADD UNIQUE KEY `first_name` (`first_name`,`last_name`,`department_ID`),
  ADD KEY `department_ID` (`department_ID`);

--
-- Indexes for table `building`
--
ALTER TABLE `building`
  ADD PRIMARY KEY (`building_ID`);

--
-- Indexes for table `classroom`
--
ALTER TABLE `classroom`
  ADD PRIMARY KEY (`classroom_ID`),
  ADD KEY `building_ID` (`building_ID`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`course_ID`),
  ADD KEY `department_ID` (`department_ID`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`department_ID`),
  ADD UNIQUE KEY `department_name` (`department_name`),
  ADD KEY `building_ID` (`building_ID`);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`instructor_ID`),
  ADD KEY `department_ID` (`department_ID`);

--
-- Indexes for table `prereq`
--
ALTER TABLE `prereq`
  ADD PRIMARY KEY (`prereq_ID`),
  ADD KEY `base_course_ID` (`base_course_ID`),
  ADD KEY `requires_course_ID` (`requires_course_ID`);

--
-- Indexes for table `section`
--
ALTER TABLE `section`
  ADD PRIMARY KEY (`section_ID`),
  ADD KEY `course_ID` (`course_ID`),
  ADD KEY `building_ID` (`building_ID`),
  ADD KEY `time_slot_ID` (`time_slot_ID`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_ID`),
  ADD KEY `department_ID` (`department_ID`),
  ADD KEY `advisor_ID` (`advisor_ID`);

--
-- Indexes for table `takes`
--
ALTER TABLE `takes`
  ADD PRIMARY KEY (`student_ID`,`section_ID`),
  ADD KEY `section_ID` (`section_ID`);

--
-- Indexes for table `teaches`
--
ALTER TABLE `teaches`
  ADD PRIMARY KEY (`instructor_ID`,`section_ID`),
  ADD KEY `section_ID` (`section_ID`);

--
-- Indexes for table `time_slot`
--
ALTER TABLE `time_slot`
  ADD PRIMARY KEY (`time_slot_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `account_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `advisor`
--
ALTER TABLE `advisor`
  MODIFY `advisor_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `building`
--
ALTER TABLE `building`
  MODIFY `building_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `classroom`
--
ALTER TABLE `classroom`
  MODIFY `classroom_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `course`
--
ALTER TABLE `course`
  MODIFY `course_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `department_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `instructor_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `prereq`
--
ALTER TABLE `prereq`
  MODIFY `prereq_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `section`
--
ALTER TABLE `section`
  MODIFY `section_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `student_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `time_slot`
--
ALTER TABLE `time_slot`
  MODIFY `time_slot_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `advises`
--
ALTER TABLE `advises`
  ADD CONSTRAINT `advises_ibfk_1` FOREIGN KEY (`advisor_ID`) REFERENCES `advisor` (`advisor_ID`) ON DELETE SET NULL,
  ADD CONSTRAINT `advises_ibfk_2` FOREIGN KEY (`student_ID`) REFERENCES `student` (`student_ID`) ON DELETE CASCADE;

--
-- Constraints for table `advisor`
--
ALTER TABLE `advisor`
  ADD CONSTRAINT `advisor_ibfk_1` FOREIGN KEY (`department_ID`) REFERENCES `department` (`department_ID`) ON DELETE SET NULL;

--
-- Constraints for table `classroom`
--
ALTER TABLE `classroom`
  ADD CONSTRAINT `classroom_ibfk_1` FOREIGN KEY (`building_ID`) REFERENCES `building` (`building_ID`) ON DELETE SET NULL;

--
-- Constraints for table `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`department_ID`) REFERENCES `department` (`department_ID`) ON DELETE SET NULL;

--
-- Constraints for table `department`
--
ALTER TABLE `department`
  ADD CONSTRAINT `department_ibfk_1` FOREIGN KEY (`building_ID`) REFERENCES `building` (`building_ID`) ON DELETE SET NULL;

--
-- Constraints for table `instructor`
--
ALTER TABLE `instructor`
  ADD CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`department_ID`) REFERENCES `department` (`department_ID`) ON DELETE SET NULL;

--
-- Constraints for table `prereq`
--
ALTER TABLE `prereq`
  ADD CONSTRAINT `prereq_ibfk_1` FOREIGN KEY (`base_course_ID`) REFERENCES `course` (`course_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `prereq_ibfk_2` FOREIGN KEY (`requires_course_ID`) REFERENCES `course` (`course_ID`) ON DELETE CASCADE;

--
-- Constraints for table `section`
--
ALTER TABLE `section`
  ADD CONSTRAINT `section_ibfk_1` FOREIGN KEY (`course_ID`) REFERENCES `course` (`course_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `section_ibfk_2` FOREIGN KEY (`building_ID`) REFERENCES `building` (`building_ID`) ON DELETE SET NULL,
  ADD CONSTRAINT `section_ibfk_3` FOREIGN KEY (`time_slot_ID`) REFERENCES `time_slot` (`time_slot_ID`) ON DELETE SET NULL;

--
-- Constraints for table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`department_ID`) REFERENCES `department` (`department_ID`) ON DELETE SET NULL,
  ADD CONSTRAINT `student_ibfk_2` FOREIGN KEY (`advisor_ID`) REFERENCES `advisor` (`advisor_ID`) ON DELETE SET NULL;

--
-- Constraints for table `takes`
--
ALTER TABLE `takes`
  ADD CONSTRAINT `takes_ibfk_1` FOREIGN KEY (`student_ID`) REFERENCES `student` (`student_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `takes_ibfk_2` FOREIGN KEY (`section_ID`) REFERENCES `section` (`section_ID`) ON DELETE CASCADE;

--
-- Constraints for table `teaches`
--
ALTER TABLE `teaches`
  ADD CONSTRAINT `teaches_ibfk_1` FOREIGN KEY (`instructor_ID`) REFERENCES `instructor` (`instructor_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `teaches_ibfk_2` FOREIGN KEY (`section_ID`) REFERENCES `section` (`section_ID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
