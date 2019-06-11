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

 Date: 11/06/2019 15:09:39
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pro_investment_project
-- ----------------------------
DROP TABLE IF EXISTS `pro_investment_project`;
CREATE TABLE `pro_investment_project`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '二级市场子项目自增ID',
  `pid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '要显示的项目编号',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目名称',
  `movie_project_id` bigint(20) NULL DEFAULT NULL COMMENT '关联的发行项目id 或 影片项目',
  `authorize_start_time` datetime(0) NULL DEFAULT NULL COMMENT '项目授权开始时间',
  `authorize_end_time` datetime(0) NULL DEFAULT NULL COMMENT '项目授权结束时间',
  `settlement_producer` json NULL COMMENT '片方结算数据：json格式：{\"settlement_object\":[{\"bank\":\"招商银行天津新港支行\",\"index\":\"1\",\"remark\":\"\",\"object_name\":\"结算对象一\",\"account_name\":\"华策影业（天津）有限公司\",\"bank_account\":\"122905052810601\"}],huaxia_rate:3000,settelment_time:\"每半年进行一次结算\"}',
  `settlement_investment` json NULL COMMENT '投资结算：json格式：{\"invest_amount\":10000000,\"invest_way\":\" 固定收益......\",\"huaxia_charge\":1,\"deduction_first\":1}',
  `duty_person` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '项目认领人(客户经理)姓名',
  `duty_person_id` int(11) NULL DEFAULT NULL COMMENT '项目认领人(客户经理account_manager)用户ID',
  `contract_bak` json NULL COMMENT '合同数据[{doc_type:6,doc_names:,doc_id,origin_name},,,,,]',
  `contract_text_bak` json NULL COMMENT '[{\"title\":\"\",\"content\":\"\"},......]',
  `permits` json NULL COMMENT '许可证[{doc_type:6,doc_names:,doc_id,origin_name},,,,,]',
  `origin` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '国别',
  `invest_status_bak` int(11) NULL DEFAULT 1 COMMENT '结算状态：1未开启，2开始结算',
  `release_date` date NULL DEFAULT NULL COMMENT '上映时间',
  `settlement_date_bak` date NULL DEFAULT NULL COMMENT '结算日期',
  `create_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modify` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最后修改时间，请勿修改',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 39 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '二级市场项目表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pro_investment_project
-- ----------------------------
INSERT INTO `pro_investment_project` VALUES (20, 'GT2017007', '妖猫传', 1528266103836, NULL, NULL, NULL, '{\"invest_way\": \"风险投资\", \"huaxia_charge\": 0, \"invest_amount\": \"8000\", \"deduction_first\": 0}', '邵建华', 7015, '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}]', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容。。。。。。\"}]', '[{\"doc_type\": 6, \"doc_names\": \"xxx\"}]', '国产', 2, '2018-10-05', '2018-12-20', '2018-12-06 15:40:56', '2019-06-05 14:14:23');
INSERT INTO `pro_investment_project` VALUES (21, 'GT2018056', '新乌龙院之笑傲江湖', 152782126472512, '2018-09-30 00:00:00', '2019-03-28 00:00:00', NULL, '{\"invest_way\": \"风险投资\", \"huaxia_charge\": 1, \"invest_amount\": 0, \"deduction_first\": 0}', '刘西南', 14, '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}]', '[{\"title\": \"合同标题1\", \"content\": \"合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1合同内容1\"}]', NULL, '中国', 1, '2018-10-05', '2018-12-01', '2018-12-24 18:32:24', '2019-06-05 11:57:10');
INSERT INTO `pro_investment_project` VALUES (22, 'GT20190315', '流浪地球', 1489385164415, NULL, NULL, NULL, NULL, '李四', 345689, '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}]', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容。。。。。。\"}]', '[{\"doc_type\": 6, \"doc_names\": \"xxx\"}]', '中国', 1, '2018-10-05', NULL, '2019-03-15 13:43:35', '2019-06-04 15:45:11');
INSERT INTO `pro_investment_project` VALUES (38, 'GT20190321', '大人物', 1489385193575, NULL, NULL, NULL, NULL, '堇年', 115200, NULL, NULL, NULL, NULL, 1, '2018-10-18', NULL, '2019-03-21 14:29:44', '2019-06-05 14:10:10');

SET FOREIGN_KEY_CHECKS = 1;
