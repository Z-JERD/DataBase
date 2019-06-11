/*
 Navicat MySQL Data Transfer

 Source Server         : fdm
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : 10.110.1.90:3306
 Source Schema         : fdm

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 11/06/2019 15:09:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pro_secondary_disk
-- ----------------------------
DROP TABLE IF EXISTS `pro_secondary_disk`;
CREATE TABLE `pro_secondary_disk`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `trust_id` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `disk_count` int(11) NOT NULL,
  `disk_type` int(11) NOT NULL COMMENT '发盘类型：1发运、2自取',
  `recipient_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '收盘人',
  `recipient_phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '联系电话',
  `post_address` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '收盘地址',
  `create_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_user` bigint(20) NOT NULL COMMENT '创建人',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '二级市场硬盘申请表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
