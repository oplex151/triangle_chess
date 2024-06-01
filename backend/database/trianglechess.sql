-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: trianglechess
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appeal`
--

DROP TABLE IF EXISTS `appeal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appeal` (
  `appealId` bigint unsigned NOT NULL AUTO_INCREMENT,
  `userId` bigint unsigned NOT NULL,
  `type` varchar(50) NOT NULL,
  `content` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appealId`),
  KEY `appeal_user_FK` (`userId`),
  CONSTRAINT `appeal_user_FK` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appeal`
--

LOCK TABLES `appeal` WRITE;
/*!40000 ALTER TABLE `appeal` DISABLE KEYS */;
/*!40000 ALTER TABLE `appeal` ENABLE KEYS */;
UNLOCK TABLES;
-- Current Database: `trianglechess`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `trianglechess` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `trianglechess`;

--
-- Table structure for table `appeal`
--

DROP TABLE IF EXISTS `appeal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appeal` (
  `appealId` bigint unsigned NOT NULL AUTO_INCREMENT,
  `userId` bigint unsigned NOT NULL,
  `type` varchar(50) NOT NULL,
  `content` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fromId` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dealed` int NOT NULL DEFAULT '0',
  `feedback` text,
  PRIMARY KEY (`appealId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appeal`
--

LOCK TABLES `appeal` WRITE;
/*!40000 ALTER TABLE `appeal` DISABLE KEYS */;
INSERT INTO `appeal` VALUES (1,4,'1','Bad_behaviour:睡了',NULL,'4',1,'OK'),(2,4,'1','Apeal_bad_report:诱因并','2024-06-01 11:49:43','4',1,'围殴知道了'),(3,4,'1','Bad_bug:大撒大撒','2024-06-01 11:49:46','4',0,NULL),(4,4,'1','Bad_bug:有bug','2024-06-01 12:44:09','4',0,NULL);
/*!40000 ALTER TABLE `appeal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `commentId` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '评论编号',
  `recordId` bigint unsigned NOT NULL COMMENT '对局Id',
  `userId` bigint unsigned NOT NULL COMMENT '发布用户Id',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论信息',
  `likeNum` int unsigned DEFAULT '0' COMMENT '点赞数',
  `commentTime` timestamp NOT NULL COMMENT '评论发表时间',
  PRIMARY KEY (`commentId`),
  KEY `comment_game_record_FK` (`recordId`),
  KEY `comment_user_FK` (`userId`),
  CONSTRAINT `comment_game_record_FK` FOREIGN KEY (`recordId`) REFERENCES `game_record` (`recordId`),
  CONSTRAINT `comment_user_FK` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friend`
--

DROP TABLE IF EXISTS `friend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `friend` (
  `userId` bigint unsigned NOT NULL,
  `friendId` bigint unsigned NOT NULL,
  KEY `firend_user_FK` (`userId`),
  KEY `firend_user_FK_1` (`friendId`),
  CONSTRAINT `firend_user_FK` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`),
  CONSTRAINT `firend_user_FK_1` FOREIGN KEY (`friendId`) REFERENCES `user` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friend`
--

LOCK TABLES `friend` WRITE;
/*!40000 ALTER TABLE `friend` DISABLE KEYS */;
INSERT INTO `friend` VALUES (1,4),(3,4);
/*!40000 ALTER TABLE `friend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_move`
--

DROP TABLE IF EXISTS `game_move`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_move` (
  `moveId` bigint unsigned NOT NULL AUTO_INCREMENT,
  `recordId` bigint unsigned NOT NULL,
  `playerId` bigint unsigned NOT NULL,
  `chessType` varchar(20) NOT NULL,
  `startPos` varchar(10) NOT NULL,
  `endPos` varchar(10) NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`moveId`),
  KEY `recordId` (`recordId`),
  CONSTRAINT `game_move_ibfk_1` FOREIGN KEY (`recordId`) REFERENCES `game_record` (`recordId`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_move`
--

LOCK TABLES `game_move` WRITE;
/*!40000 ALTER TABLE `game_move` DISABLE KEYS */;
INSERT INTO `game_move` VALUES (1,1,1,'piece','7,2,0','1,0,1','2024-05-14 05:56:28'),(2,1,2,'piece','2,0,1','4,2,1','2024-05-14 05:56:40'),(3,1,3,'piece','7,2,2','1,0,0','2024-05-14 05:56:49'),(4,1,1,'piece','1,0,1','4,0,1','2024-05-14 05:56:58'),(5,1,3,'piece','2,3,2','2,4,2','2024-05-14 05:57:12'),(6,1,1,'piece','2,0,0','4,2,0','2024-05-14 05:57:17'),(7,1,3,'piece','1,0,0','4,0,0','2024-05-14 05:57:21'),(8,2,1,'piece','7,2,0','1,0,1','2024-05-14 06:06:12'),(9,2,2,'piece','2,0,1','4,2,1','2024-05-14 06:06:18'),(10,2,3,'piece','7,2,2','1,0,0','2024-05-14 06:06:24'),(11,2,1,'piece','1,0,1','4,0,1','2024-05-14 06:06:29'),(12,2,3,'piece','2,3,2','2,4,2','2024-05-14 06:06:47'),(13,2,1,'piece','2,0,0','4,2,0','2024-05-14 06:06:50'),(14,2,3,'piece','1,0,0','4,0,0','2024-05-14 06:06:54'),(15,3,1,'piece','7,2,0','1,0,1','2024-05-14 06:12:32'),(16,3,2,'piece','2,0,1','4,2,1','2024-05-14 06:12:35'),(17,3,3,'piece','7,2,2','1,0,0','2024-05-14 06:12:39'),(18,3,1,'piece','1,0,1','4,0,1','2024-05-14 06:12:44'),(19,3,3,'piece','2,3,2','2,4,2','2024-05-14 06:12:52'),(20,3,1,'piece','2,0,0','4,2,0','2024-05-14 06:12:55'),(21,3,3,'piece','1,0,0','4,0,0','2024-05-14 06:12:59'),(22,4,1,'piece','1,2,0','7,0,2','2024-05-14 12:58:56'),(23,4,3,'piece','1,2,1','7,0,0','2024-05-14 12:59:03'),(24,4,2,'piece','6,0,2','4,2,2','2024-05-14 12:59:08'),(25,4,1,'piece','7,0,2','4,0,2','2024-05-14 12:59:11'),(26,4,3,'piece','2,3,1','2,4,1','2024-05-14 12:59:21'),(27,4,1,'piece','6,0,0','4,2,0','2024-05-14 12:59:24'),(28,4,3,'piece','7,0,0','4,0,0','2024-05-14 12:59:26'),(29,5,1,'piece','1,2,0','7,0,2','2024-05-14 13:00:18'),(30,5,3,'piece','1,2,1','7,0,0','2024-05-14 13:00:27'),(31,5,2,'piece','6,0,2','4,2,2','2024-05-14 13:00:30'),(32,5,1,'piece','7,0,2','4,0,2','2024-05-14 13:00:32'),(33,5,3,'piece','2,3,1','2,4,1','2024-05-14 13:00:35'),(34,5,1,'piece','6,0,0','4,2,0','2024-05-14 13:00:40'),(35,5,3,'piece','7,0,0','4,0,0','2024-05-14 13:00:41'),(36,51,6,'piece','1,2,0','7,0,2','2024-05-21 14:06:58'),(37,51,4,'piece','0,3,1','0,4,1','2024-05-21 14:07:01'),(38,51,5,'piece','7,2,2','7,4,2','2024-05-21 14:07:04'),(39,51,6,'piece','0,3,0','0,4,0','2024-05-21 14:07:08'),(40,51,4,'piece','1,2,1','7,0,0','2024-05-21 14:07:13'),(41,51,5,'piece','2,3,2','2,4,2','2024-05-21 14:07:16'),(42,51,6,'piece','2,3,0','2,4,0','2024-05-21 14:07:32'),(43,51,4,'piece','2,3,1','2,4,1','2024-05-21 14:07:36'),(44,51,5,'piece','1,2,2','7,0,1','2024-05-21 14:07:37'),(45,51,6,'piece','6,0,0','4,2,0','2024-05-21 14:07:44'),(46,51,4,'piece','7,0,0','4,0,0','2024-05-21 14:07:45'),(47,51,5,'piece','6,0,2','4,2,2','2024-05-21 14:07:51'),(48,51,4,'piece','6,0,1','4,2,1','2024-05-21 14:08:01'),(49,51,5,'piece','7,0,1','4,0,1','2024-05-21 14:08:03'),(50,52,4,'Leader','4,0,0','4,1,0','2024-06-01 03:31:37'),(51,58,4,'Leader','4,0,0','4,1,0','2024-06-01 04:07:41'),(52,68,4,'Gun','7,2,0','7,3,0','2024-06-01 04:50:12'),(53,68,5,'Soilder','6,3,1','6,4,1','2024-06-01 04:50:50'),(54,69,4,'Gun','7,2,0','7,3,0','2024-06-01 04:53:52'),(55,100,6,'Leader','4,0,0','4,1,0','2024-06-01 06:22:37'),(56,100,5,'Gun','7,2,1','1,3,0','2024-06-01 06:22:40'),(57,100,4,'Gun','7,2,2','1,0,1','2024-06-01 06:22:42'),(58,100,6,'Gun','1,2,0','7,0,1','2024-06-01 06:22:46'),(59,100,5,'Bishop','2,0,1','4,2,1','2024-06-01 06:22:49'),(60,100,4,'Gun','1,0,1','4,0,1','2024-06-01 06:22:52'),(61,100,6,'Soilder','2,3,0','2,4,0','2024-06-01 06:23:02'),(62,101,6,'Gun','7,2,0','1,0,2','2024-06-01 06:26:01'),(63,101,5,'WarHorse','1,0,1','2,2,1','2024-06-01 06:26:05'),(64,101,4,'Bishop','2,0,2','4,2,2','2024-06-01 06:26:08'),(65,101,6,'Gun','1,0,2','4,0,2','2024-06-01 06:26:11'),(66,102,4,'Gun','7,2,0','1,0,2','2024-06-01 06:30:26'),(67,102,6,'Gun','7,2,1','7,4,1','2024-06-01 06:30:28'),(68,102,5,'Bishop','2,0,2','4,2,2','2024-06-01 06:30:30'),(69,102,4,'Gun','1,0,2','4,0,2','2024-06-01 06:30:34'),(70,103,4,'Gun','7,2,0','1,0,2','2024-06-01 06:33:35'),(71,103,6,'WarHorse','1,0,1','2,2,1','2024-06-01 06:33:37'),(72,103,5,'Bishop','2,0,2','4,2,2','2024-06-01 06:33:39'),(73,103,4,'Gun','1,0,2','4,0,2','2024-06-01 06:33:41'),(74,103,6,'Bishop','2,0,1','4,2,1','2024-06-01 06:33:49'),(75,103,4,'Bishop','2,0,0','4,2,0','2024-06-01 06:33:58'),(76,103,6,'Gun','7,2,1','1,0,0','2024-06-01 06:34:02'),(77,103,4,'Bishop','4,2,0','2,4,0','2024-06-01 06:34:04'),(78,103,6,'Gun','1,0,0','4,0,0','2024-06-01 06:34:06'),(79,104,5,'Gun','7,2,0','1,0,2','2024-06-01 06:34:50'),(80,104,6,'Bishop','2,0,1','4,2,1','2024-06-01 06:34:52'),(81,104,4,'Bishop','2,0,2','4,2,2','2024-06-01 06:34:54'),(82,104,5,'Gun','1,0,2','4,0,2','2024-06-01 06:34:56'),(83,104,6,'Advisor','3,0,1','4,1,1','2024-06-01 06:34:59'),(84,104,5,'Gun','1,2,0','7,0,1','2024-06-01 06:35:07'),(85,104,6,'Bishop','6,0,1','8,2,1','2024-06-01 06:35:12'),(86,104,5,'Gun','7,0,1','4,0,1','2024-06-01 06:35:16');
/*!40000 ALTER TABLE `game_move` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_record`
--

DROP TABLE IF EXISTS `game_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_record` (
  `recordId` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '对局编号',
  `p1` bigint unsigned NOT NULL COMMENT '1号用户id',
  `p2` bigint unsigned NOT NULL COMMENT '2号用户id',
  `p3` bigint unsigned NOT NULL COMMENT '3号用户id',
  `startTime` timestamp NOT NULL COMMENT '对局开始时间',
  `endTime` timestamp NULL DEFAULT NULL COMMENT '对局结束时间',
  `winner` bigint unsigned DEFAULT NULL COMMENT '对局获胜者id',
  `likeNum` int unsigned DEFAULT '0' COMMENT '点赞数',
  `commentNum` int unsigned DEFAULT '0' COMMENT '评论数',
  PRIMARY KEY (`recordId`),
  KEY `game_record_user_FK` (`p1`),
  KEY `game_record_user_FK_1` (`p2`),
  KEY `game_record_user_FK_2` (`p3`),
  KEY `game_record_user_FK_3` (`winner`),
  CONSTRAINT `game_record_user_FK` FOREIGN KEY (`p1`) REFERENCES `user` (`userId`),
  CONSTRAINT `game_record_user_FK_1` FOREIGN KEY (`p2`) REFERENCES `user` (`userId`),
  CONSTRAINT `game_record_user_FK_2` FOREIGN KEY (`p3`) REFERENCES `user` (`userId`),
  CONSTRAINT `game_record_user_FK_3` FOREIGN KEY (`winner`) REFERENCES `user` (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_record`
--

LOCK TABLES `game_record` WRITE;
/*!40000 ALTER TABLE `game_record` DISABLE KEYS */;
INSERT INTO `game_record` VALUES (1,1,2,3,'2024-05-14 05:53:45','2024-05-14 05:57:22',3,0,0),(2,1,2,3,'2024-05-14 06:05:11',NULL,NULL,0,0),(3,1,2,3,'2024-05-14 06:11:06',NULL,NULL,0,0),(4,1,3,2,'2024-05-14 12:58:45','2024-05-14 12:59:27',3,0,0),(5,1,3,2,'2024-05-14 13:00:13','2024-05-14 13:00:42',3,0,0),(6,4,5,6,'2024-05-15 15:55:34',NULL,NULL,0,0),(7,4,5,6,'2024-05-15 15:57:35',NULL,NULL,0,0),(8,6,5,4,'2024-05-15 16:01:54',NULL,NULL,0,0),(9,5,4,6,'2024-05-15 16:07:21',NULL,NULL,0,0),(10,5,4,6,'2024-05-15 16:09:10',NULL,NULL,0,0),(11,4,5,6,'2024-05-15 16:14:17','2024-05-15 16:14:42',4,0,0),(12,6,5,4,'2024-05-15 16:15:04',NULL,NULL,0,0),(13,6,5,4,'2024-05-15 16:16:56',NULL,NULL,0,0),(14,5,6,4,'2024-05-15 16:18:55',NULL,NULL,0,0),(15,4,5,6,'2024-05-15 16:24:31','2024-05-15 16:24:34',5,0,0),(16,6,5,4,'2024-05-15 16:25:05',NULL,NULL,0,0),(17,6,5,4,'2024-05-15 16:25:12',NULL,NULL,0,0),(18,4,5,6,'2024-05-15 16:25:44',NULL,NULL,0,0),(19,4,5,6,'2024-05-15 16:30:32','2024-05-15 16:30:34',5,0,0),(20,4,5,6,'2024-05-15 16:31:14',NULL,NULL,0,0),(21,5,4,6,'2024-05-15 16:34:11','2024-05-15 16:34:13',5,0,0),(22,6,5,4,'2024-05-15 16:34:20','2024-05-15 16:34:24',5,0,0),(23,4,5,6,'2024-05-15 16:35:27','2024-05-15 16:35:31',6,0,0),(24,4,5,6,'2024-05-15 16:44:05','2024-05-15 16:44:36',6,0,0),(25,5,4,6,'2024-05-15 16:44:53',NULL,NULL,0,0),(26,4,5,6,'2024-05-15 16:52:15','2024-05-15 16:52:18',6,0,0),(27,6,5,4,'2024-05-15 16:52:39','2024-05-15 16:52:42',5,0,0),(28,5,6,4,'2024-05-16 02:29:22',NULL,NULL,0,0),(29,5,4,6,'2024-05-16 02:36:09',NULL,NULL,0,0),(30,5,6,4,'2024-05-16 02:48:22',NULL,NULL,0,0),(31,4,5,6,'2024-05-16 02:52:47','2024-05-16 02:52:56',5,0,0),(32,5,4,6,'2024-05-16 02:53:05',NULL,NULL,0,0),(33,4,5,6,'2024-05-16 03:03:05','2024-05-16 03:03:09',5,0,0),(34,4,5,6,'2024-05-16 03:04:48','2024-05-16 03:04:50',5,0,0),(35,4,5,6,'2024-05-16 03:07:49','2024-05-16 03:07:52',4,0,0),(36,4,5,6,'2024-05-16 03:10:55','2024-05-16 03:10:57',5,0,0),(37,4,5,6,'2024-05-16 03:12:05','2024-05-16 03:12:07',4,0,0),(38,4,5,6,'2024-05-16 03:42:45','2024-05-16 03:42:47',6,0,0),(39,5,4,6,'2024-05-21 13:33:23','2024-05-21 13:33:23',NULL,0,0),(40,5,4,6,'2024-05-21 13:34:55','2024-05-21 13:34:55',NULL,0,0),(41,5,4,6,'2024-05-21 13:35:41','2024-05-21 13:35:41',NULL,0,0),(42,5,4,6,'2024-05-21 13:37:20','2024-05-21 13:37:20',NULL,0,0),(43,5,4,6,'2024-05-21 13:37:33','2024-05-21 13:37:33',NULL,0,0),(44,5,4,6,'2024-05-21 13:37:53','2024-05-21 13:37:53',NULL,0,0),(45,6,4,5,'2024-05-21 13:39:54','2024-05-21 13:39:54',NULL,0,0),(46,5,4,6,'2024-05-21 13:43:44','2024-05-21 13:43:44',NULL,0,0),(47,5,4,6,'2024-05-21 13:44:50','2024-05-21 13:44:50',NULL,0,0),(48,5,4,6,'2024-05-21 13:45:42','2024-05-21 13:45:42',NULL,0,0),(49,4,5,6,'2024-05-21 14:01:17','2024-05-21 14:01:17',NULL,0,0),(50,5,4,6,'2024-05-21 14:04:49','2024-05-21 14:04:49',NULL,0,0),(51,6,4,5,'2024-05-21 14:06:36','2024-05-21 14:08:03',5,0,0),(52,1,2,3,'2024-06-01 08:07:39','2024-06-01 08:07:46',3,0,0);
INSERT INTO `game_record` VALUES (1,1,2,3,'2024-05-14 05:53:45','2024-05-14 05:57:22',3,0,0),(2,1,2,3,'2024-05-14 06:05:11',NULL,NULL,0,0),(3,1,2,3,'2024-05-14 06:11:06',NULL,NULL,0,0),(4,1,3,2,'2024-05-14 12:58:45','2024-05-14 12:59:27',3,0,0),(5,1,3,2,'2024-05-14 13:00:13','2024-05-14 13:00:42',3,0,0),(6,4,5,6,'2024-05-15 15:55:34',NULL,NULL,0,0),(7,4,5,6,'2024-05-15 15:57:35',NULL,NULL,0,0),(8,6,5,4,'2024-05-15 16:01:54',NULL,NULL,0,0),(9,5,4,6,'2024-05-15 16:07:21',NULL,NULL,0,0),(10,5,4,6,'2024-05-15 16:09:10',NULL,NULL,0,0),(11,4,5,6,'2024-05-15 16:14:17','2024-05-15 16:14:42',4,0,0),(12,6,5,4,'2024-05-15 16:15:04',NULL,NULL,0,0),(13,6,5,4,'2024-05-15 16:16:56',NULL,NULL,0,0),(14,5,6,4,'2024-05-15 16:18:55',NULL,NULL,0,0),(15,4,5,6,'2024-05-15 16:24:31','2024-05-15 16:24:34',5,0,0),(16,6,5,4,'2024-05-15 16:25:05',NULL,NULL,0,0),(17,6,5,4,'2024-05-15 16:25:12',NULL,NULL,0,0),(18,4,5,6,'2024-05-15 16:25:44',NULL,NULL,0,0),(19,4,5,6,'2024-05-15 16:30:32','2024-05-15 16:30:34',5,0,0),(20,4,5,6,'2024-05-15 16:31:14',NULL,NULL,0,0),(21,5,4,6,'2024-05-15 16:34:11','2024-05-15 16:34:13',5,0,0),(22,6,5,4,'2024-05-15 16:34:20','2024-05-15 16:34:24',5,0,0),(23,4,5,6,'2024-05-15 16:35:27','2024-05-15 16:35:31',6,0,0),(24,4,5,6,'2024-05-15 16:44:05','2024-05-15 16:44:36',6,0,0),(25,5,4,6,'2024-05-15 16:44:53',NULL,NULL,0,0),(26,4,5,6,'2024-05-15 16:52:15','2024-05-15 16:52:18',6,0,0),(27,6,5,4,'2024-05-15 16:52:39','2024-05-15 16:52:42',5,0,0),(28,5,6,4,'2024-05-16 02:29:22',NULL,NULL,0,0),(29,5,4,6,'2024-05-16 02:36:09',NULL,NULL,0,0),(30,5,6,4,'2024-05-16 02:48:22',NULL,NULL,0,0),(31,4,5,6,'2024-05-16 02:52:47','2024-05-16 02:52:56',5,0,0),(32,5,4,6,'2024-05-16 02:53:05',NULL,NULL,0,0),(33,4,5,6,'2024-05-16 03:03:05','2024-05-16 03:03:09',5,0,0),(34,4,5,6,'2024-05-16 03:04:48','2024-05-16 03:04:50',5,0,0),(35,4,5,6,'2024-05-16 03:07:49','2024-05-16 03:07:52',4,0,0),(36,4,5,6,'2024-05-16 03:10:55','2024-05-16 03:10:57',5,0,0),(37,4,5,6,'2024-05-16 03:12:05','2024-05-16 03:12:07',4,0,0),(38,4,5,6,'2024-05-16 03:42:45','2024-05-16 03:42:47',6,0,0),(39,5,4,6,'2024-05-21 13:33:23','2024-05-21 13:33:23',NULL,0,0),(40,5,4,6,'2024-05-21 13:34:55','2024-05-21 13:34:55',NULL,0,0),(41,5,4,6,'2024-05-21 13:35:41','2024-05-21 13:35:41',NULL,0,0),(42,5,4,6,'2024-05-21 13:37:20','2024-05-21 13:37:20',NULL,0,0),(43,5,4,6,'2024-05-21 13:37:33','2024-05-21 13:37:33',NULL,0,0),(44,5,4,6,'2024-05-21 13:37:53','2024-05-21 13:37:53',NULL,0,0),(45,6,4,5,'2024-05-21 13:39:54','2024-05-21 13:39:54',NULL,0,0),(46,5,4,6,'2024-05-21 13:43:44','2024-05-21 13:43:44',NULL,0,0),(47,5,4,6,'2024-05-21 13:44:50','2024-05-21 13:44:50',NULL,0,0),(48,5,4,6,'2024-05-21 13:45:42','2024-05-21 13:45:42',NULL,0,0),(49,4,5,6,'2024-05-21 14:01:17','2024-05-21 14:01:17',NULL,0,0),(50,5,4,6,'2024-05-21 14:04:49','2024-05-21 14:04:49',NULL,0,0),(51,6,4,5,'2024-05-21 14:06:36','2024-05-21 14:08:03',5,0,0),(52,4,5,6,'2024-06-01 03:30:50','2024-06-01 03:31:47',6,0,0),(53,4,5,6,'2024-06-01 03:59:49','2024-06-01 04:00:31',6,0,0),(54,4,5,6,'2024-06-01 04:00:50','2024-06-01 04:00:50',NULL,0,0),(55,4,5,6,'2024-06-01 04:01:56','2024-06-01 04:01:56',NULL,0,0),(56,4,5,6,'2024-06-01 04:04:03','2024-06-01 04:04:03',NULL,0,0),(57,4,5,6,'2024-06-01 04:05:00','2024-06-01 04:05:00',NULL,0,0),(58,4,5,6,'2024-06-01 04:07:13','2024-06-01 04:08:29',6,0,0),(59,4,5,6,'2024-06-01 04:12:00','2024-06-01 04:12:00',NULL,0,0),(60,4,5,6,'2024-06-01 04:13:33','2024-06-01 04:13:33',NULL,0,0),(61,4,5,6,'2024-06-01 04:15:09','2024-06-01 04:15:09',NULL,0,0),(62,4,5,6,'2024-06-01 04:19:21','2024-06-01 04:19:30',NULL,0,0),(63,4,5,6,'2024-06-01 04:21:45','2024-06-01 04:21:49',NULL,0,0),(64,4,5,6,'2024-06-01 04:23:47','2024-06-01 04:23:51',NULL,0,0),(65,4,5,6,'2024-06-01 04:40:13','2024-06-01 04:40:13',NULL,0,0),(66,4,5,6,'2024-06-01 04:42:38','2024-06-01 04:42:38',NULL,0,0),(67,4,5,6,'2024-06-01 04:44:42','2024-06-01 04:44:42',NULL,0,0),(68,4,5,6,'2024-06-01 04:50:09','2024-06-01 04:50:09',NULL,0,0),(69,4,5,6,'2024-06-01 04:53:38','2024-06-01 04:53:38',NULL,0,0),(70,4,6,5,'2024-06-01 04:55:39','2024-06-01 04:55:48',NULL,0,0),(71,6,5,4,'2024-06-01 05:01:34','2024-06-01 05:01:34',NULL,0,0),(72,4,5,6,'2024-06-01 05:02:30','2024-06-01 05:02:30',NULL,0,0),(73,5,4,6,'2024-06-01 05:03:12','2024-06-01 05:03:35',6,0,0),(74,4,5,6,'2024-06-01 05:03:53','2024-06-01 05:03:53',NULL,0,0),(75,4,5,6,'2024-06-01 05:10:33','2024-06-01 05:10:33',NULL,0,0),(76,4,5,6,'2024-06-01 05:12:32','2024-06-01 05:12:51',NULL,0,0),(77,6,5,4,'2024-06-01 05:16:02','2024-06-01 05:16:02',NULL,0,0),(78,4,5,6,'2024-06-01 05:17:18','2024-06-01 05:17:18',NULL,0,0),(79,4,5,6,'2024-06-01 05:32:47','2024-06-01 05:32:47',NULL,0,0),(80,4,5,6,'2024-06-01 05:37:08','2024-06-01 05:37:08',NULL,0,0),(81,4,5,6,'2024-06-01 05:43:35','2024-06-01 05:43:35',NULL,0,0),(82,4,5,6,'2024-06-01 05:44:25','2024-06-01 05:44:25',NULL,0,0),(83,4,5,6,'2024-06-01 05:45:29','2024-06-01 05:45:29',NULL,0,0),(84,4,5,6,'2024-06-01 05:46:57','2024-06-01 05:46:57',NULL,0,0),(85,4,5,6,'2024-06-01 05:48:39','2024-06-01 05:48:39',NULL,0,0),(86,4,5,6,'2024-06-01 05:53:00','2024-06-01 05:53:00',NULL,0,0),(87,5,6,4,'2024-06-01 05:57:20','2024-06-01 05:57:20',NULL,0,0),(88,5,6,4,'2024-06-01 05:59:30','2024-06-01 05:59:30',NULL,0,0),(89,5,4,6,'2024-06-01 06:01:34','2024-06-01 06:01:34',NULL,0,0),(90,5,6,4,'2024-06-01 06:06:52','2024-06-01 06:06:52',NULL,0,0),(91,5,6,4,'2024-06-01 06:07:55','2024-06-01 06:07:55',NULL,0,0),(92,4,6,5,'2024-06-01 06:08:19','2024-06-01 06:08:44',4,0,0),(93,4,6,5,'2024-06-01 06:08:53','2024-06-01 06:10:10',4,0,0),(94,5,6,4,'2024-06-01 06:10:27','2024-06-01 06:10:45',NULL,0,0),(95,5,6,4,'2024-06-01 06:11:00','2024-06-01 06:11:00',NULL,0,0),(96,6,4,5,'2024-06-01 06:15:26','2024-06-01 06:15:26',NULL,0,0),(97,6,5,4,'2024-06-01 06:16:17','2024-06-01 06:16:17',NULL,0,0),(98,4,6,5,'2024-06-01 06:18:16','2024-06-01 06:18:16',NULL,0,0),(99,6,5,4,'2024-06-01 06:20:49','2024-06-01 06:20:49',NULL,0,0),(100,6,5,4,'2024-06-01 06:22:18','2024-06-01 06:25:44',4,0,0),(101,6,5,4,'2024-06-01 06:25:58','2024-06-01 06:25:58',NULL,0,0),(102,4,6,5,'2024-06-01 06:30:20','2024-06-01 06:30:20',NULL,0,0),(103,4,6,5,'2024-06-01 06:33:29','2024-06-01 06:34:07',6,0,0),(104,5,6,4,'2024-06-01 06:34:37','2024-06-01 06:35:17',5,0,0);
/*!40000 ALTER TABLE `game_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userId` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `userName` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户昵称',
  `userPassword` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '账号密码',
  `rank` bigint unsigned NOT NULL DEFAULT '0',
  `score` bigint unsigned NOT NULL DEFAULT '0',
  `gender` varchar(10) DEFAULT NULL,
  `phoneNum` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `imagePath` varchar(200) DEFAULT NULL,
  `banned` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`userId`),
  UNIQUE KEY `UserAccounts_unique` (`userName`),
  CONSTRAINT `user_check` CHECK ((`gender` in (_utf8mb4'male',_utf8mb4'female')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Xhyntao','31231277',0,0,NULL,NULL,'312@qq.com',NULL,0),(2,'Xhyntao1','12345678',0,0,NULL,NULL,NULL,NULL,0),(3,'Xhyntao2','12345678',0,0,NULL,NULL,NULL,NULL,0),(4,'xu','12345678',0,0,NULL,NULL,NULL,'/static/4.png',0),(5,'xu2','12345678',0,0,NULL,NULL,NULL,'/static/5.svg',0),(6,'xu3','12345678',0,0,NULL,NULL,NULL,NULL,0),(7,'xu5','12345678',0,0,NULL,NULL,NULL,'/static/7.svg',0),(8,'xu6','12345678',0,0,NULL,NULL,NULL,NULL,0),(9,'test','1234567',0,0,'male',NULL,'323231@11.com',NULL,0),(10,'徐海岩','3456789aa',0,0,'male','15531466666','23223123@a.com',NULL,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'trianglechess'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-01 16:58:02
-- Dump completed on 2024-06-01 20:45:53
