-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: junction.proxy.rlwy.net    Database: railway
-- ------------------------------------------------------
-- Server version	9.0.1

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
-- Table structure for table `article_article`
--

DROP TABLE IF EXISTS `article_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `article_article` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `label` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `logo` varchar(255) NOT NULL,
  `category_id` bigint NOT NULL,
  `member_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `article_article_category_id_36b3c456_fk_categorie_categorie_id` (`category_id`),
  KEY `article_article_member_id_fdad5f0c_fk_member_utilisateur_ptr_id` (`member_id`),
  CONSTRAINT `article_article_category_id_36b3c456_fk_categorie_categorie_id` FOREIGN KEY (`category_id`) REFERENCES `categorie_categorie` (`id`),
  CONSTRAINT `article_article_member_id_fdad5f0c_fk_member_utilisateur_ptr_id` FOREIGN KEY (`member_id`) REFERENCES `member` (`utilisateur_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article_article`
--

LOCK TABLES `article_article` WRITE;
/*!40000 ALTER TABLE `article_article` DISABLE KEYS */;
INSERT INTO `article_article` VALUES (11,'Basckette pour homme',20000.00,1,'image/upload/v1724073314/pdma1pvbljjnw4llc1pe.jpg',2,3),(12,'Godasse',25000.00,1,'image/upload/v1724073407/wdlgqf8sn42dmmlnsjzl.jpg',2,3),(13,'Chaussure de sport',25000.00,1,'image/upload/v1724073445/a8bupnqs0nvjmn8yobnb.jpg',2,3),(14,'Chaussure en cuir pour homme',50000.00,1,'image/upload/v1724073491/ch6qgteb7mzahc5l6aao.jpg',2,3),(15,'Mocassin',15000.00,1,'image/upload/v1724073540/rszaktabzfluoznw5qol.jpg',2,3),(16,'Mocassin de sortie',18000.00,1,'image/upload/v1724073578/w2qinl6ewkfk0az54c8a.jpg',2,3),(17,'Bermuda',3500.00,1,'image/upload/v1724073646/gngzg4kh4prg3k4f0iqo.jpg',5,3),(18,'Bermuda coton pur',5000.00,1,'image/upload/v1724073676/fbtuilw5ujajrysd3uwc.jpg',5,3),(19,'Chaussette',1000.00,1,'image/upload/v1724073734/kl0dlstftgyuvh2masyr.jpg',5,3),(20,'Cullotte',3000.00,1,'image/upload/v1724073769/unbupo2ztfvaud4brxis.jpg',5,3),(21,'Boubou Bami',30000.00,1,'image/upload/v1724073912/qni0mw4nwshit9xihqoy.jpg',1,3),(22,'Costume trois pieces',70000.00,1,'image/upload/v1724073957/rtypbu1iuumv651mazc7.jpg',1,3),(23,'Costume',50000.00,1,'image/upload/v1724074000/sgaylnl0e9aucbahrbua.jpg',1,3),(24,'Ensemble coton(Cullote)',10000.00,1,'image/upload/v1724074036/ikldpuq6t1vclssn1vcv.jpg',1,3),(25,'Joggin',20000.00,1,'image/upload/v1724074084/ytv0k3czxqvqtjxqcet9.jpg',1,3),(26,'Joggin ensemble coton',35000.00,1,'image/upload/v1724074115/bg2xle4xz2ikqxuaivc0.jpg',1,3),(27,'Lacosta',5000.00,1,'image/upload/v1724074148/m3evmvc2quysgchrvvh9.jpg',1,3),(28,'Lacosta coton',6000.00,1,'image/upload/v1724074191/hfmtuvh5h8clhb0qnftn.jpg',1,3),(29,'Maillot de basckette',7500.00,1,'image/upload/v1724074245/dq4xyylloqaawmslworz.jpg',1,3),(30,'Pantalon djinn',5000.00,1,'image/upload/v1724074280/r0niubaior8zgszf5eoq.jpg',1,3),(31,'Pull',3000.00,1,'image/upload/v1724074310/onre8cfbzz1v9fjfasww.jpg',1,3),(32,'Veste',35000.00,1,'image/upload/v1724074356/xo4tmgiroqrtm7oe5vpf.jpg',1,3),(33,'Veste en cuir',20000.00,1,'image/upload/v1724074385/ncymtd0qjrcm03q8ktyh.jpg',1,3),(34,'Veste style',25000.00,1,'image/upload/v1724074413/evdmibmh446zejz637cz.jpg',1,3),(35,'Chaussure de sport pour femme',10000.00,1,'image/upload/v1724074480/z6kbrthywwusce2bdxpe.jpg',3,3),(36,'Tallon en cuir',15000.00,1,'image/upload/v1724074537/bl5tjygvr12rjzo4cfq6.jpg',3,3),(37,'Boubou femme',15000.00,1,'image/upload/v1724074585/zn7ny3ajptozlqnbxg5k.jpg',4,3),(38,'Ensembe robe de style',17000.00,1,'image/upload/v1724074628/mcqjonhsrdwmv9buhubg.jpg',4,3),(39,'Ensemble patalon decontracte',17000.00,1,'image/upload/v1724074651/q82r0k8qdpfdrth3vuz0.jpg',4,3),(40,'Ensemble responsable',25000.00,1,'image/upload/v1724074690/xcshmkrk15oo01bgzcho.jpg',4,3),(41,'Extra style',25000.00,1,'image/upload/v1724074713/k9yuwjysalyt80fja1tt.jpg',4,3),(42,'Haut pour femme',5000.00,1,'image/upload/v1724074751/mkw3wfegx7lklocvn3r5.jpg',4,3),(43,'Hidjab',15000.00,1,'image/upload/v1724075327/rf7kabjnff90etk8e1pc.jpg',4,3),(44,'Joggin pour femme',15000.00,1,'image/upload/v1724075359/z6yefvdb8cbokfua6mqk.jpg',4,3),(45,'Robe de plage',10000.00,1,'image/upload/v1724075397/bfoko6wx0jgnfeemoj5m.jpg',4,3),(46,'Robe de soiree',20000.00,1,'image/upload/v1724075424/jknjzplzlc3ot3cxrjho.jpg',4,3),(47,'Robe de soiree rafine',50000.00,1,'image/upload/v1724075452/knk155lrairhdy9hdblp.jpg',4,3),(48,'Robe de soiree sexy',17000.00,1,'image/upload/v1724075489/yditodnd9qgqeurklaoo.jpg',4,3),(49,'Robe pour femme enceinte',14500.00,1,'image/upload/v1724075536/cdnb7yx6fnxasj0fthql.jpg',4,3),(50,'Vetement de sport',10000.00,1,'image/upload/v1724075580/cjdclhzicyditio9uxyq.jpg',4,3),(51,'Sous vetement pour femme ensemble',5000.00,1,'image/upload/v1724075656/laszn2zh3nujaaauv3gh.jpg',6,3),(52,'Google Pixel 5',180000.00,1,'image/upload/v1724075819/xnjfwjpimiztsemkvcwg.jpg',7,3),(53,'Iphone 15 Pro',1200000.00,1,'image/upload/v1724075852/zkfznztaue7p05fk0tge.jpg',7,3),(54,'Iphone 15 Pro max',1500000.00,1,'image/upload/v1724075886/gxlcod7tozbnbtgbnp95.jpg',7,3),(55,'Motorolla',30000.00,1,'image/upload/v1724075919/qm8fs9mxr5ra8xtpqqrv.jpg',7,3),(56,'HP detachable',350000.00,1,'image/upload/v1724075973/y972cffugh8hjfobfcr3.jpg',8,3),(57,'HP Elite Book',850000.00,1,'image/upload/v1724076006/bksc5ghjjcxngtqggmw7.jpg',8,3),(58,'Lenovo Destok core i7',300000.00,1,'image/upload/v1724076037/fv7ux0r4vfl7uek1rguw.jpg',8,3),(63,'Mac Book Gamer',1200000.00,1,'image/upload/v1724081524/g0jauyuevrqfwivjgcct.jpg',8,3);
/*!40000 ALTER TABLE `article_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add organisation',6,'add_organisation'),(22,'Can change organisation',6,'change_organisation'),(23,'Can delete organisation',6,'delete_organisation'),(24,'Can view organisation',6,'view_organisation'),(25,'Can add cart',7,'add_cart'),(26,'Can change cart',7,'change_cart'),(27,'Can delete cart',7,'delete_cart'),(28,'Can view cart',7,'view_cart'),(29,'Can add cart item',8,'add_cartitem'),(30,'Can change cart item',8,'change_cartitem'),(31,'Can delete cart item',8,'delete_cartitem'),(32,'Can view cart item',8,'view_cartitem'),(33,'Can add role',9,'add_role'),(34,'Can change role',9,'change_role'),(35,'Can delete role',9,'delete_role'),(36,'Can view role',9,'view_role'),(37,'Can add privilegies',10,'add_privilegies'),(38,'Can change privilegies',10,'change_privilegies'),(39,'Can delete privilegies',10,'delete_privilegies'),(40,'Can view privilegies',10,'view_privilegies'),(41,'Can add article',11,'add_article'),(42,'Can change article',11,'change_article'),(43,'Can delete article',11,'delete_article'),(44,'Can view article',11,'view_article'),(45,'Can add categorie',12,'add_categorie'),(46,'Can change categorie',12,'change_categorie'),(47,'Can delete categorie',12,'delete_categorie'),(48,'Can view categorie',12,'view_categorie'),(49,'Can add utilisateur',13,'add_utilisateur'),(50,'Can change utilisateur',13,'change_utilisateur'),(51,'Can delete utilisateur',13,'delete_utilisateur'),(52,'Can view utilisateur',13,'view_utilisateur'),(53,'Can add client',14,'add_client'),(54,'Can change client',14,'change_client'),(55,'Can delete client',14,'delete_client'),(56,'Can view client',14,'view_client'),(57,'Can add member',15,'add_member'),(58,'Can change member',15,'change_member'),(59,'Can delete member',15,'delete_member'),(60,'Can view member',15,'view_member'),(61,'Can add password reset code',16,'add_passwordresetcode'),(62,'Can change password reset code',16,'change_passwordresetcode'),(63,'Can delete password reset code',16,'delete_passwordresetcode'),(64,'Can view password reset code',16,'view_passwordresetcode');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_cart`
--

DROP TABLE IF EXISTS `cart_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_cart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cart_cart_client_id_9e7560bd` (`client_id`),
  CONSTRAINT `cart_cart_client_id_9e7560bd_fk_client_utilisateur_ptr_id` FOREIGN KEY (`client_id`) REFERENCES `client` (`utilisateur_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_cart`
--

LOCK TABLES `cart_cart` WRITE;
/*!40000 ALTER TABLE `cart_cart` DISABLE KEYS */;
INSERT INTO `cart_cart` VALUES (1,11,'2024-08-23 01:16:25.949834'),(2,7,'2024-08-25 11:58:30.977074'),(3,12,'2024-08-27 09:26:25.901682');
/*!40000 ALTER TABLE `cart_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_cartitem`
--

DROP TABLE IF EXISTS `cart_cartitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_cartitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `article_id` bigint NOT NULL,
  `cart_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cart_cartitem_article_id_acd9063b_fk_article_article_id` (`article_id`),
  KEY `cart_cartitem_cart_id_370ad265_fk_cart_cart_id` (`cart_id`),
  CONSTRAINT `cart_cartitem_article_id_acd9063b_fk_article_article_id` FOREIGN KEY (`article_id`) REFERENCES `article_article` (`id`),
  CONSTRAINT `cart_cartitem_cart_id_370ad265_fk_cart_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `cart_cart` (`id`),
  CONSTRAINT `cart_cartitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_cartitem`
--

LOCK TABLES `cart_cartitem` WRITE;
/*!40000 ALTER TABLE `cart_cartitem` DISABLE KEYS */;
INSERT INTO `cart_cartitem` VALUES (1,2,11,1),(2,3,12,1),(3,1,13,1),(4,2,11,2),(5,2,11,3);
/*!40000 ALTER TABLE `cart_cartitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorie_categorie`
--

DROP TABLE IF EXISTS `categorie_categorie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorie_categorie` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `label` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorie_categorie`
--

LOCK TABLES `categorie_categorie` WRITE;
/*!40000 ALTER TABLE `categorie_categorie` DISABLE KEYS */;
INSERT INTO `categorie_categorie` VALUES (1,'Vetements pour homme',1),(2,'Chaussures pour homme',1),(3,'Chaussures pour femme',1),(4,'Vetement pour femme',1),(5,'Sous-vetements pour homme',1),(6,'Sous-vetements pour femme',1),(7,'Telephones',1),(8,'Ordinateurs',1);
/*!40000 ALTER TABLE `categorie_categorie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `utilisateur_ptr_id` bigint NOT NULL,
  PRIMARY KEY (`utilisateur_ptr_id`),
  CONSTRAINT `client_utilisateur_ptr_id_2f09ad0a_fk_utilisateur_utilisateur_id` FOREIGN KEY (`utilisateur_ptr_id`) REFERENCES `utilisateur_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (4),(5),(6),(7),(8),(11),(12);
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_utilisateur_utilisateur_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_utilisateur_utilisateur_id` FOREIGN KEY (`user_id`) REFERENCES `utilisateur_utilisateur` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(11,'article','article'),(3,'auth','group'),(2,'auth','permission'),(7,'cart','cart'),(8,'cart','cartitem'),(12,'categorie','categorie'),(4,'contenttypes','contenttype'),(6,'organisation','organisation'),(16,'passwordResetCode','passwordresetcode'),(10,'privilegies','privilegies'),(9,'rule','role'),(5,'sessions','session'),(14,'utilisateur','client'),(15,'utilisateur','member'),(13,'utilisateur','utilisateur');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'privilegies','0001_initial','2024-08-17 14:07:42.218814'),(2,'rule','0001_initial','2024-08-17 14:07:44.755637'),(3,'organisation','0001_initial','2024-08-17 14:07:45.368779'),(4,'utilisateur','0001_initial','2024-08-17 14:07:49.362329'),(5,'contenttypes','0001_initial','2024-08-17 14:07:50.185026'),(6,'admin','0001_initial','2024-08-17 14:07:52.948397'),(7,'admin','0002_logentry_remove_auto_add','2024-08-17 14:07:53.773402'),(8,'admin','0003_logentry_add_action_flag_choices','2024-08-17 14:07:54.090977'),(9,'categorie','0001_initial','2024-08-17 14:07:56.531158'),(10,'article','0001_initial','2024-08-17 14:07:58.784187'),(11,'article','0002_remove_article_logo_name_alter_article_logo','2024-08-17 14:08:03.072024'),(12,'article','0003_alter_article_logo','2024-08-17 14:08:03.399699'),(13,'contenttypes','0002_remove_content_type_name','2024-08-17 14:08:06.363192'),(14,'auth','0001_initial','2024-08-17 14:08:11.790112'),(15,'auth','0002_alter_permission_name_max_length','2024-08-17 14:08:12.506959'),(16,'auth','0003_alter_user_email_max_length','2024-08-17 14:08:12.763143'),(17,'auth','0004_alter_user_username_opts','2024-08-17 14:08:13.021525'),(18,'auth','0005_alter_user_last_login_null','2024-08-17 14:08:13.294397'),(19,'auth','0006_require_contenttypes_0002','2024-08-17 14:08:13.557415'),(20,'auth','0007_alter_validators_add_error_messages','2024-08-17 14:08:13.826739'),(21,'auth','0008_alter_user_username_max_length','2024-08-17 14:08:14.080185'),(22,'auth','0009_alter_user_last_name_max_length','2024-08-17 14:08:16.097407'),(23,'auth','0010_alter_group_name_max_length','2024-08-17 14:08:16.683208'),(24,'auth','0011_update_proxy_permissions','2024-08-17 14:08:17.668808'),(25,'auth','0012_alter_user_first_name_max_length','2024-08-17 14:08:17.936100'),(26,'utilisateur','0002_utilisateur_status','2024-08-17 14:08:19.777997'),(27,'cart','0001_initial','2024-08-17 14:08:24.386285'),(28,'cart','0002_alter_cart_client','2024-08-17 14:08:32.386094'),(29,'organisation','0002_remove_organisation_logo_name_and_more','2024-08-17 14:08:33.809634'),(30,'sessions','0001_initial','2024-08-17 14:08:35.548180'),(31,'utilisateur','0003_remove_utilisateur_logo_name_alter_utilisateur_logo','2024-08-17 14:08:38.313598'),(32,'rule','0002_remove_role_privileges_alter_role_role','2024-08-18 15:37:13.377988'),(33,'article','0004_article_urlpath','2024-08-19 15:31:26.076056'),(34,'article','0005_remove_article_urlpath','2024-08-19 15:33:18.236981'),(35,'passwordResetCode','0001_initial','2024-08-20 03:32:47.109741'),(36,'cart','0003_cart_created_at','2024-08-22 19:53:23.901395'),(37,'cart','0004_alter_cartitem_quantity','2024-08-23 01:20:51.898495');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `utilisateur_ptr_id` bigint NOT NULL,
  `organisation_id` bigint DEFAULT NULL,
  PRIMARY KEY (`utilisateur_ptr_id`),
  KEY `member_organisation_id_5c8ab5fc_fk_organisation_organisation_id` (`organisation_id`),
  CONSTRAINT `member_organisation_id_5c8ab5fc_fk_organisation_organisation_id` FOREIGN KEY (`organisation_id`) REFERENCES `organisation_organisation` (`id`),
  CONSTRAINT `member_utilisateur_ptr_id_825fba68_fk_utilisateur_utilisateur_id` FOREIGN KEY (`utilisateur_ptr_id`) REFERENCES `utilisateur_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (2,1),(9,1),(10,1),(3,2);
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organisation_organisation`
--

DROP TABLE IF EXISTS `organisation_organisation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organisation_organisation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `label` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `createDate` date NOT NULL,
  `active` tinyint(1) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `logo` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organisation_organisation`
--

LOCK TABLES `organisation_organisation` WRITE;
/*!40000 ALTER TABLE `organisation_organisation` DISABLE KEYS */;
INSERT INTO `organisation_organisation` VALUES (1,'Babana team','Babana dscription','2024-08-17',1,'698844145','image/upload/v1723910978/na2nh4ajlnphayafdnff.png'),(2,'Team 2','description 1','2024-08-17',1,'698844145','media/photos/logo.jpeg');
/*!40000 ALTER TABLE `organisation_organisation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passwordResetCode_passwordresetcode`
--

DROP TABLE IF EXISTS `passwordResetCode_passwordresetcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passwordResetCode_passwordresetcode` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `passwordResetCode_pa_user_id_d4c89d76_fk_utilisate` (`user_id`),
  CONSTRAINT `passwordResetCode_pa_user_id_d4c89d76_fk_utilisate` FOREIGN KEY (`user_id`) REFERENCES `utilisateur_utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passwordResetCode_passwordresetcode`
--

LOCK TABLES `passwordResetCode_passwordresetcode` WRITE;
/*!40000 ALTER TABLE `passwordResetCode_passwordresetcode` DISABLE KEYS */;
INSERT INTO `passwordResetCode_passwordresetcode` VALUES (5,'602934','2024-08-20 04:07:31.151791',3),(6,'698153','2024-08-20 09:40:57.528545',3),(7,'361974','2024-08-20 09:50:38.902989',3),(8,'325227','2024-08-20 10:28:45.311114',3),(9,'834917','2024-08-20 10:36:59.142147',3),(10,'556067','2024-08-20 10:49:07.219665',3);
/*!40000 ALTER TABLE `passwordResetCode_passwordresetcode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `privilegies_privilegies`
--

DROP TABLE IF EXISTS `privilegies_privilegies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `privilegies_privilegies` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `privilege` varchar(20) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `privilegies_privilegies`
--

LOCK TABLES `privilegies_privilegies` WRITE;
/*!40000 ALTER TABLE `privilegies_privilegies` DISABLE KEYS */;
INSERT INTO `privilegies_privilegies` VALUES (1,'ALL',1),(2,'ADD',1),(3,'FIND',1);
/*!40000 ALTER TABLE `privilegies_privilegies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rule_role`
--

DROP TABLE IF EXISTS `rule_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rule_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(20) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rule_role`
--

LOCK TABLES `rule_role` WRITE;
/*!40000 ALTER TABLE `rule_role` DISABLE KEYS */;
INSERT INTO `rule_role` VALUES (1,'ADMIN',1),(2,'USER',1),(3,'MEMBER',1),(4,'CLIENT',1);
/*!40000 ALTER TABLE `rule_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilisateur_utilisateur`
--

DROP TABLE IF EXISTS `utilisateur_utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilisateur_utilisateur` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `username` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `logo` varchar(255) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `rule_id` bigint NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  KEY `utilisateur_utilisateur_rule_id_fcac1592_fk_rule_role_id` (`rule_id`),
  CONSTRAINT `utilisateur_utilisateur_rule_id_fcac1592_fk_rule_role_id` FOREIGN KEY (`rule_id`) REFERENCES `rule_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilisateur_utilisateur`
--

LOCK TABLES `utilisateur_utilisateur` WRITE;
/*!40000 ALTER TABLE `utilisateur_utilisateur` DISABLE KEYS */;
INSERT INTO `utilisateur_utilisateur` VALUES (1,'pbkdf2_sha256$870000$Qagg4E2vlybfuqTV1uybPf$dSS1M4IyJZBQyubX8NAnJPMFFX5OTEKdDi3vPpXQ9WE=',NULL,'admin@gmail.com','admin','',1,'media/photos/logo.jpeg',1,1,1,0),(2,'pbkdf2_sha256$870000$KY0iFQr6t7tYucyCwQZm6m$F+AR+sSxy+oQPXmid3bYoxKazTQArxgG0BW9Yu2h8ac=',NULL,'issamanel05@gmail.com','afromane','698844145',1,'media/photos/logo.jpeg',0,0,1,0),(3,'pbkdf2_sha256$870000$CFtXKWDzFo8wyHSBTPCmde$MerpHn0XK/38tU9jMQ1njVC6JhzzkSlVMuv6oM8qzm4=',NULL,'koirangaalioum@gmail.com','babana','698844145',1,'image/upload/media/photos/logo.jpeg',0,0,2,0),(4,'pbkdf2_sha256$870000$6nGn1LqPi5edEafMoCx94H$YgUn9GpenCqTpvdwk/897R1Y1LFHNb4Cao0A7sWTLKM=',NULL,'jeffnguebou@gmail.com','jeff','699090950',1,'media/photos/logo.jpeg',0,0,4,0),(5,'pbkdf2_sha256$870000$9IKBKeCux7yp3AdApC3RgB$g80cL18/0QCneygZaROutsKEiPcgTne6QLoO5zeWXkA=',NULL,'jeffnguebou237@gmail.com','Ma','655555555',1,'media/photos/logo.jpeg',0,0,4,0),(6,'pbkdf2_sha256$870000$iBunupqa6c6IxnXpO617NC$mNt5WACnw4GDtaBupXMDE3JMhsya2+pWXLYOpSSOw0Q=',NULL,'yannickfomen@gmail.com','Jefferson','677777777',1,'media/photos/logo.jpeg',0,0,4,0),(7,'pbkdf2_sha256$870000$PZS1clqZ4oF33B4QEMKYd6$cram28Szx5YG0Z4fKWBDh3aiY4yZ0toimYWlZHEYYuU=',NULL,'ok@gmail.com','ok','699999900',1,'media/photos/logo.jpeg',0,0,4,0),(8,'pbkdf2_sha256$870000$s28eyGBaf2aXhBbA5FB4gE$i4EhDOnvrM5IasSV9kMblUDqX6t/xhuaJRLdZix7078=',NULL,'accord@gmail.com','accord','655679909',1,'media/photos/logo.jpeg',0,0,4,0),(9,'pbkdf2_sha256$870000$hZ26lO5B8rUO8QlTI4whIH$c2KgWvYJ0tlpf8l7m01QQ1RsTvqqQd7N8BH5BKyHZb0=',NULL,'issammanel15@gmail.com','issa','698844145',1,'media/photos/logo.jpeg',0,0,1,0),(10,'pbkdf2_sha256$870000$pcWB8B636olCLK9g8W3NEb$pCy4mCXQHPxloQvADhdMPPrhhzEvIMZf64spbhLY/pU=',NULL,'issamanel45@gmail.com','manel','698844145',1,'media/photos/logo.jpeg',0,0,1,0),(11,'pbkdf2_sha256$870000$WAmJDMFHJO2KnQcmvVQXT9$WdnlpSI+0cL7mocC6WSxrwk8PI7Bkol9LgpQRWYbK98=',NULL,'koire@gmail.com','koire','698192286',1,'image/upload/media/photos/logo.jpeg',0,0,4,0),(12,'pbkdf2_sha256$870000$Nr6b6rzatYwX0TvrBDELO8$EFYYqN3Jw+vGVYZKgz+sr+9dWIeWv0YTVY+SNILlKQ8=',NULL,'non@gmail.com','non','658778899',1,'media/photos/logo.jpeg',0,0,4,0);
/*!40000 ALTER TABLE `utilisateur_utilisateur` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-27 23:17:29
