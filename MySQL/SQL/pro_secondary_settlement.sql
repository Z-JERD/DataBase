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

 Date: 11/06/2019 15:09:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pro_secondary_settlement
-- ----------------------------
DROP TABLE IF EXISTS `pro_secondary_settlement`;
CREATE TABLE `pro_secondary_settlement`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL COMMENT '对应 二级市场项目自增ID',
  `chain_type` int(11) NOT NULL DEFAULT 2 COMMENT '1院线/2非院线',
  `chain` int(11) NULL DEFAULT NULL COMMENT '院线放映中的 院线ID',
  `publish_type` int(11) NULL DEFAULT NULL COMMENT '1买断/2分账',
  `cinema_trust` int(11) NULL DEFAULT NULL COMMENT '影管ID',
  `cinema_trust_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '影管名称',
  `start_date` date NULL DEFAULT NULL COMMENT '结算期 开始日期',
  `end_date` date NULL DEFAULT NULL COMMENT '结算期 截止日期',
  `shows` int(11) NULL DEFAULT NULL COMMENT '总场次',
  `revenue` bigint(20) NULL DEFAULT NULL COMMENT '分账片总票房（单位：分）',
  `amount` bigint(20) NULL DEFAULT NULL COMMENT '发行总收入（单位：分）',
  `moviecodes` json NULL COMMENT '排次号：[\'012345678901\',\'\'...]',
  `distributions` json NULL COMMENT '分账比例{\"chain\":5700,\"zhongshu\":100,\"huaxia_own\":4300,\"huaxia_lease\":4200}',
  `status` int(11) NULL DEFAULT 1 COMMENT '1待发布，2已发布，3已废弃',
  `settled` int(11) NULL DEFAULT 0 COMMENT '是否已经参与片方结算：0否，1是',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '放映方结算表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pro_secondary_settlement
-- ----------------------------
INSERT INTO `pro_secondary_settlement` VALUES (1, 17, 1, 223457, 2, NULL, NULL, '2018-11-09', '2018-11-16', NULL, NULL, 888800, NULL, '{\"chain\": 4900, \"zhongshu\": 900, \"huaxia_own\": 5100, \"huaxia_lease\": 4200}', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (3, 17, 1, 223461, 1, NULL, NULL, '2018-12-09', '2018-12-22', NULL, NULL, 666700, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (4, 17, 1, 223460, 2, NULL, NULL, '2018-12-01', '2018-12-06', NULL, NULL, 77770000, NULL, '{\"chain\": 100, \"zhongshu\": 200, \"huaxia_own\": 9900, \"huaxia_lease\": 9700}', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (6, 17, 1, 223459, 1, 330005, NULL, '2018-11-24', '2018-12-07', NULL, NULL, 555000, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (7, 17, 2, NULL, NULL, 330002, NULL, '2018-11-27', '2018-12-16', 223, NULL, 22200, NULL, 'null', 2, 0);
INSERT INTO `pro_secondary_settlement` VALUES (8, 17, 2, NULL, NULL, 330006, NULL, '2018-11-22', '2018-11-25', 111, NULL, 345600, NULL, 'null', 2, 0);
INSERT INTO `pro_secondary_settlement` VALUES (9, 17, 2, NULL, NULL, 330044, '驻京领导', '2018-10-30', '2018-12-01', 123, NULL, 45600, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (10, 17, 1, 223457, 1, NULL, NULL, '2018-11-30', '2019-12-14', NULL, NULL, 12300, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (11, 17, 1, 223457, 1, NULL, NULL, '2018-12-22', '2018-12-28', NULL, NULL, NULL, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (12, 19, 1, 223457, 1, NULL, NULL, '2018-11-10', '2018-12-12', NULL, NULL, NULL, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (13, 17, 1, 223457, 1, NULL, NULL, '2018-11-10', '2018-12-06', NULL, NULL, 400, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (14, 19, 2, NULL, NULL, 330044, '驻京领导', '2018-12-06', '2018-12-09', 2, NULL, 200, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (15, 17, 1, 223456, 2, NULL, NULL, '2018-12-05', '2018-12-08', NULL, NULL, NULL, NULL, '{\"chain\": 10000, \"zhongshu\": 0, \"huaxia_own\": 0, \"huaxia_lease\": 0}', 1, 0);
INSERT INTO `pro_secondary_settlement` VALUES (16, 17, 1, 223457, 1, NULL, NULL, '2018-12-04', '2018-12-07', NULL, NULL, 500, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (18, 17, 1, 223458, 1, NULL, NULL, '2018-12-04', '2018-11-30', NULL, NULL, 100, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (19, 1, 1, 223457, 1, NULL, NULL, '2018-12-04', '2018-12-06', NULL, NULL, 100, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (20, 1, 2, 330044, NULL, NULL, NULL, '2018-12-05', '2018-12-06', 1, NULL, 100, NULL, 'null', 1, 0);
INSERT INTO `pro_secondary_settlement` VALUES (21, 6, 2, 330044, NULL, 330044, '驻京领导', '2018-12-05', '2018-12-07', NULL, NULL, NULL, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (22, 5, 2, 330044, NULL, 330044, '驻京领导', '2018-12-05', '2018-12-07', NULL, NULL, NULL, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (23, 4, 2, 330044, NULL, 330044, '驻京领导', '2018-11-28', '2018-12-06', NULL, NULL, NULL, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (25, 7, 2, 330044, NULL, 330044, '驻京领导', '2018-12-04', '2018-12-13', NULL, NULL, NULL, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (26, 2, 2, 330044, NULL, 330044, '驻京领导', '2018-11-28', '2018-12-05', NULL, NULL, NULL, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (27, 3, 1, 223457, 2, 223457, NULL, '2018-11-28', '2018-12-06', NULL, NULL, NULL, NULL, '{\"chain\": 9800, \"zhongshu\": 0, \"huaxia_own\": 200, \"huaxia_lease\": 200}', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (28, 17, 1, 223457, 2, NULL, NULL, '2018-11-28', '2018-12-07', NULL, NULL, 99999900, NULL, '{\"chain\": 4600, \"zhongshu\": 2200, \"huaxia_own\": 5400, \"huaxia_lease\": 3200}', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (30, 1, 2, 330044, NULL, 330044, '驻京领导', '2018-12-04', '2018-12-06', NULL, NULL, NULL, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (31, 1, 1, 223457, 2, 223457, NULL, '2018-12-01', '2018-12-31', NULL, NULL, 10000000, NULL, '{\"chain\": 9000, \"zhongshu\": 500, \"huaxia_own\": 1000, \"huaxia_lease\": 500}', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (32, 3, 2, 330044, NULL, 330044, '驻京领导', '2018-12-12', '2018-12-14', 3, NULL, NULL, NULL, 'null', 1, 0);
INSERT INTO `pro_secondary_settlement` VALUES (34, 6, 2, 330042, NULL, 330042, NULL, '2018-12-05', '2018-12-08', 5, NULL, 200, NULL, 'null', 3, 0);
INSERT INTO `pro_secondary_settlement` VALUES (35, 1, 1, 223456, 2, 223456, NULL, '2018-11-27', '2018-12-01', NULL, NULL, 100, NULL, '{\"chain\": 9900, \"zhongshu\": 0, \"huaxia_own\": 100, \"huaxia_lease\": 100}', 1, 0);

SET FOREIGN_KEY_CHECKS = 1;
