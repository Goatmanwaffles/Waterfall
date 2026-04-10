-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 10, 2026 at 05:03 AM
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
    INSERT INTO TEACHES(instructor_ID, section_ID)
    VALUES (temp_instructor_ID, temp_section_ID);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_account` (IN `temp_username` VARCHAR(20), IN `temp_password` VARCHAR(20), IN `temp_role` VARCHAR(20))   BEGIN
    INSERT INTO ACCOUNT (username, password, role)
    VALUES (
        temp_username,
        temp_password,
        temp_role
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_instructor` (IN `temp_first_name` VARCHAR(20), IN `temp_last_name` VARCHAR(20), IN `temp_dept_name` VARCHAR(20), IN `temp_salary` NUMERIC(8,2))   BEGIN
    INSERT INTO INSTRUCTOR (first_name, last_name, department_ID, salary)
    VALUES (
        temp_first_name,
        temp_last_name,
        (SELECT department_ID FROM department WHERE department_name = temp_dept_name), 
        temp_salary
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_section` (IN `temp_course_ID` INT, IN `temp_semester` VARCHAR(6), IN `temp_year` NUMERIC(4,0), IN `temp_building_ID` INT, IN `temp_time_slot_ID` INT)   BEGIN
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
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_student` (IN `temp_first_name` VARCHAR(20), IN `temp_last_name` VARCHAR(20), IN `temp_department_name` VARCHAR(20), IN `temp_total_credits` NUMERIC(3,0), IN `temp_advisor_first_name` VARCHAR(20), IN `temp_advisor_last_name` VARCHAR(20), IN `temp_advisor_department_name` VARCHAR(20))   BEGIN
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
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_account` (IN `temp_account_ID` INT)   BEGIN
    DELETE FROM ACCOUNT
    WHERE account_ID = temp_account_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_instructor` (IN `temp_instructor_ID` INT)   BEGIN
    DELETE FROM INSTRUCTOR
    WHERE  instructor_ID = temp_instructor_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_section` (IN `temp_course_ID` INT, IN `temp_section_ID` INT, IN `temp_semester` VARCHAR(6), IN `temp_year` NUMERIC(4,0))   BEGIN
    DELETE FROM SECTION
    WHERE course_id = temp_course_ID
        AND section_ID = temp_section_ID
        AND semester = temp_semester
        AND year = temp_year;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_student` (IN `temp_student_ID` INT)   BEGIN
    DELETE FROM STUDENT
    WHERE  student_ID = temp_student_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `drop_section` (IN `temp_student_ID` INT, IN `temp_section_ID` INT)   BEGIN
    DELETE FROM TAKES
    WHERE section_ID = temp_section_ID
        AND student_ID = temp_student_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `enroll_in_section` (IN `temp_student_ID` INT, IN `temp_section_ID` INT, IN `temp_grades` VARCHAR(2))   BEGIN
    INSERT INTO TAKES(student_ID, section_ID, grades)
    VALUES (temp_student_ID, temp_section_ID, temp_grades);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_accounts` ()   BEGIN
    SELECT * FROM ACCOUNT;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_instructors` ()   BEGIN
    SELECT * FROM INSTRUCTOR;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_sections` ()   BEGIN
    SELECT * FROM SECTION;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_students` ()   BEGIN
    SELECT * FROM STUDENT;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `give_grade_to_section` (IN `temp_student_ID` INT, IN `temp_section_ID` INT, IN `temp_grades` VARCHAR(2))   BEGIN
    UPDATE TAKES
    SET grades = temp_grades
    WHERE student_ID = temp_student_ID
        AND section_ID = temp_section_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_account` (IN `temp_account_ID` INT, IN `temp_username` VARCHAR(20), IN `temp_password` VARCHAR(20), IN `temp_role` VARCHAR(20))   BEGIN
UPDATE ACCOUNT
SET username = temp_username,
    password = temp_password,
    role = temp_role
    WHERE account_ID = temp_account_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_instructor` (IN `temp_instructor_ID` INT, IN `temp_first_name` VARCHAR(20), IN `temp_last_name` VARCHAR(20), IN `temp_department_name` VARCHAR(20), IN `temp_salary` NUMERIC(8,2))   BEGIN
    UPDATE INSTRUCTOR
    SET first_name = temp_first_name,
        last_name = temp_last_name,
        department_ID = (SELECT department_ID FROM department WHERE department_name = temp_department_name),
        salary = temp_salary
    WHERE instructor_ID = temp_instructor_ID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_section` (IN `temp_section_ID` INT, IN `temp_course_ID` INT, IN `temp_semester` VARCHAR(6), IN `temp_year` NUMERIC(4,0), IN `temp_building_ID` INT, IN `temp_time_slot_ID` INT)   BEGIN
UPDATE SECTION
SET building_ID = temp_building_ID,
    time_slot_ID = temp_time_slot_ID
    WHERE course_ID = temp_course_ID
        AND section_ID = temp_section_ID
        AND semester = temp_semester
        AND year = temp_year;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `update_student` (IN `temp_student_ID` INT, IN `temp_first_name` VARCHAR(20), IN `temp_last_name` VARCHAR(20), IN `temp_department_name` VARCHAR(20), IN `temp_total_credits` NUMERIC(3,0), IN `temp_advisor_ID` INT)   BEGIN
    UPDATE STUDENT
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
(1, 'Drew2000', 'TrulyCool2003', 'Administrator'),
(2, 'Link', 'GannonGannon88', 'Administrator'),
(3, 'dropKick2000', 'CalebCalebCaleb', 'Instructor'),
(4, 'aroddy', 'Coolest!', 'Instructor'),
(5, 'Ganondworf', '123892138', 'Administrator'),
(6, 'OrangeMan', 'Drop73Drop12!', 'Instructor'),
(7, 'SuperCool', 'RealDoctor3626', 'Student'),
(8, 'DrMario', 'Linkus', 'Administrator'),
(9, 'coolGuy77', 'DrewPass99', 'Instructor'),
(10, 'Caleb999', 'FavoriteColor', 'Administrator');

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
(7, 'Craig', 'Raklovits', 7),
(5, 'Craig', 'Smith', 5),
(9, 'Joseph', 'Morneweck', 9),
(1, 'Leah', 'Johnson', 1),
(2, 'Leah', 'Morneweck', 2),
(8, 'Thomas', 'Morneweck', 8),
(6, 'TJ', 'Redy', 6),
(4, 'Tommy', 'Redy', 4),
(10, 'Tommy', 'Smith', 10),
(3, 'Tommy', 'So', 3);

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
(1, 'White'),
(2, 'MSB'),
(3, 'Smith'),
(4, 'DI'),
(5, 'MSB'),
(6, 'DI'),
(7, 'DI'),
(8, 'Smith'),
(9, 'Smith'),
(10, 'White');

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
(1, 1, 819, 6670),
(2, 2, 364, 4059),
(3, 3, 220, 1461),
(4, 4, 193, 9230),
(5, 5, 409, 3178),
(6, 6, 271, 5025),
(7, 7, 547, 1058),
(8, 8, 5, 5406),
(9, 9, 379, 9211),
(10, 10, 447, 7602);

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
(1, 'Elementary Japanese 1', 1, 15),
(2, 'CS2', 2, 87),
(3, 'Elementary Japanese 1', 3, 37),
(4, 'Elementary Japanese 1', 4, 46),
(5, 'Elementary Japanese 1', 5, 94),
(6, 'Discrete Structures', 6, 49),
(7, 'Discrete Structures', 7, 96),
(8, 'CS2', 8, 5),
(9, 'Elementary Japanese 1', 9, 27),
(10, 'Discrete Structures', 10, 41);

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
(1, 'CS', 1, 5464129400.54),
(2, 'BIO', 2, 4539722553.45),
(3, 'MATH', 3, 8515428389.85),
(4, 'CHEM', 4, 5497251449.54),
(5, 'NURS', 5, 2975414960.29),
(6, 'PHYS', 6, 2423345625.24),
(7, 'ENGL', 7, 2679870595.26),
(8, 'FRNC', 8, 8059187066.80),
(9, 'JAPN', 9, 7427061707.74),
(10, 'BOTN', 10, 6808284235.68);

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
(1, 'Giovanni', 'Kahn', 1, 340357.34),
(2, 'Mikhail', 'Nesterenko', 2, 403061.40),
(3, 'Giovanni', 'Nesterenko', 3, 365719.36),
(4, 'Giovanni', 'Phares', 4, 817309.81),
(5, 'Giovanni', 'Phares', 5, 706234.70),
(6, 'Javed', 'Kahn', 6, 526419.52),
(7, 'Mikhail', 'Kahn', 7, 600338.60),
(8, 'Giovanni', 'Kahn', 8, 195888.19),
(9, 'Mikhail', 'Kahn', 9, 814884.81),
(10, 'Javed', 'Kahn', 10, 476612.47);

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
(1, 1, 'Spring', 1971, 1, 1),
(2, 2, 'Spring', 1826, 2, 2),
(3, 3, 'Fall', 1789, 3, 3),
(4, 4, 'Fall', 1895, 4, 4),
(5, 5, 'Winter', 1827, 5, 5),
(6, 6, 'Fall', 1749, 6, 6),
(7, 7, 'Fall', 2038, 7, 7),
(8, 8, 'Summer', 1930, 8, 8),
(9, 9, 'Fall', 1872, 9, 9),
(10, 10, 'Fall', 1762, 10, 10);

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
(1, 'Logan', 'Roddy', 1, 45, 1),
(2, 'Logan', 'Roddy', 2, 227, 2),
(3, 'Andrew', 'Roddy', 3, 163, 3),
(4, 'Logan', 'Roddy', 4, 86, 4),
(5, 'Logan', 'Roddy', 5, 190, 5),
(6, 'Caleb', 'Senol', 6, 106, 6),
(7, 'Caleb', 'Roddy', 7, 71, 7),
(8, 'Caleb', 'Senol', 8, 81, 8),
(9, 'Andrew', 'Roddy', 9, 181, 9),
(10, 'Andrew', 'Stanberry', 10, 237, 10);

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
(1, 1, 'F'),
(2, 2, 'A-'),
(3, 3, 'A+'),
(4, 4, 'B'),
(5, 5, 'B-'),
(6, 6, 'B+'),
(7, 7, 'C+'),
(8, 8, 'B+'),
(9, 9, 'F'),
(10, 10, 'A-');

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
(1, 'W', 20, 58, 2, 33),
(2, 'F', 7, 52, 12, 52),
(3, 'H', 5, 2, 22, 36),
(4, 'F', 13, 39, 14, 7),
(5, 'M', 21, 18, 0, 37),
(6, 'H', 16, 53, 22, 35),
(7, 'M', 11, 45, 15, 13),
(8, 'F', 8, 3, 8, 11),
(9, 'F', 12, 40, 3, 3),
(10, 'F', 20, 38, 17, 49);

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
