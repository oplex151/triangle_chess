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
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_move`
--

LOCK TABLES `game_move` WRITE;
/*!40000 ALTER TABLE `game_move` DISABLE KEYS */;
INSERT INTO `game_move` VALUES (1,1,1,'piece','7,2,0','1,0,1','2024-05-14 05:56:28'),(2,1,2,'piece','2,0,1','4,2,1','2024-05-14 05:56:40'),(3,1,3,'piece','7,2,2','1,0,0','2024-05-14 05:56:49'),(4,1,1,'piece','1,0,1','4,0,1','2024-05-14 05:56:58'),(5,1,3,'piece','2,3,2','2,4,2','2024-05-14 05:57:12'),(6,1,1,'piece','2,0,0','4,2,0','2024-05-14 05:57:17'),(7,1,3,'piece','1,0,0','4,0,0','2024-05-14 05:57:21'),(8,2,1,'piece','7,2,0','1,0,1','2024-05-14 06:06:12'),(9,2,2,'piece','2,0,1','4,2,1','2024-05-14 06:06:18'),(10,2,3,'piece','7,2,2','1,0,0','2024-05-14 06:06:24'),(11,2,1,'piece','1,0,1','4,0,1','2024-05-14 06:06:29'),(12,2,3,'piece','2,3,2','2,4,2','2024-05-14 06:06:47'),(13,2,1,'piece','2,0,0','4,2,0','2024-05-14 06:06:50'),(14,2,3,'piece','1,0,0','4,0,0','2024-05-14 06:06:54'),(15,3,1,'piece','7,2,0','1,0,1','2024-05-14 06:12:32'),(16,3,2,'piece','2,0,1','4,2,1','2024-05-14 06:12:35'),(17,3,3,'piece','7,2,2','1,0,0','2024-05-14 06:12:39'),(18,3,1,'piece','1,0,1','4,0,1','2024-05-14 06:12:44'),(19,3,3,'piece','2,3,2','2,4,2','2024-05-14 06:12:52'),(20,3,1,'piece','2,0,0','4,2,0','2024-05-14 06:12:55'),(21,3,3,'piece','1,0,0','4,0,0','2024-05-14 06:12:59'),(22,4,1,'piece','1,2,0','7,0,2','2024-05-14 12:58:56'),(23,4,3,'piece','1,2,1','7,0,0','2024-05-14 12:59:03'),(24,4,2,'piece','6,0,2','4,2,2','2024-05-14 12:59:08'),(25,4,1,'piece','7,0,2','4,0,2','2024-05-14 12:59:11'),(26,4,3,'piece','2,3,1','2,4,1','2024-05-14 12:59:21'),(27,4,1,'piece','6,0,0','4,2,0','2024-05-14 12:59:24'),(28,4,3,'piece','7,0,0','4,0,0','2024-05-14 12:59:26'),(29,5,1,'piece','1,2,0','7,0,2','2024-05-14 13:00:18'),(30,5,3,'piece','1,2,1','7,0,0','2024-05-14 13:00:27'),(31,5,2,'piece','6,0,2','4,2,2','2024-05-14 13:00:30'),(32,5,1,'piece','7,0,2','4,0,2','2024-05-14 13:00:32'),(33,5,3,'piece','2,3,1','2,4,1','2024-05-14 13:00:35'),(34,5,1,'piece','6,0,0','4,2,0','2024-05-14 13:00:40'),(35,5,3,'piece','7,0,0','4,0,0','2024-05-14 13:00:41'),(36,51,6,'piece','1,2,0','7,0,2','2024-05-21 14:06:58'),(37,51,4,'piece','0,3,1','0,4,1','2024-05-21 14:07:01'),(38,51,5,'piece','7,2,2','7,4,2','2024-05-21 14:07:04'),(39,51,6,'piece','0,3,0','0,4,0','2024-05-21 14:07:08'),(40,51,4,'piece','1,2,1','7,0,0','2024-05-21 14:07:13'),(41,51,5,'piece','2,3,2','2,4,2','2024-05-21 14:07:16'),(42,51,6,'piece','2,3,0','2,4,0','2024-05-21 14:07:32'),(43,51,4,'piece','2,3,1','2,4,1','2024-05-21 14:07:36'),(44,51,5,'piece','1,2,2','7,0,1','2024-05-21 14:07:37'),(45,51,6,'piece','6,0,0','4,2,0','2024-05-21 14:07:44'),(46,51,4,'piece','7,0,0','4,0,0','2024-05-21 14:07:45'),(47,51,5,'piece','6,0,2','4,2,2','2024-05-21 14:07:51'),(48,51,4,'piece','6,0,1','4,2,1','2024-05-21 14:08:01'),(49,51,5,'piece','7,0,1','4,0,1','2024-05-21 14:08:03');
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
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_record`
--

