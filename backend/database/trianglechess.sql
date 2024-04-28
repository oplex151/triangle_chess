-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: triangle_chess
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
  `endTime` timestamp NOT NULL COMMENT '对局结束时间',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_record`
--

LOCK TABLES `game_record` WRITE;
/*!40000 ALTER TABLE `game_record` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'triangle_chess'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-26 22:59:46
