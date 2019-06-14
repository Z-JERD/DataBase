-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: 10.110.1.90    Database: arch2018
-- ------------------------------------------------------
-- Server version	5.7.22-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acct_user_group`
--

DROP TABLE IF EXISTS `acct_user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acct_user_group` (
  `gid` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户组id',
  `group_name` varchar(50) NOT NULL DEFAULT '' COMMENT '用户组名称',
  `group_info` varchar(255) NOT NULL DEFAULT '' COMMENT '用户组信息',
  `ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`gid`),
  UNIQUE KEY `grouip_name` (`group_name`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acct_user_group`
--

LOCK TABLES `acct_user_group` WRITE;
/*!40000 ALTER TABLE `acct_user_group` DISABLE KEYS */;
INSERT INTO `acct_user_group` VALUES (1,'超级管理员组','所有权限','2015-06-18 05:49:47'),(2,'发行组','发行权限','2015-07-08 04:27:48'),(3,'华夏员工组','领导权限','2015-07-08 08:55:45'),(4,'开发组','所有权限','2015-07-10 03:20:18'),(5,'影院组','影院权限','2015-10-16 01:52:08'),(6,'院线组','院线用户','2015-10-24 08:01:31'),(7,'影院组员工','影院员工权限','2015-10-16 01:52:08'),(8,'院线组员工','院线员工权限','2015-10-24 08:01:31'),(9,'设备厂商组','设备厂商组','2015-10-24 08:04:53'),(10,'片方组','片方组','2015-10-24 08:05:49'),(11,'监察机构','监察机构','2015-10-24 08:06:25'),(12,'管理办公室组','所有权限','2015-11-26 02:15:24'),(13,'中国巨幕组','中国巨幕','2016-01-27 01:23:35'),(14,'普通用户组','普通用户权限','2015-10-24 08:01:31'),(15,'统计报表组','查看统计报表','2016-06-06 03:32:44'),(16,'发行经理','发行项目审核管理','2017-06-21 03:43:07'),(17,'院线责任人','院线责任人','2017-06-21 03:45:27'),(18,'艺术院线影院组','艺术院线影院组','2016-11-10 02:40:46'),(19,'艺术院线管理组','艺术院线管理组','2016-11-10 02:40:46'),(20,'数字制作组','数字制作组','2016-11-10 02:40:46'),(21,'中数发展用户','中数发展用户','2017-07-13 09:27:40'),(22,'艺术院线报表组','艺术院线报表组','2016-12-20 01:33:36'),(23,'证书管理组','证书管理组','2016-12-27 09:11:13'),(24,'管理公司组','管理公司组','2016-12-28 02:45:45'),(25,'结算报表组','结算报表组','2017-01-05 06:28:50'),(26,'结算中心组','结算中心组','2017-03-20 09:08:25'),(27,'硬盘管理组','硬盘管理组','2017-03-23 09:56:26'),(28,'数字制作费审核组','数字制作费审核组','2017-04-13 05:16:12'),(29,'数字制作费确认组','数字制作费确认组','2017-04-13 05:16:12'),(30,'公司主管','公司领导组','2017-06-21 03:42:59'),(31,'结算中心审核人','结算中心审核人组','2017-03-20 09:08:25'),(32,'院线管理','院线管理','2017-06-23 09:11:02'),(33,'投资管理','投资管理','2017-06-29 02:36:19'),(34,'结算中心院线对接人','结算中心院线对接人','2017-07-05 07:16:48'),(35,'二级市场管理','二级市场管理','2017-07-13 01:47:41'),(36,'协会总局用户','协会总局用户','2017-07-13 09:27:20'),(37,'设备厂商组只读组','设备厂商组只读权限','2017-08-25 05:39:20'),(38,'华夏票房统计','华夏票房统计','2017-08-29 01:37:41'),(39,'十一档票房汇总','十一档票房汇总','2017-09-27 10:29:18'),(40,'硬盘发运组','硬盘发运组','2017-10-19 08:14:18'),(41,'财务部主管','财务部主管','2017-10-20 09:37:35'),(42,'财务部责任人','财务部责任人','2017-10-20 09:38:20'),(43,'数字制作母盘管理','数字制作母盘管理','2017-10-24 03:51:55'),(44,'密钥制作组','密钥制作组','2017-11-09 09:20:55'),(45,'硬盘统计管理组','硬盘统计管理组','2017-11-16 05:58:36'),(46,'设备厂商证书上传组','设备厂商证书上传组','2018-04-10 08:31:36'),(47,'设备信息管理组','设备信息管理组','2018-04-10 08:31:34'),(48,'DMS硬盘查询','DMS硬盘查询','2018-04-12 09:52:04'),(49,'运单统计','运单统计','2018-05-23 06:48:51');
/*!40000 ALTER TABLE `acct_user_group` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-13 15:53:14