LOCK TABLES `game_record` WRITE;
/*!40000 ALTER TABLE `game_record` DISABLE KEYS */;
INSERT INTO `game_record` VALUES (1,1,2,3,'2024-05-14 05:53:45','2024-05-14 05:57:22',3,0,0),(2,1,2,3,'2024-05-14 06:05:11',NULL,NULL,0,0),(3,1,2,3,'2024-05-14 06:11:06',NULL,NULL,0,0),(4,1,3,2,'2024-05-14 12:58:45','2024-05-14 12:59:27',3,0,0),(5,1,3,2,'2024-05-14 13:00:13','2024-05-14 13:00:42',3,0,0),(6,4,5,6,'2024-05-15 15:55:34',NULL,NULL,0,0),(7,4,5,6,'2024-05-15 15:57:35',NULL,NULL,0,0),(8,6,5,4,'2024-05-15 16:01:54',NULL,NULL,0,0),(9,5,4,6,'2024-05-15 16:07:21',NULL,NULL,0,0),(10,5,4,6,'2024-05-15 16:09:10',NULL,NULL,0,0),(11,4,5,6,'2024-05-15 16:14:17','2024-05-15 16:14:42',4,0,0),(12,6,5,4,'2024-05-15 16:15:04',NULL,NULL,0,0),(13,6,5,4,'2024-05-15 16:16:56',NULL,NULL,0,0),(14,5,6,4,'2024-05-15 16:18:55',NULL,NULL,0,0),(15,4,5,6,'2024-05-15 16:24:31','2024-05-15 16:24:34',5,0,0),(16,6,5,4,'2024-05-15 16:25:05',NULL,NULL,0,0),(17,6,5,4,'2024-05-15 16:25:12',NULL,NULL,0,0),(18,4,5,6,'2024-05-15 16:25:44',NULL,NULL,0,0),(19,4,5,6,'2024-05-15 16:30:32','2024-05-15 16:30:34',5,0,0),(20,4,5,6,'2024-05-15 16:31:14',NULL,NULL,0,0),(21,5,4,6,'2024-05-15 16:34:11','2024-05-15 16:34:13',5,0,0),(22,6,5,4,'2024-05-15 16:34:20','2024-05-15 16:34:24',5,0,0),(23,4,5,6,'2024-05-15 16:35:27','2024-05-15 16:35:31',6,0,0),(24,4,5,6,'2024-05-15 16:44:05','2024-05-15 16:44:36',6,0,0),(25,5,4,6,'2024-05-15 16:44:53',NULL,NULL,0,0),(26,4,5,6,'2024-05-15 16:52:15','2024-05-15 16:52:18',6,0,0),(27,6,5,4,'2024-05-15 16:52:39','2024-05-15 16:52:42',5,0,0),(28,5,6,4,'2024-05-16 02:29:22',NULL,NULL,0,0),(29,5,4,6,'2024-05-16 02:36:09',NULL,NULL,0,0),(30,5,6,4,'2024-05-16 02:48:22',NULL,NULL,0,0),(31,4,5,6,'2024-05-16 02:52:47','2024-05-16 02:52:56',5,0,0),(32,5,4,6,'2024-05-16 02:53:05',NULL,NULL,0,0),(33,4,5,6,'2024-05-16 03:03:05','2024-05-16 03:03:09',5,0,0),(34,4,5,6,'2024-05-16 03:04:48','2024-05-16 03:04:50',5,0,0),(35,4,5,6,'2024-05-16 03:07:49','2024-05-16 03:07:52',4,0,0),(36,4,5,6,'2024-05-16 03:10:55','2024-05-16 03:10:57',5,0,0),(37,4,5,6,'2024-05-16 03:12:05','2024-05-16 03:12:07',4,0,0),(38,4,5,6,'2024-05-16 03:42:45','2024-05-16 03:42:47',6,0,0),(39,5,4,6,'2024-05-21 13:33:23','2024-05-21 13:33:23',NULL,0,0),(40,5,4,6,'2024-05-21 13:34:55','2024-05-21 13:34:55',NULL,0,0),(41,5,4,6,'2024-05-21 13:35:41','2024-05-21 13:35:41',NULL,0,0),(42,5,4,6,'2024-05-21 13:37:20','2024-05-21 13:37:20',NULL,0,0),(43,5,4,6,'2024-05-21 13:37:33','2024-05-21 13:37:33',NULL,0,0),(44,5,4,6,'2024-05-21 13:37:53','2024-05-21 13:37:53',NULL,0,0),(45,6,4,5,'2024-05-21 13:39:54','2024-05-21 13:39:54',NULL,0,0),(46,5,4,6,'2024-05-21 13:43:44','2024-05-21 13:43:44',NULL,0,0),(47,5,4,6,'2024-05-21 13:44:50','2024-05-21 13:44:50',NULL,0,0),(48,5,4,6,'2024-05-21 13:45:42','2024-05-21 13:45:42',NULL,0,0),(49,4,5,6,'2024-05-21 14:01:17','2024-05-21 14:01:17',NULL,0,0),(50,5,4,6,'2024-05-21 14:04:49','2024-05-21 14:04:49',NULL,0,0),(51,6,4,5,'2024-05-21 14:06:36','2024-05-21 14:08:03',5,0,0);
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
  PRIMARY KEY (`userId`),
  UNIQUE KEY `UserAccounts_unique` (`userName`),
  CONSTRAINT `user_check` CHECK ((`gender` in (_utf8mb4'male',_utf8mb4'female')))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Xhyntao','12345678',0,0,NULL,NULL,NULL),(2,'Xhyntao1','12345678',0,0,NULL,NULL,NULL),(3,'Xhyntao2','12345678',0,0,NULL,NULL,NULL),(4,'xu','12345678',0,0,NULL,NULL,NULL),(5,'xu2','12345678',0,0,NULL,NULL,NULL),(6,'xu3','12345678',0,0,NULL,NULL,NULL);
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

-- Dump completed on 2024-05-26  0:31:05
