-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: May 11, 2023 at 08:47 AM
-- Server version: 5.7.32
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_city`
--
CREATE DATABASE IF NOT EXISTS `smart_city` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `smart_city`;

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `id` varchar(36) NOT NULL,
  `vehicleType` varchar(225) NOT NULL,
  `plateNumber` varchar(255) DEFAULT NULL,
  `plateCity` varchar(255) DEFAULT NULL,
  `streamId` varchar(36) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`id`, `vehicleType`, `plateNumber`, `plateCity`, `streamId`, `timestamp`) VALUES
('188238d6-61ff-434e-afa4-8e2aae845ab3', 'motorcycle', '', '', '370192a2-926e-49fe-8c4c-ef2420add6d0', '2023-05-10 02:28:02'),
('1c577f84-8da8-4dbe-a15e-01312e4563ee', 'motorcycle', 'KE1187A', '', '370192a2-926e-49fe-8c4c-ef2420add6d0', '2023-05-10 02:29:14'),
('9618126b-bdd0-4207-bc27-327c6e815818', 'motorcycle', '', '', '370192a2-926e-49fe-8c4c-ef2420add6d0', '2023-05-10 02:29:04'),
('bf4317fd-4830-4a6a-84f4-65e6b311a793', 'motorcycle', '', '', '9b338a7b-94d3-431c-bd93-57e2b5f549e3', '2023-05-10 01:41:53'),
('d7a6ed61-7431-4c64-8f25-a3e6770edcdf', 'motorcycle', 'E5584IJ', 'Kuningan, Cirebon, Majalengka, Indramayu', '370192a2-926e-49fe-8c4c-ef2420add6d0', '2023-05-10 02:28:29'),
('da1d2a54-ad1f-45c8-a47c-9503d14d4504', 'motorcycle', '', '', '0b7637f2-d5a2-42f7-b550-07cd93a12a14', '2023-05-10 02:24:50'),
('deea6e5a-241b-4c1e-8121-08f8ecbd8b29', 'motorcycle', '', '', '370192a2-926e-49fe-8c4c-ef2420add6d0', '2023-05-10 02:28:40');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
