-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 16, 2026 at 09:02 AM
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
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
) ENGINE=MyISAM AUTO_INCREMENT=77 DEFAULT CHARSET=latin1;

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
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add category', 6, 'add_category'),
(22, 'Can change category', 6, 'change_category'),
(23, 'Can delete category', 6, 'delete_category'),
(24, 'Can view category', 6, 'view_category'),
(25, 'Can add district', 7, 'add_district'),
(26, 'Can change district', 7, 'change_district'),
(27, 'Can delete district', 7, 'delete_district'),
(28, 'Can view district', 7, 'view_district'),
(29, 'Can add subcategory', 8, 'add_subcategory'),
(30, 'Can change subcategory', 8, 'change_subcategory'),
(31, 'Can delete subcategory', 8, 'delete_subcategory'),
(32, 'Can view subcategory', 8, 'view_subcategory'),
(33, 'Can add custom user', 9, 'add_customuser'),
(34, 'Can change custom user', 9, 'change_customuser'),
(35, 'Can delete custom user', 9, 'delete_customuser'),
(36, 'Can view custom user', 9, 'view_customuser'),
(37, 'Can add student', 10, 'add_student'),
(38, 'Can change student', 10, 'change_student'),
(39, 'Can delete student', 10, 'delete_student'),
(40, 'Can view student', 10, 'view_student'),
(41, 'Can add employer', 11, 'add_employer'),
(42, 'Can change employer', 11, 'change_employer'),
(43, 'Can delete employer', 11, 'delete_employer'),
(44, 'Can view employer', 11, 'view_employer'),
(45, 'Can add Subscription Plan', 12, 'add_subscriptionplan'),
(46, 'Can change Subscription Plan', 12, 'change_subscriptionplan'),
(47, 'Can delete Subscription Plan', 12, 'delete_subscriptionplan'),
(48, 'Can view Subscription Plan', 12, 'view_subscriptionplan'),
(49, 'Can add Job Posting', 13, 'add_jobposting'),
(50, 'Can change Job Posting', 13, 'change_jobposting'),
(51, 'Can delete Job Posting', 13, 'delete_jobposting'),
(52, 'Can view Job Posting', 13, 'view_jobposting'),
(53, 'Can add application', 14, 'add_application'),
(54, 'Can change application', 14, 'change_application'),
(55, 'Can delete application', 14, 'delete_application'),
(56, 'Can view application', 14, 'view_application'),
(57, 'Can add Location', 15, 'add_location'),
(58, 'Can change Location', 15, 'change_location'),
(59, 'Can delete Location', 15, 'delete_location'),
(60, 'Can view Location', 15, 'view_location'),
(61, 'Can add subscription plan', 16, 'add_subscriptionplan'),
(62, 'Can change subscription plan', 16, 'change_subscriptionplan'),
(63, 'Can delete subscription plan', 16, 'delete_subscriptionplan'),
(64, 'Can view subscription plan', 16, 'view_subscriptionplan'),
(65, 'Can add subscription', 17, 'add_subscription'),
(66, 'Can change subscription', 17, 'change_subscription'),
(67, 'Can delete subscription', 17, 'delete_subscription'),
(68, 'Can view subscription', 17, 'view_subscription'),
(69, 'Can add jobposting', 18, 'add_jobposting'),
(70, 'Can change jobposting', 18, 'change_jobposting'),
(71, 'Can delete jobposting', 18, 'delete_jobposting'),
(72, 'Can view jobposting', 18, 'view_jobposting'),
(73, 'Can add notification', 19, 'add_notification'),
(74, 'Can change notification', 19, 'change_notification'),
(75, 'Can delete notification', 19, 'delete_notification'),
(76, 'Can view notification', 19, 'view_notification');

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
  `user_id` bigint(20) NOT NULL,
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
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'MyApp', 'category'),
(7, 'MyApp', 'district'),
(8, 'MyApp', 'subcategory'),
(9, 'guest', 'customuser'),
(10, 'guest', 'student'),
(11, 'guest', 'employer'),
(12, 'employer', 'subscriptionplan'),
(13, 'employer', 'jobposting'),
(14, 'student', 'application'),
(15, 'MyApp', 'location'),
(16, 'guest', 'subscriptionplan'),
(17, 'guest', 'subscription'),
(18, 'guest', 'jobposting'),
(19, 'guest', 'notification');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'MyApp', '0001_initial', '2026-01-02 09:26:39.706472'),
(2, 'contenttypes', '0001_initial', '2026-01-02 09:26:39.754327'),
(3, 'contenttypes', '0002_remove_content_type_name', '2026-01-02 09:26:39.826549'),
(4, 'auth', '0001_initial', '2026-01-02 09:26:40.106941'),
(5, 'auth', '0002_alter_permission_name_max_length', '2026-01-02 09:26:40.147575'),
(6, 'auth', '0003_alter_user_email_max_length', '2026-01-02 09:26:40.161523'),
(7, 'auth', '0004_alter_user_username_opts', '2026-01-02 09:26:40.175564'),
(8, 'auth', '0005_alter_user_last_login_null', '2026-01-02 09:26:40.188412'),
(9, 'auth', '0006_require_contenttypes_0002', '2026-01-02 09:26:40.193912'),
(10, 'auth', '0007_alter_validators_add_error_messages', '2026-01-02 09:26:40.206050'),
(11, 'auth', '0008_alter_user_username_max_length', '2026-01-02 09:26:40.220178'),
(12, 'auth', '0009_alter_user_last_name_max_length', '2026-01-02 09:26:40.238192'),
(13, 'auth', '0010_alter_group_name_max_length', '2026-01-02 09:26:40.280531'),
(14, 'auth', '0011_update_proxy_permissions', '2026-01-02 09:26:40.298168'),
(15, 'auth', '0012_alter_user_first_name_max_length', '2026-01-02 09:26:40.310262'),
(16, 'guest', '0001_initial', '2026-01-02 09:26:40.776460'),
(17, 'admin', '0001_initial', '2026-01-02 09:26:40.927548'),
(18, 'admin', '0002_logentry_remove_auto_add', '2026-01-02 09:26:40.949005'),
(19, 'admin', '0003_logentry_add_action_flag_choices', '2026-01-02 09:26:40.971353'),
(20, 'employer', '0001_initial', '2026-01-02 09:26:41.156338'),
(21, 'sessions', '0001_initial', '2026-01-02 09:26:41.202786'),
(22, 'student', '0001_initial', '2026-01-02 09:26:41.359749'),
(23, 'employer', '0002_jobposting_skills_required_jobposting_working_hours', '2026-01-02 10:59:22.111499'),
(24, 'MyApp', '0002_location', '2026-01-02 11:05:06.482361'),
(25, 'guest', '0002_student_district_student_location', '2026-01-03 09:39:29.003759'),
(26, 'guest', '0003_remove_student_district_remove_student_location', '2026-01-03 10:02:15.178497'),
(27, 'guest', '0004_student_district', '2026-01-03 10:02:15.282840'),
(28, 'guest', '0005_subscriptionplan_employer_jobs_posted_and_more', '2026-01-03 10:17:58.743218'),
(29, 'employer', '0003_jobposting_is_active_alter_jobposting_location_and_more', '2026-01-06 07:05:04.726974'),
(30, 'guest', '0006_remove_employer_jobs_posted_and_more', '2026-01-06 07:05:05.411502'),
(31, 'student', '0002_application_interview_location_and_more', '2026-01-06 07:07:58.283804'),
(32, 'MyApp', '0003_alter_category_id_alter_district_id_and_more', '2026-01-15 06:10:11.469550'),
(33, 'MyApp', '0004_remove_category_id_remove_district_id_and_more', '2026-01-15 06:10:11.861263'),
(34, 'employer', '0004_remove_jobposting_work_mode_jobposting_hourly_pay_and_more', '2026-01-15 06:10:12.509228'),
(35, 'guest', '0007_customuser_role', '2026-01-15 06:11:45.525389'),
(36, 'guest', '0008_delete_jobposting', '2026-01-15 06:13:26.102634'),
(37, 'guest', '0009_remove_employer_district_employer_area_and_more', '2026-01-15 06:13:49.949116'),
(38, 'guest', '0010_employer_profile_picture_employer_website_and_more', '2026-01-15 06:18:25.952293'),
(39, 'guest', '0011_notification', '2026-01-15 06:18:25.973304'),
(40, 'student', '0003_alter_application_job', '2026-01-15 06:18:51.249937');

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

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('v7nudetf126ztgh4lh5yvf6dlpboxnpa', 'e30:1vd3sp:SLZz4pslV8La4beRsDsXWMv-ovdGKz7_wDiNgdQmE3I', '2026-01-20 10:01:47.243775'),
('e031zc9ouo6y4mrdszn79lr3gxvxkemq', 'e30:1vd3tK:gV4wmG4j3cmhlTKwuOOg1fgDXtHwKxDfRx-VPYLz86Y', '2026-01-20 10:02:18.179133');

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
  `skills_required` longtext NOT NULL,
  `working_hours` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `hourly_pay` decimal(10,2) NOT NULL,
  `part_time_category` varchar(50) NOT NULL,
  `shift_timing` varchar(100) NOT NULL,
  `working_days` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employer_jobposting_employer_id_06838ef5` (`employer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employer_jobposting`
--

INSERT INTO `employer_jobposting` (`id`, `job_title`, `job_description`, `location`, `posted_date`, `expiry_date`, `salary_range`, `employer_id`, `skills_required`, `working_hours`, `is_active`, `hourly_pay`, `part_time_category`, `shift_timing`, `working_days`) VALUES
(2, 'web devolepment', 'this is a great company for you to handle things', 'muvatupuzha', '2026-01-06', '2026-01-21', '20000-30000', 1, 'python,java', 'Part Time', 1, '0.00', 'flexible', 'Flexible', 'Flexible');

-- --------------------------------------------------------

--
-- Table structure for table `employer_subscriptionplan`
--

DROP TABLE IF EXISTS `employer_subscriptionplan`;
CREATE TABLE IF NOT EXISTS `employer_subscriptionplan` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(100) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `price` decimal(8,2) NOT NULL,
  `features` longtext NOT NULL,
  `emp_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employer_subscriptionplan_emp_id_ebb16c81` (`emp_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employer_subscriptionplan`
--

INSERT INTO `employer_subscriptionplan` (`id`, `plan_name`, `start_date`, `end_date`, `price`, `features`, `emp_id`) VALUES
(1, 'sponsor', '2026-01-06', '2026-02-05', '199.00', 'Priority listing, Email support, Verified badge', 1);

-- --------------------------------------------------------

--
-- Table structure for table `guest_customuser`
--

DROP TABLE IF EXISTS `guest_customuser`;
CREATE TABLE IF NOT EXISTS `guest_customuser` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `guest_customuser`
--

INSERT INTO `guest_customuser` (`id`, `password`, `last_login`, `is_superuser`, `name`, `email`, `is_active`, `is_staff`, `role`) VALUES
(5, 'pbkdf2_sha256$600000$Pwda6fZ0wWDzsny7MC9on0$mzOS0KsYpT1uLaPP7z2FnXla2jHCQQrB1RsoUAc+glQ=', NULL, 0, 'Nebin Reji', 'nebinreji2006@gmail.com', 1, 0, 'employer'),
(2, 'pbkdf2_sha256$600000$GEIKEQwjg290lmgsrkLt3N$rCXSVE4wcVYPVmsF3FCci9LDsboZsNy32Frbh5f87uA=', '2026-01-16 08:49:51.033119', 1, 'admin', 'admin@gmail.com', 1, 1, 'admin'),
(4, 'pbkdf2_sha256$600000$7IE2CfFNi9eLyMnet0eTms$IbS8E8v97bSL1hlKMdxuPtPnO/xUp6nbF7Hp4cWdLxk=', NULL, 0, 'Nebin Reji', 'nebinreji2005@gmail.com', 1, 0, 'employer');

-- --------------------------------------------------------

--
-- Table structure for table `guest_customuser_groups`
--

DROP TABLE IF EXISTS `guest_customuser_groups`;
CREATE TABLE IF NOT EXISTS `guest_customuser_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `guest_customuser_groups_customuser_id_group_id_9a6a6d03_uniq` (`customuser_id`,`group_id`),
  KEY `guest_customuser_groups_customuser_id_5be51151` (`customuser_id`),
  KEY `guest_customuser_groups_group_id_8fc7facc` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `guest_customuser_user_permissions`
