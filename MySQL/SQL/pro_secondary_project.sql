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

 Date: 11/06/2019 15:07:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pro_secondary_project
-- ----------------------------
DROP TABLE IF EXISTS `pro_secondary_project`;
CREATE TABLE `pro_secondary_project`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '二级市场子项目自增ID',
  `pid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '要显示的项目编号',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目名称',
  `movie_project_id` bigint(20) NULL DEFAULT NULL COMMENT '关联的发行项目id 或 影片项目',
  `authorize_start_time` datetime(0) NULL DEFAULT NULL COMMENT '项目授权开始时间',
  `authorize_end_time` datetime(0) NULL DEFAULT NULL COMMENT '项目授权结束时间',
  `settlement_producer` json NULL COMMENT '片方结算数据：json格式：{\"settlement_object\":[{\"bank\":\"招商银行天津新港支行\",\"index\":\"1\",\"remark\":\"\",\"object_name\":\"结算对象一\",\"account_name\":\"华策影业（天津）有限公司\",\"bank_account\":\"122905052810601\"}],huaxia_rate:3000,settelment_time:\"每半年进行一次结算\"}',
  `duty_person` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '项目认领人(客户经理)姓名',
  `duty_person_id` int(11) NULL DEFAULT NULL COMMENT '项目认领人(客户经理account_manager)用户ID',
  `duty_person_array` json NULL COMMENT '项目责任人复数',
  `duty_person_idx` json NULL COMMENT '项目责任人复数索引',
  `contract` json NULL COMMENT '合同数据[{doc_type:6,doc_names:,doc_id,origin_name},,,,,]',
  `permits` json NULL COMMENT '许可证[{doc_type:6,doc_names:,doc_id,origin_name},,,,,]',
  `origin` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '国别',
  `release_date` date NULL DEFAULT NULL COMMENT '上映时间',
  `create_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modify` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最后修改时间，请勿修改',
  `fares` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '最低票价',
  `rerun_date` date NULL DEFAULT NULL COMMENT '复映时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `pid`(`pid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '二级市场项目表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pro_secondary_project
