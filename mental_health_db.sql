-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 14, 2024 at 07:14 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mental_health_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `mental_health_data`
--

CREATE TABLE `mental_health_data` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `q1` int(11) DEFAULT NULL,
  `q2` int(11) DEFAULT NULL,
  `q3` int(11) DEFAULT NULL,
  `q4` int(11) NOT NULL,
  `q5` int(11) NOT NULL,
  `q6` int(11) NOT NULL,
  `q7` int(11) NOT NULL,
  `q8` int(11) NOT NULL,
  `q9` int(11) NOT NULL,
  `q10` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mental_health_data`
--

INSERT INTO `mental_health_data` (`id`, `user_id`, `q1`, `q2`, `q3`, `q4`, `q5`, `q6`, `q7`, `q8`, `q9`, `q10`, `timestamp`) VALUES
(1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, '2024-10-11 06:01:52'),
(2, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, '2024-10-11 13:34:41'),
(3, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '2024-10-11 13:38:20'),
(5, 1, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, '2024-10-13 17:13:16'),
(6, 1, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, '2024-10-13 17:23:14'),
(7, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, '2024-10-13 17:23:20'),
(8, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, '2024-10-13 17:24:25'),
(9, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2024-10-13 17:27:11'),
(10, 1, 2, 2, 1, 2, 1, 3, 2, 2, 1, 3, '2024-10-13 17:27:57'),
(11, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, '2024-10-13 17:38:00'),
(12, 1, 2, 1, 2, 0, 0, 2, 0, 2, 0, 0, '2024-10-13 18:00:36'),
(13, 1, 2, 1, 2, 0, 0, 2, 0, 2, 1, 3, '2024-10-13 18:01:00'),
(14, 1, 3, 1, 0, 1, 0, 2, 2, 2, 1, 3, '2024-10-14 07:38:31'),
(15, 3, 1, 2, 3, 1, 2, 0, 1, 0, 2, 3, '2024-10-14 07:40:20'),
(16, 1, 2, 1, 0, 0, 2, 1, 2, 0, 2, 3, '2024-10-14 08:40:02');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`) VALUES
(1, 'an', '$pbkdf2-sha256$29000$IKTUujemFELoPcfY29tbCw$xS/9ZTTYRCOjL2WCK4IQ8AlF32bEKmecho6JQZN5UUg'),
(2, 'kak', '$pbkdf2-sha256$29000$cw5hDKFUSgkBIKSUslaKMQ$iv1RYCRg9VpBePX6Vo6ZKZPKyu8WMCQ4L1SqXcY9MXU'),
(3, 'sneha', '$pbkdf2-sha256$29000$aU1pLYWQMkaIMaa0dq5VSg$Eqxa8Xf2KatmDF9JNzSsMpIedinIfzCaOl62knHDSzY');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `mental_health_data`
--
ALTER TABLE `mental_health_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `mental_health_data`
--
ALTER TABLE `mental_health_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `mental_health_data`
--
ALTER TABLE `mental_health_data`
  ADD CONSTRAINT `mental_health_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
