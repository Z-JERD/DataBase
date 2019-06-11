/*
 Navicat MySQL Data Transfer

 Source Server         : fdm
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : 10.110.1.90:3306
 Source Schema         : arch2018

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 11/06/2019 15:14:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ccc_cinema_trust
-- ----------------------------
DROP TABLE IF EXISTS `ccc_cinema_trust`;
CREATE TABLE `ccc_cinema_trust`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '特定ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '院线简称',
  `full_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '院线全称',
  `tribe` tinyint(4) NULL DEFAULT NULL COMMENT '院线类别，1：一级市场院线，2：二级市场非院线',
  `user_id` bigint(20) NULL DEFAULT NULL COMMENT '对应登录账号id,可为空',
  `trust_address` json NULL COMMENT '{\"sheng\":110000000,\"shi\":110100000,\"xian\":110101000,\"zhen\":110101001,\"city\":110000000,\"sheng_s\":\"xx\",\"shi_s\":\"xx\",\"xian_s\":\"xx\",\"zhen_s\":\"xx\",\"street\":\"xxx\"}',
  `sheng` int(11) GENERATED ALWAYS AS (json_unquote(json_extract(`trust_address`,'$.sheng'))) VIRTUAL NULL,
  `shi` int(11) GENERATED ALWAYS AS (json_unquote(json_extract(`trust_address`,'$.shi'))) VIRTUAL NULL,
  `xian` int(11) GENERATED ALWAYS AS (json_unquote(json_extract(`trust_address`,'$.xian'))) VIRTUAL NULL,
  `address` varchar(900) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci GENERATED ALWAYS AS (concat(json_unquote(json_extract(`trust_address`,'$.sheng_s')),' ',json_unquote(json_extract(`trust_address`,'$.shi_s')),' ',json_unquote(json_extract(`trust_address`,'$.xian_s')),' ',json_unquote(json_extract(`trust_address`,'$.zhen_s')),' ',json_unquote(json_extract(`trust_address`,'$.street')))) VIRTUAL NULL,
  `phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系电话',
  `fax` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '传真',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电子邮箱',
  `last_modified` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '硬盘数量',
  `invalid` int(11) NULL DEFAULT 0 COMMENT '标记删除：0：不删 ，1标删',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 330046 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '管理公司' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ccc_cinema_trust
-- ----------------------------
INSERT INTO `ccc_cinema_trust` VALUES (330001, '万达', '万达', 1, 3614, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:33:08', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330002, '大地影院集团', '大地影院', 1, 7646, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330003, '恒大影管', '恒大影管', 1, 7652, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330004, '星美国际影商城', '星美国际影商城', 1, 9005, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330005, '橙天嘉禾影管', '橙天嘉禾影管', 1, 9006, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330006, '卢米埃', '卢米埃', 1, 9007, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330007, '山东齐纳影管公司', '山东齐纳影管公司', 1, 40, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-12-07 15:45:26', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330008, '大连中影华晨', '大连中影华晨', 1, NULL, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-12-07 15:44:48', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330009, 'CGV', 'CGV', 1, NULL, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-12-07 14:37:03', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330010, '影立方', '影立方', 1, 11325, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330011, '华谊影管', '华谊影管', 1, 11326, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330012, '上影影管', '上影影管', 1, 11327, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330013, '耀莱影管', '耀莱影管', 1, 11328, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330014, '四川太平洋影管', '四川太平洋影管', 1, 11329, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330015, '武商摩尔', '武商摩尔', 1, 11330, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330016, '百誉影管', '百誉影管', 1, 11363, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330017, '比高影管', '比高影管', 1, 11364, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330018, '新干线影管', '新干线影管', 1, 11365, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330019, '新东北影管', '新东北影管', 1, 11366, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330020, '浙江星光影管', '浙江星光影管', 1, 11367, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330021, 'UME影管', 'UME影管', 1, 11423, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330022, '奥斯卡', '奥斯卡', 1, 11424, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330023, '百老汇', '百老汇', 1, 11425, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330024, '博纳影管', '博纳影管', 1, 11426, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330025, '横店影管', '横店影管', 1, 11427, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330026, '华策影管', '华策影管', 1, 11428, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330027, '嘉华影管', '嘉华影管', 1, 11429, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330028, '金逸影管', '金逸影管', 1, 11430, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330029, '美嘉影管', '美嘉影管', 1, 11431, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330030, '完美世界', '完美世界', 1, 11432, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330031, '星轶影管', '星轶影管', 1, 11433, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330032, '幸福蓝海影管', '幸福蓝海影管', 1, 11434, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330033, '越界影管', '越界影管', 1, 11435, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330034, '浙江时代影管', '浙江时代影管', 1, 11436, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330035, '中影影管', '中影影管', 1, 11437, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-11-05 17:24:51', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330036, '左岸风', '左岸风', 1, 11438, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330037, '山东鲁信影管', '山东鲁信影管', 1, 11439, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330038, '珠影影管', '珠影影管', 1, 11440, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330039, '长城沃美影管', '长城沃美影管', 1, 11441, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330040, 'UA影管', 'UA影管', 1, 11445, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-11-05 17:24:49', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330041, '保利影管', '保利影管', 1, 11446, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2018-04-28 16:32:56', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330042, '部队', '部队', 2, NULL, '{\"shi\": \"370200000\", \"city\": \"370200000\", \"xian\": \"370202000\", \"zhen\": \"370202001\", \"sheng\": \"370000000\", \"shi_s\": \"青岛\", \"city_s\": \"青岛市\", \"street\": \"体育馆\", \"xian_s\": \"市南\", \"zhen_s\": \"香港中路街道\", \"sheng_s\": \"山东\", \"latitude\": 36.071601716492566, \"longitude\": 120.39727487683096}', DEFAULT, DEFAULT, DEFAULT, DEFAULT, '15888888888', '068-1234567', 'live7951@gmail.com', '2018-12-07 16:31:16', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330043, '各省广电', '各省广电', 2, NULL, '{\"shi\": 230200000, \"city\": \"230200000\", \"xian\": 230206000, \"zhen\": 230206001, \"sheng\": 230000000, \"shi_s\": \"齐齐哈尔\", \"city_s\": \"齐齐哈尔市\", \"street\": \"123号\", \"xian_s\": \"富拉尔基\", \"zhen_s\": \"红岸街道\", \"sheng_s\": \"黑龙江\", \"latitude\": 47.209416575879075, \"longitude\": 123.65423009573018}', DEFAULT, DEFAULT, DEFAULT, DEFAULT, '15888888888', '068-1234567', 'live7951@gmail.com', '2019-05-22 17:44:02', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330044, '驻京领导', '驻京领导', 2, NULL, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, '', '', '', '2018-12-07 16:31:12', 0);
INSERT INTO `ccc_cinema_trust` VALUES (330045, '中宣部', '中宣部', 2, NULL, NULL, DEFAULT, DEFAULT, DEFAULT, DEFAULT, NULL, NULL, NULL, '2019-05-22 17:44:02', 0);

SET FOREIGN_KEY_CHECKS = 1;