--

DROP TABLE IF EXISTS `guest_customuser_user_permissions`;
CREATE TABLE IF NOT EXISTS `guest_customuser_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `guest_customuser_user_pe_customuser_id_permission_b56e5a59_uniq` (`customuser_id`,`permission_id`),
  KEY `guest_customuser_user_permissions_customuser_id_07f709c6` (`customuser_id`),
  KEY `guest_customuser_user_permissions_permission_id_7ccbb7eb` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `guest_employer`
--

DROP TABLE IF EXISTS `guest_employer`;
CREATE TABLE IF NOT EXISTS `guest_employer` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `company_name` varchar(200) NOT NULL,
  `contact_person` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` longtext NOT NULL,
  `verification_status` tinyint(1) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `company_logo` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `website` varchar(200) DEFAULT NULL,
  `area` varchar(100) NOT NULL,
  `industry` varchar(100) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `guest_employer`
--

INSERT INTO `guest_employer` (`id`, `company_name`, `contact_person`, `phone`, `email`, `address`, `verification_status`, `user_id`, `company_logo`, `description`, `website`, `area`, `industry`, `profile_picture`) VALUES
(2, 'Alph Tech', 'Nebin Reji', '07012927512', 'nebinreji2006@gmail.com', 'Kottancheril(H),Vazhakulam\r\nVazhakulam P.O', 1, 5, '', 'it is a very great company', NULL, 'Ernakulam', 'IT', '');

