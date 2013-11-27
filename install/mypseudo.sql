-- phpMyAdmin SQL Dump
-- version 4.0.8
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 26, 2013 at 08:31 PM
-- Server version: 5.1.66-0+squeeze1
-- PHP Version: 5.3.3-7+squeeze17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `mypseudo`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_callback`(IN `callback_id` INT(0))
    READS SQL DATA
    SQL SECURITY INVOKER
select
mypseudo.callbacks.url as url,
mypseudo.callbacks.id,
mypseudo.callbacks.enabled,
mypseudo.callbacks.callback_url as callbacks_url,
mypseudo.callbacks.script as script,
mypseudo.callbacks.last_update as last_time
from mypseudo.callbacks
where callback_id=mypseudo.callbacks.id
limit 1$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_parser_vars`(IN `callback_id` INT(0))
    READS SQL DATA
    SQL SECURITY INVOKER
select
mypseudo.parser_vars.id as id,
mypseudo.parser_vars.keyword as keyword,
mypseudo.parser_vars.value as value
from mypseudo.parser_vars
where callback_id=mypseudo.parser_vars.callbacks_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_request_vars`(IN `callback_id` INT(0))
    READS SQL DATA
    SQL SECURITY INVOKER
select
mypseudo.request_vars.id as id,
mypseudo.request_vars.keyword as keyword,
mypseudo.request_vars.value as value
from mypseudo.request_vars
where callback_id=mypseudo.request_vars.callbacks_id$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `list_callbacks`()
    READS SQL DATA
    SQL SECURITY INVOKER
select
mypseudo.callbacks.url as url,
mypseudo.callbacks.id,
mypseudo.callbacks.enabled,
mypseudo.callbacks.callback_url as callbacks_url,
mypseudo.callbacks.script as script,
mypseudo.callbacks.last_update as last_time
from mypseudo.callbacks
order by id asc$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `callbacks`
--

CREATE TABLE IF NOT EXISTS `callbacks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(1023) NOT NULL,
  `callback_url` varchar(1023) NOT NULL,
  `script` varchar(255) NOT NULL,
  `last_time` timestamp NULL DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT NULL,
  `period` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=43 ;

-- --------------------------------------------------------

--
-- Table structure for table `callbacks_data`
--

CREATE TABLE IF NOT EXISTS `callbacks_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `callbacks_id` int(11) NOT NULL,
  `keyword` varchar(255) CHARACTER SET latin1 NOT NULL,
  `value` text CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `callback_keyword` (`callbacks_id`,`keyword`),
  KEY `callbacks` (`callbacks_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=19 ;

-- --------------------------------------------------------

--
-- Table structure for table `parser_vars`
--

CREATE TABLE IF NOT EXISTS `parser_vars` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `callbacks_id` int(11) NOT NULL,
  `keyword` varchar(255) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `keyword_callbacks_id` (`callbacks_id`,`keyword`),
  KEY `callbacks` (`callbacks_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=32 ;

-- --------------------------------------------------------

--
-- Table structure for table `request_vars`
--

CREATE TABLE IF NOT EXISTS `request_vars` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `callbacks_id` int(11) NOT NULL,
  `keyword` varchar(255) NOT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `keyword_callbacks_id` (`callbacks_id`,`keyword`),
  KEY `callbacks` (`callbacks_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `callbacks_data`
--
ALTER TABLE `callbacks_data`
  ADD CONSTRAINT `callbacks_data_ibfk_1` FOREIGN KEY (`callbacks_id`) REFERENCES `callbacks` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `parser_vars`
--
ALTER TABLE `parser_vars`
  ADD CONSTRAINT `callbacks_id_foreign_key` FOREIGN KEY (`callbacks_id`) REFERENCES `callbacks` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `request_vars`
--
ALTER TABLE `request_vars`
  ADD CONSTRAINT `callbacks_id_foreign_constraint` FOREIGN KEY (`callbacks_id`) REFERENCES `callbacks` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
