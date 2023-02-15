-- MySQL dump 10.13  Distrib 8.0.31, for Linux (x86_64)
--
-- Host: localhost    Database: database_task
-- ------------------------------------------------------
-- Server version	8.0.31-0ubuntu0.22.04.1

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
-- Table structure for table `EmployeeInfo`
--

DROP TABLE IF EXISTS `EmployeeInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EmployeeInfo` (
  `EmpID` int NOT NULL AUTO_INCREMENT,
  `EmpFname` varchar(50) NOT NULL,
  `EmpLname` varchar(50) NOT NULL,
  `Department` varchar(50) NOT NULL,
  `Project` varchar(10) NOT NULL,
  `Address` varchar(100) NOT NULL,
  `DOB` date NOT NULL,
  `Gender` enum('M','F') NOT NULL,
  PRIMARY KEY (`EmpID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmployeeInfo`
--

LOCK TABLES `EmployeeInfo` WRITE;
/*!40000 ALTER TABLE `EmployeeInfo` DISABLE KEYS */;
INSERT INTO `EmployeeInfo` VALUES (1,'Sanjay','Mehra','HR','P1','Hyderabad(HYD)','1976-12-01','M'),(2,'Ananya','Mishra','Admin','P2','Delhi(DEL)','1968-05-02','F'),(3,'Rohan','Diwan','Account','P3','Mumbai(BOM)','1980-01-01','M'),(4,'Sonia','Kulkarni','HR','P1','Hyderabad(HYD)','1992-05-02','F'),(5,'Ankit','Kapoor','Admin','P2','Delhi(DEL)','1994-07-03','M');
/*!40000 ALTER TABLE `EmployeeInfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EmployeePosition`
--

DROP TABLE IF EXISTS `EmployeePosition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EmployeePosition` (
  `EmpID` int NOT NULL AUTO_INCREMENT,
  `EmpPosition` varchar(100) NOT NULL,
  `DateOfJoining` varchar(100) NOT NULL,
  `Salary` decimal(10,0) NOT NULL,
  PRIMARY KEY (`EmpID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmployeePosition`
--

LOCK TABLES `EmployeePosition` WRITE;
/*!40000 ALTER TABLE `EmployeePosition` DISABLE KEYS */;
INSERT INTO `EmployeePosition` VALUES (1,'Manager','2022-05-01',500000),(2,'Executive','2022-05-02',75000),(3,'Manager','2022-05-01',90000),(4,'Lead','2022-05-02',85000),(5,'Executive','2022-05-01',300000);
/*!40000 ALTER TABLE `EmployeePosition` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-23 10:41:05



-- Q&A
-- 1. Write a query to fetch the number of employees working in the department ‘Admin’
SELECT Department, COUNT(*) FROM EmployeeInfo WHERE Department='Admin' GROUP BY Department;
+------------+----------+
| Department | COUNT(*) |
+------------+----------+
| Admin      |        2 |
+------------+----------+


-- 2. Write a query to retrieve the first four characters of  EmpLname from the EmployeeInfo table.
SELECT SUBSTRING(EmpLname, 1, 4) AS 'EmpLname' FROM EmployeeInfo;
+----------+
| EmpLname |
+----------+
| Mehr     |
| Mish     |
| Diwa     |
| Kulk     |
| Kapo     |
+----------+


-- 3. Write q query to find all the employees whose salary is between 50000 to 100000.
SELECT * FROM EmployeePosition WHERE Salary BETWEEN 50000 AND 100000;
+-------+-------------+---------------+--------+
| EmpID | EmpPosition | DateOfJoining | Salary |
+-------+-------------+---------------+--------+
|     2 | Executive   | 2022-05-02    |  75000 |
|     3 | Manager     | 2022-05-01    |  90000 |
|     4 | Lead        | 2022-05-02    |  85000 |
+-------+-------------+---------------+--------+

-- 4. Write a query to find the names of employees that begin with ‘S’
SELECT * FROM EmployeeInfo WHERE EmpFname LIKE 'S%';
+-------+----------+----------+------------+---------+----------------+------------+--------+
| EmpID | EmpFname | EmpLname | Department | Project | Address        | DOB        | Gender |
+-------+----------+----------+------------+---------+----------------+------------+--------+
|     1 | Sanjay   | Mehra    | HR         | P1      | Hyderabad(HYD) | 1976-12-01 | M      |
|     4 | Sonia    | Kulkarni | HR         | P1      | Hyderabad(HYD) | 1992-05-02 | F      |
+-------+----------+----------+------------+---------+----------------+------------+--------+

-- 5. Write a query to fetch top N records order by salary. (ex. top 5 records)
SELECT * FROM EmployeePosition ORDER BY Salary DESC LIMIT 5;
+-------+-------------+---------------+--------+
| EmpID | EmpPosition | DateOfJoining | Salary |
+-------+-------------+---------------+--------+
|     1 | Manager     | 2022-05-01    | 500000 |
|     5 | Executive   | 2022-05-01    | 300000 |
|     3 | Manager     | 2022-05-01    |  90000 |
|     4 | Lead        | 2022-05-02    |  85000 |
|     2 | Executive   | 2022-05-02    |  75000 |
+-------+-------------+---------------+--------+

-- 6. Write a query to fetch details of all employees excluding the employees with first names, “Sanjay” and “Sonia” from the EmployeeInfo table.
SELECT * FROM EmployeeInfo WHERE EmpFname NOT IN ('Sanjay', 'Sonia');
+-------+----------+----------+------------+---------+-------------+------------+--------+
| EmpID | EmpFname | EmpLname | Department | Project | Address     | DOB        | Gender |
+-------+----------+----------+------------+---------+-------------+------------+--------+
|     2 | Ananya   | Mishra   | Admin      | P2      | Delhi(DEL)  | 1968-05-02 | F      |
|     3 | Rohan    | Diwan    | Account    | P3      | Mumbai(BOM) | 1980-01-01 | M      |
|     5 | Ankit    | Kapoor   | Admin      | P2      | Delhi(DEL)  | 1994-07-03 | M      |
+-------+----------+----------+------------+---------+-------------+------------+--------+


-- 7. Write a query to fetch the department-wise count of employees sorted by department’s count in ascending order.
SELECT Department, COUNT(EmpID) FROM EmployeeInfo GROUP BY Department ORDER BY Department ASC;
+------------+--------------+
| Department | COUNT(EmpID) |
+------------+--------------+
| Account    |            1 |
| Admin      |            2 |
| HR         |            2 |
+------------+--------------+


-- 8. Create indexing for any particular field and show the difference in data fetching before and after indexing

-- find the Record who is working in HR department without indexing
-- without indexing it search the every record in Linear fashion
-- Time complexity Take : O(N) in worst Case
EXPLAIN SELECT * FROM EmployeeInfo WHERE Department = "HR";
+----+-------------+--------------+------------+------+---------------+------+---------+------+------+----------+-------------+
| id | select_type | table        | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
+----+-------------+--------------+------------+------+---------------+------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | EmployeeInfo | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    5 |    20.00 | Using where |
+----+-------------+--------------+------------+------+---------------+------+---------+------+------+----------+-------------+

-- create index on department column
CREATE INDEX ind_dept ON EmployeeInfo(Department);

-- index are created | index name : ind_dept
SHOW CREATE TABLE EmployeeInfo;
+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table        | Create Table                                                                                                                                                                                                                                                                                                                                                                                                                                                |
+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| EmployeeInfo | CREATE TABLE `EmployeeInfo` (
  `EmpID` int NOT NULL AUTO_INCREMENT,
  `EmpFname` varchar(50) NOT NULL,
  `EmpLname` varchar(50) NOT NULL,
  `Department` varchar(50) NOT NULL,
  `Project` varchar(10) NOT NULL,
  `Address` varchar(100) NOT NULL,
  `DOB` date NOT NULL,
  `Gender` enum('M','F') NOT NULL,
  PRIMARY KEY (`EmpID`),
  KEY `ind_dept` (`Department`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+--------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

-- search the record who is working on HR department with using indexing
 EXPLAIN SELECT * FROM EmployeeInfo WHERE Department = "HR";
 
 -- see the [ row column ] only 2 row that look
+----+-------------+--------------+------------+------+---------------+----------+---------+-------+------+----------+-------+
| id | select_type | table        | partitions | type | possible_keys | key      | key_len | ref   | rows | filtered | Extra |
+----+-------------+--------------+------------+------+---------------+----------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | EmployeeInfo | NULL       | ref  | ind_dept      | ind_dept | 202     | const |    2 |   100.00 | NULL  |
+----+-------------+--------------+------------+------+---------------+----------+---------+-------+------+----------+-------+