-- --------------------------------------------------------

--
-- Table structure for table `guest_student`
--

DROP TABLE IF EXISTS `guest_student`;
CREATE TABLE IF NOT EXISTS `guest_student` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `student_name` varchar(200) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `academic_status` varchar(100) NOT NULL,
  `skills` longtext NOT NULL,
  `id_card` varchar(100) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `district_id` bigint(20) DEFAULT NULL,
  `bio` longtext NOT NULL,
  `portfolio_link` varchar(200) DEFAULT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `resume` varchar(100) DEFAULT NULL,
  `availability` varchar(200) NOT NULL,
  `preferred_roles` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `guest_student_district_id_0618f0d3` (`district_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `myapp_category`
--

DROP TABLE IF EXISTS `myapp_category`;
CREATE TABLE IF NOT EXISTS `myapp_category` (
  `category_name` varchar(100) NOT NULL,
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `myapp_category`
--

INSERT INTO `myapp_category` (`category_name`, `category_id`) VALUES
('IT', 1);

-- --------------------------------------------------------

--
-- Table structure for table `myapp_district`
--

DROP TABLE IF EXISTS `myapp_district`;
CREATE TABLE IF NOT EXISTS `myapp_district` (
  `district_name` varchar(100) NOT NULL,
  `district_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`district_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `myapp_district`
--

INSERT INTO `myapp_district` (`district_name`, `district_id`) VALUES
('Ernakulam', 1);

-- --------------------------------------------------------

--
-- Table structure for table `myapp_location`
--

DROP TABLE IF EXISTS `myapp_location`;
CREATE TABLE IF NOT EXISTS `myapp_location` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `location_name` varchar(100) NOT NULL,
  `district_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `MyApp_location_district_id_27f3f414` (`district_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `myapp_subcategory`
--

DROP TABLE IF EXISTS `myapp_subcategory`;
CREATE TABLE IF NOT EXISTS `myapp_subcategory` (
  `subcategory_name` varchar(100) NOT NULL,
  `category_id` bigint(20) NOT NULL,
  `subcategory_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`subcategory_id`),
  KEY `MyApp_subcategory_category_id_3f4b9d34` (`category_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `student_application`
--

DROP TABLE IF EXISTS `student_application`;
CREATE TABLE IF NOT EXISTS `student_application` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `applied_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `interview_date` datetime(6) DEFAULT NULL,
  `job_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  `interview_location` longtext DEFAULT NULL,
  `interview_mode` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_application_job_id_31dc5ce1` (`job_id`),
  KEY `student_application_student_id_93e05b71` (`student_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student_application`
--

INSERT INTO `student_application` (`id`, `applied_date`, `status`, `interview_date`, `job_id`, `student_id`, `interview_location`, `interview_mode`) VALUES
(1, '2026-01-06 09:37:17.492522', 'pending', NULL, 2, 1, NULL, NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
