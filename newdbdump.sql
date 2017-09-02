-- MySQL dump 10.13  Distrib 5.6.35, for osx10.9 (x86_64)
--
-- Host: localhost    Database: newdb
-- ------------------------------------------------------
-- Server version	5.6.35

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('c7f173f1484d');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `captain`
--

DROP TABLE IF EXISTS `captain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `captain` (
  `id` int(11) NOT NULL,
  `tournament_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tournament_id` (`tournament_id`),
  CONSTRAINT `captain_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`),
  CONSTRAINT `captain_ibfk_2` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captain`
--

LOCK TABLES `captain` WRITE;
/*!40000 ALTER TABLE `captain` DISABLE KEYS */;
INSERT INTO `captain` VALUES (33,12),(9,13),(19,13),(20,13),(21,13),(22,13),(23,13),(24,13),(25,13),(26,13),(27,13),(28,13),(29,13),(30,13),(31,13),(32,13),(34,13);
/*!40000 ALTER TABLE `captain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `judge`
--

DROP TABLE IF EXISTS `judge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `judge` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `judge_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `judge`
--

LOCK TABLES `judge` WRITE;
/*!40000 ALTER TABLE `judge` DISABLE KEYS */;
INSERT INTO `judge` VALUES (8);
/*!40000 ALTER TABLE `judge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizer`
--

DROP TABLE IF EXISTS `organizer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `organizer` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `organizer_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizer`
--

LOCK TABLES `organizer` WRITE;
/*!40000 ALTER TABLE `organizer` DISABLE KEYS */;
INSERT INTO `organizer` VALUES (7),(10),(12),(14),(15),(16),(17),(18);
/*!40000 ALTER TABLE `organizer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `total_score` int(11) DEFAULT NULL,
  `captain_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `captain_id` (`captain_id`),
  CONSTRAINT `team_ibfk_1` FOREIGN KEY (`captain_id`) REFERENCES `captain` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES (1,'Winners',0,9);
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tournament`
--

DROP TABLE IF EXISTS `tournament`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tournament` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `organizer_id` int(11) DEFAULT NULL,
  `judge_id` int(11) DEFAULT NULL,
  `name` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `organizer_id` (`organizer_id`),
  KEY `judge_id` (`judge_id`),
  CONSTRAINT `tournament_ibfk_1` FOREIGN KEY (`organizer_id`) REFERENCES `organizer` (`id`),
  CONSTRAINT `tournament_ibfk_2` FOREIGN KEY (`judge_id`) REFERENCES `judge` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tournament`
--

LOCK TABLES `tournament` WRITE;
/*!40000 ALTER TABLE `tournament` DISABLE KEYS */;
INSERT INTO `tournament` VALUES (1,7,8,NULL),(2,18,8,'nmsdf'),(3,18,8,'sdfsdfs'),(4,18,8,'sdfsdfs'),(5,18,8,'asdfsdfsdf'),(6,18,8,'asdfsdfsdf'),(7,18,8,'asdfsdfsdf'),(8,18,8,'asdfsdfsdf'),(9,18,8,'New tournament'),(10,18,8,'Great tour '),(11,18,8,'Great sdkfjsdf'),(12,18,8,'KISKA'),(13,18,8,'Real');
/*!40000 ALTER TABLE `tournament` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(15) DEFAULT NULL,
  `first_name` varchar(40) DEFAULT NULL,
  `last_name` varchar(40) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `password` varchar(80) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'Fujman','Narek','Martikian','narek@voliacable.com','pbkdf2:sha256:50000$7P9elirh$8a7a49078cbf22cdafd1fd0fd160f3f9a6016081c9dc1a49651',NULL),(4,'Neww','dslkdfjs','ksjfksjdf','sdkf@kljsfd.com','sha256$Evl7sYfE$4c09b9caf499d216b9ceb5046a2d61b9631b824d6300b3bba19b049a240cf618',NULL),(5,'Babe','sldfsdfj','ksdjflskdjf','babe@babe.com','sha256$E6oZrNRM$e07d01d98558c8747d0c0864ec4899ce13a8fd288283b2842bfe6ff2e46badb0',NULL),(6,'Klips','Namename','Namename','email@email.com','sha256$s77MGDFF$5538c20a93fc206c1dae2af44322573ae220dd272bfd5cfbeb0ff139406579bd','judge'),(7,'Orgiz','Orgizz','Orgizz','sjdhf@mail.com','asdfsadfsdf','organizer'),(8,'Judgie','Judge','Judgerson','judge@mail.com','asdfssdfsdf','judge'),(9,'captainn','Cappp','Captainson','captain@mail.com','asdfssdfsdf','captain'),(10,'NewOrg','Clark','Peterson','clark@gmail.com','sha256$MVrdsRfA$c5af4f32b5f8e2a39ca4774053d14f7bc6155cbea7e3d847f6f3ba2b224f3d45','organizer'),(12,'NewwORH','sdjfsd','kfsdfjsd','sjdf@kdf.com','sha256$OvTwgcse$3b45791b9eec78c539bbd1926bd89e866f0ec5cf369866d70fa02e23b381ad96','organizer'),(14,'Fujmansdf','fjsdfhskdjfh','sfjdhfkjshdf','jhsdf@mail.com','sha256$0w9L1Ut0$5be4ace463145202d9437e5f51e5329148fb5a23cd24a092f2443573a6020406','organizer'),(15,'Fujmsdf','jkksdjfsakdfj','lkjsdlfjsdf','kjk@lksdjf.com','sha256$pn4VD0P3$8120bf165b26c1bd7db14839ecb6a9ab205c520236033a097fac8f41d90c5b83','organizer'),(16,'asdfsjdfaj','kjhsdkfhskdfhj','jhdskfhsdf','kjhkjh@djksfh.com','sha256$Wc1UZsGS$96ea4fcf1be4b8b8ac4b3eaba4b289de0c30bf07527b3baf6e7c9200e1932954','organizer'),(17,'asdfhsdfj','jhsdkfhjsjkdf','kjhskdfhskdf','jshdfk@dlsfj.com','sha256$6QCsT1WV$3bb7e075876d43a9fce6ba1475f5da1986b2d3049304dc75e44f3447a7dace61','organizer'),(18,'LOLK','LOLK','LOLK','lolk@lolk.com','sha256$1CRISJWo$cb3ddf386bde84b7f73f140ac010f847d053bae6c0d51ded00ebfa082944c221','organizer'),(19,'capt1','John','Lennon','capt1@mail.com','1q2w3e','captain'),(20,'capt2','Jim','Morrison','capt2@mail.com','1q2w3e','captain'),(21,'capt3','Jimi','Hendrix','capt3@mail.com','1q2w3e','captain'),(22,'capt4','Paul','Mccartney','capt4@mail.com','1q2w3e','captain'),(23,'capt5','Ringo','Starr','capt5@mail.com','1q2w3e','captain'),(24,'capt6','Kevin','Parker','capt6@mail.com','1q2w3e','captain'),(25,'capt7','Miles','Devis','capt7@mail.com','1q2w3e','captain'),(26,'capt8','Eric','Clapton','capt8@mail.com','1q2w3e','captain'),(27,'capt9','George','Harrison','capt9@mail.com','1q2w3e','captain'),(28,'capt10','Donald','Duck','capt10@mail.com','1q2w3e','captain'),(29,'capt11','Joey','Tribbiani','capt11@mail.com','1q2w3e','captain'),(30,'capt12','Mike','Tyson','capt12@mail.com','1q2w3e','captain'),(31,'capt13','Floyd','Mayweather','capt13@mail.com','1q2w3e','captain'),(32,'capt14','Bill','Clinton','capt14@mail.com','1q2w3e','captain'),(33,'capt15','Ross','Geller','capt15@mail.com','1q2w3e','captain'),(34,'capt16','Ray','Charles','capt16@mail.com','1q2w3e','captain');
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

-- Dump completed on 2017-09-02  6:36:10
