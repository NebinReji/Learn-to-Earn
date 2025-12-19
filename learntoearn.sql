-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 17, 2025 at 05:32 PM
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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=65 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add tbl_districts', 7, 'add_tbl_districts'),
(26, 'Can change tbl_districts', 7, 'change_tbl_districts'),
(27, 'Can delete tbl_districts', 7, 'delete_tbl_districts'),
(28, 'Can view tbl_districts', 7, 'view_tbl_districts'),
(29, 'Can add district', 7, 'add_district'),
(30, 'Can change district', 7, 'change_district'),
(31, 'Can delete district', 7, 'delete_district'),
(32, 'Can view district', 7, 'view_district'),
(33, 'Can add category', 8, 'add_category'),
(34, 'Can change category', 8, 'change_category'),
(35, 'Can delete category', 8, 'delete_category'),
(36, 'Can view category', 8, 'view_category'),
(37, 'Can add subcategory', 9, 'add_subcategory'),
(38, 'Can change subcategory', 9, 'change_subcategory'),
(39, 'Can delete subcategory', 9, 'delete_subcategory'),
(40, 'Can view subcategory', 9, 'view_subcategory'),
(41, 'Can add employer', 10, 'add_employer'),
(42, 'Can change employer', 10, 'change_employer'),
(43, 'Can delete employer', 10, 'delete_employer'),
(44, 'Can view employer', 10, 'view_employer'),
(45, 'Can add employer', 11, 'add_employer'),
(46, 'Can change employer', 11, 'change_employer'),
(47, 'Can delete employer', 11, 'delete_employer'),
(48, 'Can view employer', 11, 'view_employer'),
(49, 'Can add jobposting', 12, 'add_jobposting'),
(50, 'Can change jobposting', 12, 'change_jobposting'),
(51, 'Can delete jobposting', 12, 'delete_jobposting'),
(52, 'Can view jobposting', 12, 'view_jobposting'),
(53, 'Can add student', 13, 'add_student'),
(54, 'Can change student', 13, 'change_student'),
(55, 'Can delete student', 13, 'delete_student'),
(56, 'Can view student', 13, 'view_student'),
(57, 'Can add application', 14, 'add_application'),
(58, 'Can change application', 14, 'change_application'),
(59, 'Can delete application', 14, 'delete_application'),
(60, 'Can view application', 14, 'view_application'),
(61, 'Can add student', 15, 'add_student'),
(62, 'Can change student', 15, 'change_student'),
(63, 'Can delete student', 15, 'delete_student'),
(64, 'Can view student', 15, 'view_student');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'MyApp', 'district'),
(8, 'MyApp', 'category'),
(9, 'MyApp', 'subcategory'),
(10, 'MyApp', 'employer'),
(11, 'guest', 'employer'),
(12, 'guest', 'jobposting'),
(13, 'student', 'student'),
(14, 'student', 'application'),
(15, 'guest', 'student');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'MyApp', '0001_initial', '2025-12-11 11:04:20.405900'),
(2, 'contenttypes', '0001_initial', '2025-12-11 11:04:20.468703'),
(3, 'auth', '0001_initial', '2025-12-11 11:04:21.057000'),
(4, 'admin', '0001_initial', '2025-12-11 11:04:21.193182'),
(5, 'admin', '0002_logentry_remove_auto_add', '2025-12-11 11:04:21.206827'),
(6, 'admin', '0003_logentry_add_action_flag_choices', '2025-12-11 11:04:21.229253'),
(7, 'contenttypes', '0002_remove_content_type_name', '2025-12-11 11:04:21.324562'),
(8, 'auth', '0002_alter_permission_name_max_length', '2025-12-11 11:04:21.368388'),
(9, 'auth', '0003_alter_user_email_max_length', '2025-12-11 11:04:21.415711'),
(10, 'auth', '0004_alter_user_username_opts', '2025-12-11 11:04:21.432346'),
(11, 'auth', '0005_alter_user_last_login_null', '2025-12-11 11:04:21.481891'),
(12, 'auth', '0006_require_contenttypes_0002', '2025-12-11 11:04:21.486597'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2025-12-11 11:04:21.508426'),
(14, 'auth', '0008_alter_user_username_max_length', '2025-12-11 11:04:21.552192'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2025-12-11 11:04:21.601402'),
(16, 'auth', '0010_alter_group_name_max_length', '2025-12-11 11:04:21.648700'),
(17, 'auth', '0011_update_proxy_permissions', '2025-12-11 11:04:21.667342'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2025-12-11 11:04:21.717181'),
(19, 'sessions', '0001_initial', '2025-12-11 11:04:21.762991'),
(20, 'MyApp', '0002_rename_tbl_districts_district', '2025-12-12 01:48:26.265045'),
(21, 'MyApp', '0003_category', '2025-12-12 02:02:45.863849'),
(22, 'MyApp', '0004_subcategory', '2025-12-12 06:02:31.609139'),
(24, 'guest', '0001_initial', '2025-12-17 07:24:55.483490'),
(25, 'MyApp', '0005_employer', '2025-12-17 07:46:34.447968'),
(26, 'guest', '0002_add_jobposting', '2025-12-17 09:03:06.529118'),
(27, 'guest', '0003_add_employer_verification_status', '2025-12-17 09:19:08.617160'),
(28, 'MyApp', '0006_delete_employer', '2025-12-17 09:56:33.074129'),
(29, 'student', '0001_initial', '2025-12-17 09:56:48.650103'),
(30, 'student', '0002_application', '2025-12-17 10:29:38.339832'),
(31, 'student', '0003_alter_application_options_and_more', '2025-12-17 16:59:06.807870'),
(32, 'guest', '0004_student', '2025-12-17 17:01:55.576564');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `guest_employer`
--

DROP TABLE IF EXISTS `guest_employer`;
CREATE TABLE IF NOT EXISTS `guest_employer` (
  `employer_id` int(11) NOT NULL AUTO_INCREMENT,
  `company_name` varchar(200) NOT NULL,
  `contact_person` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` longtext NOT NULL,
  `district_id` int(11) NOT NULL,
  `verification_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`employer_id`),
  KEY `guest_employer_district_id_16824b37` (`district_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `guest_employer`
--

INSERT INTO `guest_employer` (`employer_id`, `company_name`, `contact_person`, `phone`, `email`, `address`, `district_id`, `verification_status`) VALUES
(2, 'student', 'Nebin Reji', '07012927513', 'nebinreji2004@gmail.com', 'bethleham', 5, 0);

-- --------------------------------------------------------

--
-- Table structure for table `guest_jobposting`
--

DROP TABLE IF EXISTS `guest_jobposting`;
CREATE TABLE IF NOT EXISTS `guest_jobposting` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `job_title` varchar(200) NOT NULL,
  `job_description` longtext NOT NULL,
  `location` varchar(100) NOT NULL,
  `work_mode` varchar(50) NOT NULL,
  `posted_date` date NOT NULL,
  `expiry_date` date NOT NULL,
  `salary_range` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `employer_id_id` int(11) NOT NULL,
  PRIMARY KEY (`job_id`),
  KEY `guest_jobposting_employer_id_id_2d7837d5` (`employer_id_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `guest_jobposting`
--

INSERT INTO `guest_jobposting` (`job_id`, `job_title`, `job_description`, `location`, `work_mode`, `posted_date`, `expiry_date`, `salary_range`, `is_active`, `employer_id_id`) VALUES
(1, 'web devolepment', 'web development', 'muvatupuzha', 'online', '2025-12-17', '2025-12-02', '20000-30000', 1, 2),
(2, 'web devolepment', 'web development', 'muvatupuzha', 'online', '2025-12-17', '2025-12-02', '20000-30000', 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `guest_student`
--

DROP TABLE IF EXISTS `guest_student`;
CREATE TABLE IF NOT EXISTS `guest_student` (
  `student_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_name` varchar(200) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `academic_status` varchar(100) NOT NULL,
  `skills` longtext NOT NULL,
  `id_card` varchar(100) NOT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `guest_student`
--

INSERT INTO `guest_student` (`student_id`, `student_name`, `email`, `phone_number`, `academic_status`, `skills`, `id_card`) VALUES
(1, 'nebin', 'nebinreji2004@gmail.com', '345675644322', 'degree', 'reading', 'id_cards/WhatsApp_Image_2025-11-03_at_16.15.53_93414aa8.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `myapp_category`
--

DROP TABLE IF EXISTS `myapp_category`;
CREATE TABLE IF NOT EXISTS `myapp_category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `myapp_category`
--

INSERT INTO `myapp_category` (`category_id`, `category_name`) VALUES
(2, 'Retail');

-- --------------------------------------------------------

--
-- Table structure for table `myapp_district`
--

DROP TABLE IF EXISTS `myapp_district`;
CREATE TABLE IF NOT EXISTS `myapp_district` (
  `district_id` int(11) NOT NULL AUTO_INCREMENT,
  `district_name` varchar(100) NOT NULL,
  PRIMARY KEY (`district_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `myapp_district`
--

INSERT INTO `myapp_district` (`district_id`, `district_name`) VALUES
(5, 'Ernakulam');

-- --------------------------------------------------------

--
-- Table structure for table `myapp_subcategory`
--

DROP TABLE IF EXISTS `myapp_subcategory`;
CREATE TABLE IF NOT EXISTS `myapp_subcategory` (
  `subcategory_id` int(11) NOT NULL AUTO_INCREMENT,
  `subcategory_name` varchar(100) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`subcategory_id`),
  KEY `MyApp_subcategory_category_id_3f4b9d34` (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `myapp_subcategory`
--

INSERT INTO `myapp_subcategory` (`subcategory_id`, `subcategory_name`, `category_id`) VALUES
(1, 'Cashier', 2);

-- --------------------------------------------------------

--
-- Table structure for table `student_application`
--

DROP TABLE IF EXISTS `student_application`;
CREATE TABLE IF NOT EXISTS `student_application` (
  `application_id` int(11) NOT NULL AUTO_INCREMENT,
  `applied_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `job_id_id` int(11) NOT NULL,
  `student_id_id` int(11) NOT NULL,
  `interview_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`application_id`),
  KEY `student_application_job_id_31dc5ce1` (`job_id_id`),
  KEY `student_application_student_id_93e05b71` (`student_id_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
