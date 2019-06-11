/*
 Navicat MySQL Data Transfer

 Source Server         : bpm_dev
 Source Server Type    : MySQL
 Source Server Version : 50712
 Source Host           : 10.110.1.82:13030
 Source Schema         : bpm_dev

 Target Server Type    : MySQL
 Target Server Version : 50712
 File Encoding         : 65001

 Date: 11/06/2019 15:22:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pro_secondary_subaccount
-- ----------------------------
DROP TABLE IF EXISTS `pro_secondary_subaccount`;
CREATE TABLE `pro_secondary_subaccount`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目编号',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目名称',
  `release_date` date NULL DEFAULT NULL COMMENT '上映时间',
  `code` char(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '排次号、影片编码',
  `edition_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '影片版本名称',
  `zone` tinyint(1) NULL DEFAULT NULL COMMENT '发行范围 0:全国 1:甲区 2:乙区 3:其他 4:无',
  `distributions` json NULL COMMENT '分账结算信息 [{\"start_time\":\"2017-02-01\",\"end_time\":\"2017-03-01\",\"chain\":5700,\"zhongshu\":100,\"huaxia_lease\":4200,huaxia_own:4300}]',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_modify` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最后修改时间',
  `confirmed` int(11) NOT NULL DEFAULT 1,
  `edition` tinyint(1) NULL DEFAULT NULL COMMENT '影片版本',
  `modify_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最新数据添加时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '二级市场院线分账表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pro_secondary_subaccount
-- ----------------------------
INSERT INTO `pro_secondary_subaccount` VALUES (9, 'GFR2018004', '空天猎', NULL, '001106562017', '2D 数字', 3, '[{\"chains\": [223456, 223462], \"end_time\": \"2019-06-05\", \"huaxia_own\": 4300, \"start_time\": \"2019-05-08\", \"create_time\": \"2019-05-29 18:44:29\", \"huaxia_lease\": 4200}, {\"chains\": [223462, 223468, 223475, 223476], \"end_time\": \"2019-08-01\", \"huaxia_own\": 4300, \"start_time\": \"2019-06-14\", \"create_time\": \"2019-05-29 18:48:24\", \"huaxia_lease\": 4200}, {\"chains\": true, \"end_time\": \"2020-07-16\", \"huaxia_own\": 4300, \"start_time\": \"2020-06-27\", \"create_time\": \"2019-06-03 16:31:08\", \"huaxia_lease\": 4200}]', '2019-05-29 18:44:30', '2019-06-03 16:31:08', 1, 1, '2019-06-03 16:31:08');
INSERT INTO `pro_secondary_subaccount` VALUES (10, 'GFR2018002', '明月几时有', NULL, '001100022017', '2D 数字', 3, '[{\"chains\": [223492, 223498], \"end_time\": \"2019-06-05\", \"huaxia_own\": 4300, \"start_time\": \"2019-05-08\", \"create_time\": \"2019-05-29 20:04:51\", \"huaxia_lease\": 4200}, {\"chains\": true, \"end_time\": \"2019-07-10\", \"huaxia_own\": 4300, \"start_time\": \"2019-06-10\", \"create_time\": \"2019-05-30 13:51:11\", \"huaxia_lease\": 4200}]', '2019-05-29 20:04:52', '2019-06-03 15:49:31', 0, 1, '2019-05-30 13:51:11');
INSERT INTO `pro_secondary_subaccount` VALUES (15, 'GFR2018017', '西虹市首富', NULL, '001106062018', '2D 数字', 0, '[{\"chains\": [223474, 223485], \"end_time\": \"2019-06-13\", \"huaxia_own\": 4300, \"start_time\": \"2019-05-07\", \"create_time\": \"2019-05-30 18:11:41\", \"huaxia_lease\": 4200}]', '2019-05-30 18:11:42', '2019-06-03 15:49:31', 1, 1, '2019-05-30 18:11:41');
INSERT INTO `pro_secondary_subaccount` VALUES (18, 'GFR2018004', '空天猎', NULL, '001806562017', '中国巨幕', 0, '[{\"chains\": [223474, 223480, 223487], \"end_time\": \"2019-06-13\", \"huaxia_own\": 4300, \"start_time\": \"2019-05-15\", \"create_time\": \"2019-05-31 16:45:59\", \"huaxia_lease\": 4200}]', '2019-05-31 16:46:00', '2019-05-31 16:46:00', 1, 6, '2019-05-31 16:45:59');
INSERT INTO `pro_secondary_subaccount` VALUES (20, 'GFR2018001', '湄公河行动', NULL, '001105712016', '2D 数字', 3, '[{\"chains\": [223462, 223468], \"end_time\": \"2019-07-18\", \"huaxia_own\": 4300, \"start_time\": \"2019-06-12\", \"create_time\": \"2019-06-03 15:47:09\", \"huaxia_lease\": 4200}]', '2019-06-03 15:47:10', '2019-06-03 15:49:31', 1, 1, '2019-06-03 15:47:09');
INSERT INTO `pro_secondary_subaccount` VALUES (21, 'GFR2018007', '使徒行者', '2018-06-05', '001105072016', '2D 数字', 0, '[{\"chains\": [223462, 223468], \"end_time\": \"2019-07-03\", \"huaxia_own\": 4300, \"start_time\": \"2019-07-03\", \"create_time\": \"2019-06-03 15:57:12\", \"huaxia_lease\": 4200}]', '2019-06-03 15:57:13', '2019-06-03 15:57:13', 1, 1, '2019-06-03 15:57:12');
INSERT INTO `pro_secondary_subaccount` VALUES (22, 'GFR2018003', '二师兄来了', '2018-06-06', '001101902018', '2D 数字', 3, '[{\"chains\": [223474, 223479], \"end_time\": \"2019-07-11\", \"huaxia_own\": 4300, \"start_time\": \"2019-06-04\", \"create_time\": \"2019-06-03 16:12:59\", \"huaxia_lease\": 4200}]', '2019-06-03 16:13:00', '2019-06-03 16:13:00', 1, 1, '2019-06-03 16:12:59');
INSERT INTO `pro_secondary_subaccount` VALUES (23, 'GFR2018019', '擒贼先擒王', '2019-05-10', '001101432018', '2D 数字', 3, '[{\"chains\": [223456, 223462, 223468], \"end_time\": \"2019-07-18\", \"huaxia_own\": 4300, \"start_time\": \"2019-06-07\", \"create_time\": \"2019-06-06 10:04:23\", \"huaxia_lease\": 4200}]', '2019-06-06 10:04:23', '2019-06-06 10:04:23', 1, 1, '2019-06-06 10:04:23');

SET FOREIGN_KEY_CHECKS = 1;
