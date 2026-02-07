-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 06, 2026 at 06:57 PM
-- Server version: 10.4.10-MariaDB
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `learntoearn`
--

-- --------------------------------------------------------

--
-- Table structure for table `employer_jobposting`
--

DROP TABLE IF EXISTS `employer_jobposting`;
CREATE TABLE IF NOT EXISTS `employer_jobposting` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `job_title` varchar(200) NOT NULL,
  `job_description` longtext NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `posted_date` date NOT NULL,
  `expiry_date` date NOT NULL,
  `salary_range` varchar(100) DEFAULT NULL,
  `employer_id` bigint(20) NOT NULL,
  `hourly_pay` decimal(10,2) DEFAULT NULL,
  `part_time_category` varchar(50) NOT NULL,
  `shift_timing` varchar(100) NOT NULL,
  `working_days` varchar(100) NOT NULL,
  `job_type` varchar(10) NOT NULL,
  `requirements` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `employer_jobposting_employer_id_06838ef5` (`employer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employer_jobposting`
--

INSERT INTO `employer_jobposting` (`id`, `job_title`, `job_description`, `location`, `posted_date`, `expiry_date`, `salary_range`, `employer_id`, `hourly_pay`, `part_time_category`, `shift_timing`, `working_days`, `job_type`, `requirements`) VALUES
(7, 'Junior Python Developer', 'Assist in backend development using Django.', NULL, '2026-02-07', '2026-03-08', '15000-25000', 5, NULL, 'evening', 'Flexible', 'Mon-Fri', 'offline', 'Basic communication skills and enthusiasm.'),
(8, 'UI/UX Designer Intern', 'Design user-friendly interfaces for web apps.', NULL, '2026-02-07', '2026-03-08', '8000-12000', 5, NULL, 'remote', 'Flexible', 'Mon-Fri', 'online', 'Basic communication skills and enthusiasm.'),
(9, 'Store Assistant', 'Manage inventory and assist customers.', NULL, '2026-02-07', '2026-03-08', '400/day', 6, NULL, 'weekend', 'Flexible', 'Sat-Sun', 'offline', 'Basic communication skills and enthusiasm.'),
(10, 'Billing Executive', 'Handle POS transactions.', NULL, '2026-02-07', '2026-03-08', '12000/month', 6, NULL, 'evening', 'Flexible', 'Mon-Fri', 'offline', 'Basic communication skills and enthusiasm.'),
(11, 'Online Math Tutor', 'Teach high school math to students online.', NULL, '2026-02-07', '2026-03-08', '500/hour', 7, NULL, 'flexible', 'Flexible', 'Mon-Fri', 'online', 'Basic communication skills and enthusiasm.');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
