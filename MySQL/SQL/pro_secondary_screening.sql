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

 Date: 11/06/2019 15:22:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pro_secondary_screening
-- ----------------------------
DROP TABLE IF EXISTS `pro_secondary_screening`;
CREATE TABLE `pro_secondary_screening`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cinema_trust` int(11) NOT NULL COMMENT '放映方id',
  `cinema_trust_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预付款放映方名称',
  `pid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目编号',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目名称',
  `start_date` date NULL DEFAULT NULL COMMENT '放映开始日期',
  `end_date` date NULL DEFAULT NULL COMMENT '放映结束日期',
  `shows` int(11) NULL DEFAULT NULL COMMENT '总场次',
  `rent_income` decimal(20, 2) NULL DEFAULT NULL COMMENT '放映方对应的片租收入',
  `bind_imprest` int(11) NULL DEFAULT 0 COMMENT '放映方是否绑定预付款：0否，1是',
  `imprest_unit_ids` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '对应的预付款单位id',
  `imprest_data` json NULL COMMENT '绑定的预付款数据',
  `amount` decimal(20, 2) NULL DEFAULT NULL COMMENT '实际到账收入',
  `settled` int(11) NULL DEFAULT 0 COMMENT '结算状态：0 未结算，1 结算中 2 已结算',
  `task_id` bigint(20) NULL DEFAULT NULL COMMENT '对应的结算任务自增id',
  `account_time` datetime(0) NULL DEFAULT NULL COMMENT '放映登记的结算日期',
  `financial_voucher` json NULL COMMENT '放映方绑定当前项目对应的NC数据 {\"1001A11000000001LY11\":{.....}, \"1001A11000000001LXTT\":{.....} }',
  `invalid` int(10) NOT NULL DEFAULT 0 COMMENT '标记删除 0：未删除 1：删除',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_modify` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最后修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '二级市场放映登记表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pro_secondary_screening
