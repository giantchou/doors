-- MySQL dump 10.13  Distrib 5.7.22, for osx10.11 (x86_64)
--
-- Host: 47.92.116.232    Database: doors
-- ------------------------------------------------------
-- Server version	5.6.35-log

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
-- Table structure for table `cases`
--

DROP TABLE IF EXISTS `cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cases` (
  `cid` int(11) NOT NULL AUTO_INCREMENT COMMENT '案例id',
  `title` varchar(100) NOT NULL COMMENT '案例标题',
  `keyword` varchar(50) NOT NULL COMMENT '案例牵涉关键词,多个用逗号分隔',
  `abstract` varchar(150) NOT NULL COMMENT '摘要',
  `content` text NOT NULL COMMENT '案例内容',
  `addtime` int(11) NOT NULL COMMENT '案例采集时间',
  `from_web` varchar(255) NOT NULL COMMENT '案例采集来自哪里',
  `title_img` varchar(255) NOT NULL COMMENT '案例图片',
  `cate1` int(3) NOT NULL COMMENT '案例所属的1级分类',
  `cate2` int(3) NOT NULL COMMENT '案例所属的2级分类',
  PRIMARY KEY (`cid`),
  UNIQUE KEY `nid` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='工程案例表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cases`
--

LOCK TABLES `cases` WRITE;
/*!40000 ALTER TABLE `cases` DISABLE KEYS */;
/*!40000 ALTER TABLE `cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cate`
--

DROP TABLE IF EXISTS `cate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cate` (
  `cateid` int(3) NOT NULL AUTO_INCREMENT COMMENT '分类id',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `level` tinyint(4) NOT NULL COMMENT '分类级别',
  `parentid` int(3) NOT NULL DEFAULT '0' COMMENT '父分类id',
  PRIMARY KEY (`cateid`),
  UNIQUE KEY `cateid` (`cateid`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='分类表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cate`
--

LOCK TABLES `cate` WRITE;
/*!40000 ALTER TABLE `cate` DISABLE KEYS */;
INSERT INTO `cate` VALUES (1,'工业门系列',1,0),(2,'电动伸缩门',1,0),(3,'别墅庭院大门',1,0),(4,'旋转门',1,0),(5,'停车管理配套产品',1,0),(6,'围栏',1,0),(7,'路障',1,0),(8,'岗亭',1,0),(9,'自动感应门',1,0),(10,'悬浮门',1,0),(11,'电动刷卡门',1,0),(12,'侧小门',1,0),(13,'声障系列',1,0),(14,'预留2',1,0),(15,'预留3',1,0),(16,' 悬浮折叠门',2,1),(17,'无轨悬浮门',2,1),(18,' 伸缩平移门',2,1),(19,' 铝合金-电动伸缩门',2,2),(20,'不锈钢-电动伸缩门',2,2),(21,' 铜艺-别墅庭院大门',2,3),(22,'铝艺-别墅庭院大门',2,3),(23,'不锈钢-别墅庭院大门',2,3),(24,'两翼旋转门 ',2,4),(25,'三翼旋转门 ',2,4),(26,'四翼旋转门 ',2,4),(27,'水晶旋转门 ',2,4),(28,'环柱旋转门 ',2,4),(29,'电动道闸',2,5),(30,'人行通道闸',2,5),(31,'车牌识别系统',2,5),(32,'停车管理系统方案',2,5),(33,'铝艺围栏',2,6),(34,'铁艺围栏',2,6),(35,'不锈钢围栏',2,6),(36,'木艺围栏',2,6);
/*!40000 ALTER TABLE `cate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cate_product_hyperlink`
--

DROP TABLE IF EXISTS `cate_product_hyperlink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cate_product_hyperlink` (
  `id` int(10) NOT NULL,
  `keyword` varchar(20) NOT NULL COMMENT '关键词',
  `productlink` varchar(255) NOT NULL COMMENT '产品链接',
  `catelevel` tinyint(3) NOT NULL COMMENT '关键词所属分类级别'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cate_product_hyperlink`
--

LOCK TABLES `cate_product_hyperlink` WRITE;
/*!40000 ALTER TABLE `cate_product_hyperlink` DISABLE KEYS */;
/*!40000 ALTER TABLE `cate_product_hyperlink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news` (
  `nid` int(11) NOT NULL AUTO_INCREMENT COMMENT '新闻id',
  `title` varchar(100) NOT NULL COMMENT '新闻标题',
  `keyword` varchar(50) NOT NULL COMMENT '新闻牵涉关键词,多个用逗号分隔',
  `abstract` varchar(150) NOT NULL COMMENT '摘要',
  `content` text NOT NULL COMMENT '新闻内容',
  `addtime` int(11) NOT NULL COMMENT '采集时间',
  `from_web` varchar(255) NOT NULL COMMENT '采集来自哪里',
  `title_img` varchar(255) NOT NULL COMMENT '标题图片',
  `cate1` int(3) NOT NULL COMMENT '新闻资讯所属的1级分类',
  `cate2` int(3) NOT NULL COMMENT '新闻资讯所属的2级分类',
  PRIMARY KEY (`nid`),
  UNIQUE KEY `nid` (`nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='新闻资讯表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `pid` int(11) NOT NULL AUTO_INCREMENT COMMENT '产品id',
  `title` varchar(100) NOT NULL COMMENT '产品标题',
  `keyword` varchar(50) NOT NULL COMMENT '产品牵涉关键词,多个用逗号分隔',
  `abstract` varchar(150) NOT NULL COMMENT '摘要',
  `content` text NOT NULL COMMENT '产品介绍内容',
  `addtime` int(11) NOT NULL COMMENT '产品采集时间',
  `from_web` varchar(255) NOT NULL COMMENT '产品采集来自哪里',
  `title_img` varchar(255) NOT NULL COMMENT '产品图片',
  `material` varchar(100) NOT NULL COMMENT '材质',
  `cate1` int(3) NOT NULL COMMENT '产品所属1级分类',
  `cate2` int(3) NOT NULL COMMENT '产品所属2级分类',
  `hot` tinyint(2) DEFAULT '0' COMMENT '产品热度',
  PRIMARY KEY (`pid`),
  UNIQUE KEY `nid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='产品表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-12 13:10:57
