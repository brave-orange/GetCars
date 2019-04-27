/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1_3306
Source Server Version : 50625
Source Host           : 127.0.0.1:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50625
File Encoding         : 65001

Date: 2019-04-27 12:51:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for cars
-- ----------------------------
DROP TABLE IF EXISTS `cars`;
CREATE TABLE `cars` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `car_name` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `sorce` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `type` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `engine` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `car_body` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `gearbox` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `price` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `img` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `brand` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6458 DEFAULT CHARSET=latin1;