-- ----------------------------
INSERT INTO `pro_secondary_project` VALUES (1, 'GFR2018001', '湄公河行动', 1530158611, '2018-06-01 00:00:00', '2018-10-31 00:00:00', '{\"settlement_object\": [{\"bank\": \"招商银行股份有限公司上海分行营业部\", \"index\": \"1\", \"remark\": \"\", \"object_name\": \"结算对象一\", \"account_name\": \"上海淘票票影视文化有限公司\", \"bank_account\": \"121922013310201\"}]}', '崔佳', 76, NULL, NULL, '[]', '[]', '中国', '2018-08-17', '2018-11-22 13:54:04', '2019-06-10 11:37:04', 'A类城市4个：北京、上海、广州、深圳', '2018-09-05');
INSERT INTO `pro_secondary_project` VALUES (2, 'GFR2018002', '明月几时有', 1497577281727, '2018-06-01 00:00:00', '2018-10-31 00:00:00', NULL, '崔佳', 76, NULL, NULL, '[]', '[]', NULL, NULL, '2018-11-22 13:54:04', '2019-06-03 15:49:37', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (3, 'GFR2018003', '二师兄来了', 1522120258968, '2019-05-31 00:00:00', NULL, '{\"huaxia_chain_rate\": 1200, \"settlement_object\": [{\"bank\": \"招行华贸中心支行\", \"index\": \"1\", \"remark\": \"\", \"object_name\": \"结算对象一\", \"account_name\": \"指点影业（北京）有限公司\", \"bank_account\": \"110915213110502\"}], \"huaxia_cinema_trust_rate\": 5400}', '崔佳', 76, NULL, NULL, '[]', '[]', '中国', '2018-05-10', '2018-11-22 13:54:04', '2019-06-03 16:11:45', '', '2018-06-06');
INSERT INTO `pro_secondary_project` VALUES (4, 'GFR2018004', '空天猎', 1501472492040, '2017-11-13 00:00:00', '2022-11-12 00:00:00', '{\"settlement_object\": [{\"bank\": \"中国民生银行股份有限公司北京首体南路支行\", \"index\": \"1\", \"remark\": \"\", \"object_name\": \"结算对象一\", \"account_name\": \"霍尔果斯春秋时代文化传媒有限公司\", \"bank_account\": \"696746072\"}, {\"bank\": \"工行杭州茅廊巷支行\", \"index\": \"2\", \"remark\": \"\", \"object_name\": \"结算对象二\", \"account_name\": \"华策影业（天津）有限公司\", \"bank_account\": \"1202053019900101585\"}, {\"bank\": \"中国银行北京大北窑支行\", \"index\": \"3\", \"remark\": \"\", \"object_name\": \"结算对象三\", \"account_name\": \"寰宇纵横世纪电影发行（北京）有限公司\", \"bank_account\": \"319462811484\"}]}', '崔佳', 76, NULL, NULL, '[]', '[]', '国产', '2018-06-03', '2018-11-22 13:54:04', '2019-06-03 16:09:53', '最低票价五十元', '2018-07-03');
INSERT INTO `pro_secondary_project` VALUES (5, 'GFR2018005', '十八洞村', NULL, '2018-06-01 00:00:00', '2018-10-31 00:00:00', NULL, '王天石', 13, NULL, NULL, '[]', '[]', NULL, NULL, '2018-11-22 13:54:04', '2019-05-31 12:45:49', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (6, 'GFR2018006', '豆福传', NULL, NULL, NULL, NULL, '崔佳', 76, NULL, NULL, '[]', '[]', NULL, NULL, '2018-11-22 13:54:04', '2018-11-22 13:54:04', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (7, 'GFR2018007', '使徒行者', 1469609718112, NULL, NULL, NULL, '崔佳', 76, NULL, NULL, '[]', '[]', NULL, '2018-05-05', '2018-11-22 13:54:04', '2019-06-03 15:57:26', NULL, '2018-06-05');
INSERT INTO `pro_secondary_project` VALUES (8, 'GFR2018008', '七月与安生', 1473737409497, NULL, NULL, NULL, '崔佳', 76, NULL, NULL, '[]', '[]', NULL, NULL, '2018-11-22 13:54:04', '2018-11-27 15:54:14', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (9, 'GFR2018009', '傲娇与偏见', 1490684960905, '2017-03-24 00:00:00', '2018-03-23 00:00:00', '{\"settlement_object\": [{\"bank\": \"招商银行股份有限公司上海分行营业部\", \"index\": \"1\", \"remark\": \"\", \"object_name\": \"结算对象一\", \"account_name\": \"上海淘票票影视文化有限公司\", \"bank_account\": \"121922013310201\"}]}', '崔佳', 76, NULL, NULL, '[]', '[]', '中国', NULL, '2018-11-22 13:54:04', '2019-05-31 12:45:49', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (10, 'GFR2018010', '冰河追凶', NULL, NULL, NULL, NULL, '崔佳', 76, NULL, NULL, '[]', '[]', NULL, NULL, '2018-11-22 13:54:04', '2018-11-22 13:54:04', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (11, 'GFR2018011', '情圣', 1480903007789, '1970-01-16 00:00:00', '1970-01-23 00:00:00', '{\"settlement_object\": [{\"bank\": \"招商银行股份有限公司北京阜外大街支行\", \"index\": \"1\", \"remark\": \"\", \"object_name\": \"结算对象一\", \"account_name\": \"天津猫眼文化传媒有限公司\", \"bank_account\": \"110917150710902\"}]}', '崔佳', 76, NULL, NULL, '[]', '[]', '中国', NULL, '2018-11-22 13:54:04', '2019-05-31 12:45:49', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (12, 'GFR2018012', '巨额来电', 1508222437973, '2017-11-22 00:00:00', '2018-12-08 00:00:00', '{\"agent_fee\": {\"contract_text\": \"    甲、乙双方确认，双方各自提取本片在中国大陆地区（不含香港、澳门、台湾地区）院线票房分账收入的5%作为发行代理费。\\n     甲、乙双方同意，双方根据本片应得的发行收入按以下顺序回收和分配：\\n（1）首先扣除乙方应得的发行服务费；\\n（2）乙方需根据本合同第五条第8款第(1)项进行每期结算时；甲乙双方应同时共同制作本片的宣发决算报告，并同时确认宣发决算报告中双方就本片垫付之宣传发行费用和每期结算甲乙双方可扣除实际垫付之宣传发行费用之数额及甲乙双方应得之发行代理费，为免歧义，在完成上述之决算过程中，甲乙双方按照决算报告中已确定各自实际垫付的宣发费用比例同时回收各自垫付的宣传发行费用；\\n(3) 待甲乙双方确认每期可扣除实际垫付之宣传发行费用之数额及甲乙双方应得之发行代理费后，再扣除双方确认宣发决算报告中乙方垫付的宣传发行费用。在净分账收入扣除经确认的乙方垫付的宣传发行费用后之款项，则视为剩余发行收入(以下简称“剩余发行收入”。\\n（4）乙方将剩余发行收入(当中包括甲方在当期结算中确认的甲方可扣除实际垫付之宣传发行费用之数额及甲乙双方应得之发行代理费)，支付至甲方指定的银行账户；\\n（5）甲方将乙方应得的发行代理费支付至乙方指定的银行账户。\\n\"}, \"digital_fee\": {\"docs\": [{\"type\": \"image\", \"doc_id\": \"3950\", \"thumbs\": [\"33ekq3jeh6dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"33ekq3jeh6dev0.jpeg\", \"doc_type\": \"12\", \"origin_name\": \"《巨额来电》数字制作费清单.jpg\"}], \"payway\": {\"qita\": \"包含在华影宣发预算中\"}, \"sum_digital_fee_1\": \"1000000\", \"sum_digital_fee_2\": \"14247500\", \"sum_digital_fee_3\": \"12208000\"}, \"service_fee\": {\"data\": {\"huaxia_max\": \"2000000\", \"huaxia_rate\": \"100\"}, \"function_name\": \"huaxia_rate_max\", \"boxoffice_type\": \"净票房非中数部分\", \"distribute_object\": \"华夏分成\"}, \"settlement_time\": {\"months\": \"3\", \"start_time\": \"2018-01-07\"}, \"settlement_object\": [{\"bank\": \"中国银行北京大北窑支行\", \"index\": \"1\", \"remark\": \"\", \"object_name\": \"结算对象一\", \"account_name\": \"寰宇纵横世纪电影发行（北京）有限公司\", \"bank_account\": \"319462811484\"}]}', '崔佳', 76, NULL, NULL, '[{\"type\": \"image\", \"thumbs\": [\"28hqj1mr9tdev0.png\"], \"catalog\": \"prjdoc\", \"doc_name\": \"28hqj1mr9tdev0.png\", \"doc_type\": \"6\", \"origin_name\": \"20180524195019372.png\"}]', '[]', '中国', NULL, '2018-11-22 13:54:04', '2019-05-31 12:45:49', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (13, 'GFR2018013', '决战食神', 1484290733876, NULL, NULL, NULL, '崔佳', 76, NULL, NULL, '[]', '[]', NULL, NULL, '2018-11-22 13:54:04', '2018-11-27 15:45:21', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (14, 'GFR2018014', '悟空传', 1498788478362, NULL, NULL, NULL, '崔佳', 76, NULL, NULL, '[]', '[]', NULL, NULL, '2018-11-22 13:54:04', '2018-11-23 11:07:11', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (15, 'GFR2018015', '大耳朵图图之美食狂想曲', 1499240594084, '2017-07-05 00:00:00', '2018-01-31 00:00:00', '{\"settlement_object\": [{\"bank\": \"中国光大银行股份有限公司上海市西支行\", \"index\": \"1\", \"remark\": \"\", \"object_name\": \"结算对象一\", \"account_name\": \"上海民新影视娱乐有限公司\", \"bank_account\": \"36690188000170295\"}]}', '崔佳', 76, NULL, NULL, '[]', '[]', '中国', NULL, '2018-11-22 13:54:04', '2019-05-31 12:45:50', NULL, NULL);
INSERT INTO `pro_secondary_project` VALUES (16, 'GFR2018016', '机器之血', 1511416918642, NULL, NULL, '{\"huaxia_rate\": 0, \"settelment_time\": \"机器之血的结算周期说明\", \"settlement_object\": []}', '崔佳', 76, NULL, NULL, '[]', '[]', '中国', NULL, '2018-11-22 13:54:04', '2019-06-03 15:52:33', NULL, '2019-06-13');
INSERT INTO `pro_secondary_project` VALUES (17, 'GFR2018017', '西虹市首富', 1531897014994, '2018-12-19 00:00:00', '2019-03-18 00:00:00', '{\"index\": \"undefined\", \"huaxia_rate\": 0, \"settelment_time\": \"这里填结算周期\", \"huaxia_chain_rate\": 1200, \"settlement_object\": [{\"bank\": \"22222222222222\", \"index\": \"5\", \"remark\": \"这是一备注\", \"object_name\": \"结算对象五\", \"account_name\": \"张三\", \"bank_account\": \"121312313131231\"}, {\"bank\": \"33333333333333\", \"index\": \"8\", \"remark\": \"\", \"object_name\": \"结算对象八\", \"account_name\": \"李四\", \"bank_account\": \"3456246524523452345\"}, {\"bank\": \"1111111111111\", \"index\": \"9\", \"remark\": \"\", \"object_name\": \"结算对象九\", \"account_name\": \"啊手动阀\", \"bank_account\": \"342523523523452354\"}], \"huaxia_cinema_trust_rate\": 2400}', '崔佳', 76, NULL, NULL, '[]', '[]', '中国', NULL, '2018-11-22 13:54:04', '2019-06-03 15:52:22', NULL, '2018-11-22');
INSERT INTO `pro_secondary_project` VALUES (18, 'GFR2018018', '藏北秘岭-重返无人区', 1540881752199, NULL, NULL, NULL, '崔佳', 76, NULL, NULL, '[]', '[]', NULL, NULL, '2018-11-22 13:54:04', '2019-06-03 15:51:49', NULL, '2019-06-05');
INSERT INTO `pro_secondary_project` VALUES (19, 'GFR2018019', '擒贼先擒王', 1522208673370, '2018-05-18 00:00:00', '2019-05-17 00:00:00', NULL, '崔佳', 76, NULL, NULL, '[]', '[]', '中国', '2019-05-01', '2018-11-22 13:54:04', '2019-06-10 11:27:23', NULL, '2019-05-11');

SET FOREIGN_KEY_CHECKS = 1;
