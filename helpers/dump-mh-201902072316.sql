-- MySQL dump 10.17  Distrib 10.3.12-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: mh
-- ------------------------------------------------------
-- Server version	10.3.12-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `contact_details`
--

DROP TABLE IF EXISTS `contact_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_details` (
  `contact_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `contact_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_details`
--

LOCK TABLES `contact_details` WRITE;
/*!40000 ALTER TABLE `contact_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emails`
--

DROP TABLE IF EXISTS `emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emails` (
  `email_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `contact_id_fk` int(10) unsigned NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`email_id`),
  KEY `emails_contact_details_FK` (`contact_id_fk`),
  CONSTRAINT `emails_contact_details_FK` FOREIGN KEY (`contact_id_fk`) REFERENCES `contact_details` (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails`
--

LOCK TABLES `emails` WRITE;
/*!40000 ALTER TABLE `emails` DISABLE KEYS */;
/*!40000 ALTER TABLE `emails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estates`
--

DROP TABLE IF EXISTS `estates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estates` (
  `estate_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `contact_id_fk` int(10) unsigned NOT NULL,
  `listing_url_id_fk` int(10) unsigned NOT NULL,
  `recorded_on` datetime NOT NULL,
  `recorded_by` varchar(30) NOT NULL,
  `title_estate` varchar(600) DEFAULT NULL,
  `direct_url` varchar(600) NOT NULL,
  PRIMARY KEY (`estate_id`),
  KEY `estates_contact_details_FK` (`contact_id_fk`),
  KEY `estates_listing_urls_FK` (`listing_url_id_fk`),
  CONSTRAINT `estates_contact_details_FK` FOREIGN KEY (`contact_id_fk`) REFERENCES `contact_details` (`contact_id`),
  CONSTRAINT `estates_listing_urls_FK` FOREIGN KEY (`listing_url_id_fk`) REFERENCES `listing_urls` (`listing_url_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estates`
--

LOCK TABLES `estates` WRITE;
/*!40000 ALTER TABLE `estates` DISABLE KEYS */;
/*!40000 ALTER TABLE `estates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `first_listing_urls`
--

DROP TABLE IF EXISTS `first_listing_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `first_listing_urls` (
  `first_listing_url_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `estate_id_fk` int(10) unsigned NOT NULL,
  `first_listing_url` varchar(600) NOT NULL,
  PRIMARY KEY (`first_listing_url_id`),
  KEY `origin_urls_estates_FK` (`estate_id_fk`),
  CONSTRAINT `origin_urls_estates_FK` FOREIGN KEY (`estate_id_fk`) REFERENCES `estates` (`estate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `first_listing_urls`
--

LOCK TABLES `first_listing_urls` WRITE;
/*!40000 ALTER TABLE `first_listing_urls` DISABLE KEYS */;
/*!40000 ALTER TABLE `first_listing_urls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listing_urls`
--

DROP TABLE IF EXISTS `listing_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `listing_urls` (
  `listing_url_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `listing_url` varchar(600) NOT NULL,
  PRIMARY KEY (`listing_url_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listing_urls`
--

LOCK TABLES `listing_urls` WRITE;
/*!40000 ALTER TABLE `listing_urls` DISABLE KEYS */;
/*!40000 ALTER TABLE `listing_urls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phones`
--

DROP TABLE IF EXISTS `phones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phones` (
  `phone_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `contact_id_fk` int(10) unsigned NOT NULL,
  `phone` varchar(50) NOT NULL,
  PRIMARY KEY (`phone_id`),
  KEY `phones_contact_details_FK` (`contact_id_fk`),
  CONSTRAINT `phones_contact_details_FK` FOREIGN KEY (`contact_id_fk`) REFERENCES `contact_details` (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phones`
--

LOCK TABLES `phones` WRITE;
/*!40000 ALTER TABLE `phones` DISABLE KEYS */;
/*!40000 ALTER TABLE `phones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'mh'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-07 23:16:28
