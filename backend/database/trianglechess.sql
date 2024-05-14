-- MySQL dump 10.13  Distrib 8.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: trianglechess
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `trianglechess`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `trianglechess` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `trianglechess`;

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
  `content` varchar(100) NOT NULL COMMENT '评论信息',
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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_move`
--

LOCK TABLES `game_move` WRITE;
/*!40000 ALTER TABLE `game_move` DISABLE KEYS */;
INSERT INTO `game_move` VALUES (1,1,1,'piece','7,2,0','1,0,1','2024-05-14 05:56:28'),(2,1,2,'piece','2,0,1','4,2,1','2024-05-14 05:56:40'),(3,1,3,'piece','7,2,2','1,0,0','2024-05-14 05:56:49'),(4,1,1,'piece','1,0,1','4,0,1','2024-05-14 05:56:58'),(5,1,3,'piece','2,3,2','2,4,2','2024-05-14 05:57:12'),(6,1,1,'piece','2,0,0','4,2,0','2024-05-14 05:57:17'),(7,1,3,'piece','1,0,0','4,0,0','2024-05-14 05:57:21'),(8,2,1,'piece','7,2,0','1,0,1','2024-05-14 06:06:12'),(9,2,2,'piece','2,0,1','4,2,1','2024-05-14 06:06:18'),(10,2,3,'piece','7,2,2','1,0,0','2024-05-14 06:06:24'),(11,2,1,'piece','1,0,1','4,0,1','2024-05-14 06:06:29'),(12,2,3,'piece','2,3,2','2,4,2','2024-05-14 06:06:47'),(13,2,1,'piece','2,0,0','4,2,0','2024-05-14 06:06:50'),(14,2,3,'piece','1,0,0','4,0,0','2024-05-14 06:06:54'),(15,3,1,'piece','7,2,0','1,0,1','2024-05-14 06:12:32'),(16,3,2,'piece','2,0,1','4,2,1','2024-05-14 06:12:35'),(17,3,3,'piece','7,2,2','1,0,0','2024-05-14 06:12:39'),(18,3,1,'piece','1,0,1','4,0,1','2024-05-14 06:12:44'),(19,3,3,'piece','2,3,2','2,4,2','2024-05-14 06:12:52'),(20,3,1,'piece','2,0,0','4,2,0','2024-05-14 06:12:55'),(21,3,3,'piece','1,0,0','4,0,0','2024-05-14 06:12:59'),(22,4,1,'piece','1,2,0','7,0,2','2024-05-14 12:58:56'),(23,4,3,'piece','1,2,1','7,0,0','2024-05-14 12:59:03'),(24,4,2,'piece','6,0,2','4,2,2','2024-05-14 12:59:08'),(25,4,1,'piece','7,0,2','4,0,2','2024-05-14 12:59:11'),(26,4,3,'piece','2,3,1','2,4,1','2024-05-14 12:59:21'),(27,4,1,'piece','6,0,0','4,2,0','2024-05-14 12:59:24'),(28,4,3,'piece','7,0,0','4,0,0','2024-05-14 12:59:26'),(29,5,1,'piece','1,2,0','7,0,2','2024-05-14 13:00:18'),(30,5,3,'piece','1,2,1','7,0,0','2024-05-14 13:00:27'),(31,5,2,'piece','6,0,2','4,2,2','2024-05-14 13:00:30'),(32,5,1,'piece','7,0,2','4,0,2','2024-05-14 13:00:32'),(33,5,3,'piece','2,3,1','2,4,1','2024-05-14 13:00:35'),(34,5,1,'piece','6,0,0','4,2,0','2024-05-14 13:00:40'),(35,5,3,'piece','7,0,0','4,0,0','2024-05-14 13:00:41');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_record`
--

LOCK TABLES `game_record` WRITE;
/*!40000 ALTER TABLE `game_record` DISABLE KEYS */;
INSERT INTO `game_record` VALUES (1,1,2,3,'2024-05-14 05:53:45','2024-05-14 05:57:22',3,0,0),(2,1,2,3,'2024-05-14 06:05:11',NULL,NULL,0,0),(3,1,2,3,'2024-05-14 06:11:06',NULL,NULL,0,0),(4,1,3,2,'2024-05-14 12:58:45','2024-05-14 12:59:27',3,0,0),(5,1,3,2,'2024-05-14 13:00:13','2024-05-14 13:00:42',3,0,0);
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
  PRIMARY KEY (`userId`),
  UNIQUE KEY `UserAccounts_unique` (`userName`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Xhyntao','12345678'),(2,'Xhyntao1','12345678'),(3,'Xhyntao2','12345678');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-14 23:37:33
