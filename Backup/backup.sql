-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2021 at 05:37 AM
-- Server version: 10.4.16-MariaDB
-- PHP Version: 7.4.12

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
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`staffID`, `username`, `password`) VALUES
('123456789', '123', '123'),
('ASD', '', 'asd'),
('QWE', NULL, 'qwe');

-- --------------------------------------------------------

--
-- Table structure for table `officer`
--

CREATE TABLE `officer` (
  `officerID` varchar(50) NOT NULL,
  `officerName` varchar(50) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  `plateNum` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `officer`
--

INSERT INTO `officer` (`officerID`, `officerName`, `username`, `password`, `rank`, `plateNum`) VALUES
('ZXC', 'ZXC', NULL, 'zxc', 'Korporal', 'zxc');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `staffID` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `plateNum` varchar(50) NOT NULL,
  `vaccinationStatus` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`staffID`, `name`, `plateNum`, `vaccinationStatus`) VALUES
('123456789', 'abc', '', ''),
('ASD', 'asd', 'ASD', 'Unvaccinated'),
('QWE', 'qwe', 'QWE', 'Fully vaccinated');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `studentID` varchar(10) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `year` int(1) DEFAULT NULL,
  `hostelStatus` varchar(20) DEFAULT NULL,
  `plateNum` varchar(20) DEFAULT NULL,
  `vaccinationStatus` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`studentID`, `name`, `year`, `hostelStatus`, `plateNum`, `vaccinationStatus`) VALUES
('ASD', 'ASD', 2, 'Inside UTeM', 'ASD', 'Unvaccinated'),
('b999999999', 'abc', 2, 'campus', 'cab1234', '2 dose');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

CREATE TABLE `vehicle` (
  `plateNum` varchar(10) NOT NULL,
  `vehType` varchar(10) NOT NULL,
  `vehBrand` varchar(20) DEFAULT NULL,
  `vehModel` varchar(20) DEFAULT NULL,
  `roadTaxExpiry` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`plateNum`, `vehType`, `vehBrand`, `vehModel`, `roadTaxExpiry`) VALUES
('AAA1111', 'bike', 'yamaha', 'r15', '2022-12-15'),
('ASD', 'Car', 'ASD', 'ASD', '2021-12-13'),
('CAB1234', 'bike', 'yamaha', 'y15', '2022-12-15'),
('CBA1234', 'car', 'proton', 'saga', '2022-12-15'),
('QWE', 'Bike', 'QWE', 'QWE', '2021-12-14'),
('ZXC', 'Bike', 'ZXC', 'ZXC', '2021-12-13');

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
