-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 12, 2021 at 07:48 AM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `plate_num_rec`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `staffID` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `entry_log`
--

CREATE TABLE `entry_log` (
  `plateNum` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `time` time(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `officer`
--

CREATE TABLE `officer` (
  `officerID` varchar(50) NOT NULL,
  `officerName` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `rank` varchar(50) NOT NULL,
  `plateNum` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `staffID` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `plateNum` varchar(50) NOT NULL,
  `vaccinationStatus` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`staffID`, `name`, `status`, `plateNum`, `vaccinationStatus`) VALUES
('b23456789', 'cba', 'lecturer', 'cba1234', '2 dose');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `studentID` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `year` int(5) NOT NULL,
  `hostelStatus` varchar(50) NOT NULL,
  `plateNum` varchar(50) NOT NULL,
  `vaccinationStatus` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`studentID`, `name`, `year`, `hostelStatus`, `plateNum`, `vaccinationStatus`) VALUES
('b031910126', 'abc', 2, 'campus', 'cab1234', '2 dose'),
('b999999999', 'abc', 2, 'campus', 'cab1234', '2 dose');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

CREATE TABLE `vehicle` (
  `plateNum` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `carBrand` varchar(50) NOT NULL,
  `roadTaxExpiry` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`plateNum`, `name`, `carBrand`, `roadTaxExpiry`) VALUES
('ABC 1234', 'Aniq', 'Saga', '2021-12-16'),
('CAB1234', 'anqib', 'pijot', '2022-12-15');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`staffID`);

--
-- Indexes for table `officer`
--
ALTER TABLE `officer`
  ADD PRIMARY KEY (`officerID`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`staffID`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`studentID`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`plateNum`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