-- ----------------------------
INSERT INTO `pro_secondary_screening` VALUES (24, 330042, '部队', 'GFR2018001', '湄公河行动', '2019-06-01', '2019-06-03', 2, 20000.00, 0, NULL, '[]', 20000.00, 1, 24, NULL, '{\"1001A11000000001LXTT\": {\"R\": 2, \"NOV\": 0, \"bind\": false, \"ASSID\": \"1001A11000000001LHD0\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"00\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"C\", \"PK_DETAIL\": \"1001A11000000001LXX2\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001LXTT\", \"DEBITAMOUNT\": 0, \"EXPLANATION\": \"##20000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 600, \"PROJECT_CODE\": \"GFR2018001\", \"PROJECT_NAME\": \"湄公河行动（EJ）\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"10\", \"MARCLASS_NAME\": \"二级市场影片\", \"MATERIAL_CODE\": \"HY00000769\", \"MATERIAL_NAME\": \"湄公河行动（EJ）\", \"pretax_amount\": \"20000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": 600}}', 0, '2019-06-05 14:03:12', '2019-06-10 16:06:10');
INSERT INTO `pro_secondary_screening` VALUES (25, 330042, '部队', 'GFR2018017', '西虹市首富', '2019-06-06', '2019-06-09', 1, 20000.00, 0, NULL, '[]', 0.00, 0, NULL, NULL, '{}', 0, '2019-06-05 14:04:38', '2019-06-06 14:57:13');
INSERT INTO `pro_secondary_screening` VALUES (26, 330042, '部队', 'GFR2018012', '巨额来电', '2019-06-17', '2019-06-22', 1, 30000.00, 0, NULL, '[]', 30000.00, 1, 24, NULL, '{\"1001A11000000001GFR22\": {\"NOV\": 247, \"bind\": false, \"ASSID\": \"1001A11000000001LFHF\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"01\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"C\", \"PK_DETAIL\": \"1001A11000000001J168\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001GFR22\", \"DEBITAMOUNT\": 0, \"EXPLANATION\": \"##30000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 2000, \"PROJECT_CODE\": \"GFR2018012\", \"PROJECT_NAME\": \"巨额来电\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"0109\", \"MARCLASS_NAME\": \"2018年国产影片\", \"MATERIAL_CODE\": \"HY00000772\", \"MATERIAL_NAME\": \"巨额来电\", \"pretax_amount\": \"30000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": 66037.74}}', 0, '2019-06-05 14:05:19', '2019-06-10 16:06:10');
INSERT INTO `pro_secondary_screening` VALUES (27, 330043, '各省广电', 'GFR2018001', '湄公河行动', '2019-07-01', '2019-07-04', 1, 40000.00, 0, NULL, '[]', 40000.00, 1, 24, NULL, '{\"1001A11000000001LHGX\": {\"R\": 1, \"NOV\": 0, \"bind\": false, \"ASSID\": \"1001A11000000001LHD0\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"00\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"C\", \"PK_DETAIL\": \"1001A11000000001LHJY\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001LHGX\", \"DEBITAMOUNT\": 0, \"EXPLANATION\": \"##30000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 600, \"PROJECT_CODE\": \"GFR2018001\", \"PROJECT_NAME\": \"湄公河行动（EJ）\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"10\", \"MARCLASS_NAME\": \"二级市场影片\", \"MATERIAL_CODE\": \"HY00000769\", \"MATERIAL_NAME\": \"湄公河行动（EJ）\", \"pretax_amount\": \"30000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": 600}, \"1001A11000000001LY11\": {\"R\": 3, \"NOV\": 0, \"bind\": false, \"ASSID\": \"1001A11000000001LHD0\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"00\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"C\", \"PK_DETAIL\": \"1001A11000000001LY48\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001LY11\", \"DEBITAMOUNT\": 0, \"EXPLANATION\": \"##10000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": -600, \"PROJECT_CODE\": \"GFR2018001\", \"PROJECT_NAME\": \"湄公河行动（EJ）\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"10\", \"MARCLASS_NAME\": \"二级市场影片\", \"MATERIAL_CODE\": \"HY00000769\", \"MATERIAL_NAME\": \"湄公河行动（EJ）\", \"pretax_amount\": \"10000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": -600}}', 0, '2019-06-05 14:06:26', '2019-06-10 16:06:10');
INSERT INTO `pro_secondary_screening` VALUES (28, 330043, '各省广电', 'GFR2018012', '巨额来电', '2019-06-11', '2019-06-21', 1, 100000.00, 0, NULL, '[]', 0.00, 0, NULL, NULL, '{}', 0, '2019-06-05 14:40:21', '2019-06-10 15:57:13');
INSERT INTO `pro_secondary_screening` VALUES (29, 330043, '各省广电', 'GFR2018017', '西虹市首富', '2019-06-04', '2019-06-07', 1, 110000.00, 0, NULL, '[]', 110000.00, 1, 24, NULL, '{\"1001A11000000001ZGF\": {\"R\": 4, \"NOV\": 0, \"bind\": false, \"ASSID\": \"1001A11000000001LHD0\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"00\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"D\", \"PK_DETAIL\": \"1001A11000000001LY48\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001ZGF\", \"DEBITAMOUNT\": 900, \"EXPLANATION\": \"##30000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 0, \"PROJECT_CODE\": \"GF2018063\", \"PROJECT_NAME\": \"西虹市首富\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"0109\", \"MARCLASS_NAME\": \"2018年国产影片\", \"MATERIAL_CODE\": \"HY00000771\", \"MATERIAL_NAME\": \"西虹市首富\", \"pretax_amount\": \"30000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": -600}, \"1001A11000000001HGZX\": {\"R\": 3, \"NOV\": 0, \"bind\": false, \"ASSID\": \"1001A11000000001LHD0\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"00\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"D\", \"PK_DETAIL\": \"1001A11000000001LY48\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001HGZX\", \"DEBITAMOUNT\": 800, \"EXPLANATION\": \"##10000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 0, \"PROJECT_CODE\": \"GF2018063\", \"PROJECT_NAME\": \"西虹市首富\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"0109\", \"MARCLASS_NAME\": \"2018年国产影片\", \"MATERIAL_CODE\": \"HY00000771\", \"MATERIAL_NAME\": \"西虹市首富\", \"pretax_amount\": \"10000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": -600}, \"1001A11000000001J166\": {\"NOV\": 247, \"bind\": false, \"ASSID\": \"1001A11000000001LFHF\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"01\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"D\", \"PK_DETAIL\": \"1001A11000000001J168\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001J166\", \"DEBITAMOUNT\": 0, \"EXPLANATION\": \"##20000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 66037.74, \"PROJECT_CODE\": \"GF2018063\", \"PROJECT_NAME\": \"西虹市首富\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"0109\", \"MARCLASS_NAME\": \"    2018年国产影片\", \"MATERIAL_CODE\": \"HY00000771\", \"MATERIAL_NAME\": \"西虹市首富\", \"pretax_amount\": \"20000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": 66037.74}, \"1001A11000000001JERD\": {\"R\": 5, \"NOV\": 0, \"bind\": false, \"ASSID\": \"1001A11000000001LHD0\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"00\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"D\", \"PK_DETAIL\": \"1001A11000000001LY48\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001JERD\", \"DEBITAMOUNT\": 900, \"EXPLANATION\": \"##10000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 0, \"PROJECT_CODE\": \"GF2018063\", \"PROJECT_NAME\": \"西虹市首富\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"0109\", \"MARCLASS_NAME\": \"2018年国产影片\", \"MATERIAL_CODE\": \"HY00000771\", \"MATERIAL_NAME\": \"西虹市首富\", \"pretax_amount\": \"10000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": -600}, \"1001A11000000001LHGX\": {\"NOV\": 0, \"bind\": false, \"ASSID\": \"1001A11000000001LHGT\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"00\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"C\", \"PK_DETAIL\": \"1001A11000000001LHNW\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001LHGX\", \"DEBITAMOUNT\": 0, \"EXPLANATION\": \"##40000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 10000, \"PROJECT_CODE\": \"GF2018063\", \"PROJECT_NAME\": \"西虹市首富\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"0109\", \"MARCLASS_NAME\": \"    2018年国产影片\", \"MATERIAL_CODE\": \"HY00000771\", \"MATERIAL_NAME\": \"西虹市首富\", \"pretax_amount\": \"40000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": 10000}}', 0, '2019-06-05 14:41:46', '2019-06-10 16:06:10');
INSERT INTO `pro_secondary_screening` VALUES (30, 330044, '驻京领导', 'GFR2018017', '西虹市首富', '2019-06-06', '2019-06-07', 1, 2000.00, 1, '18', '[{\"imprest_id\": 18, \"rent_income\": \"2000.00\", \"imprest_name\": \"驻京领导\"}]', NULL, 0, NULL, NULL, NULL, 1, '2019-06-05 16:41:19', '2019-06-05 16:52:38');
INSERT INTO `pro_secondary_screening` VALUES (31, 330044, '驻京领导', 'GFR2018012', '巨额来电', '2019-06-11', '2019-06-12', 1, 10000.00, 1, '18', '[{\"imprest_id\": 18, \"rent_income\": \"10000.00\", \"imprest_name\": \"驻京领导\"}]', 10000.00, 1, 24, NULL, '{\"1001A11000000001GFR20\": {\"NOV\": 247, \"bind\": false, \"ASSID\": \"1001A11000000001LFHF\", \"YEARV\": \"2019\", \"PK_ORG\": \"0001A610000000002RN3\", \"PERIODV\": \"01\", \"CURR_CODE\": \"CNY\", \"CURR_NAME\": \"人民币\", \"DIRECTION\": \"C\", \"PK_DETAIL\": \"1001A11000000001J168\", \"screen_id\": null, \"PK_VOUCHER\": \"1001A11000000001GFR20\", \"DEBITAMOUNT\": 0, \"EXPLANATION\": \"##10000.00##，期初\", \"ACCOUNT_CODE\": \"22020602\", \"ACCOUNT_NAME\": \"二级市场片租收入\", \"CREDITAMOUNT\": 66037.74, \"PROJECT_CODE\": \"GFR2018012\", \"PROJECT_NAME\": \"巨额来电\", \"DEBITQUANTITY\": 0, \"MARCLASS_CODE\": \"0109\", \"MARCLASS_NAME\": \"2018年国产影片\", \"MATERIAL_CODE\": \"HY00000772\", \"MATERIAL_NAME\": \"巨额来电\", \"pretax_amount\": \"10000.00\", \"CREDITQUANTITY\": 0, \"LOCALDEBITAMOUNT\": 0, \"LOCALCREDITAMOUNT\": 66037.74}}', 0, '2019-06-05 16:53:15', '2019-06-10 16:06:10');

SET FOREIGN_KEY_CHECKS = 1;
