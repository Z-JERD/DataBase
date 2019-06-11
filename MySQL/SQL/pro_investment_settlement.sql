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

 Date: 11/06/2019 15:09:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pro_investment_settlement
-- ----------------------------
DROP TABLE IF EXISTS `pro_investment_settlement`;
CREATE TABLE `pro_investment_settlement`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '结算数据自增ID',
  `pid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '投资项目编号',
  `invest_way` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '投资方式',
  `invest_amount` decimal(20, 2) NOT NULL COMMENT '投资金额',
  `huaxia_charge` int(11) NULL DEFAULT NULL COMMENT '华夏结算发行款 1:是，0:否',
  `deduction_first` int(11) NULL DEFAULT NULL COMMENT '先行抵扣 1:是，0:否',
  `invest_status` int(11) NULL DEFAULT 1 COMMENT '结算状态：1未开启，2开始结算',
  `settlement_date` json NULL COMMENT '结算日期',
  `settlement_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '结算日期相关合同摘要',
  `contract_text` json NULL COMMENT '其他合同相关摘要[{\"title\":\"\",\"content\":\"\"},......]',
  `contract` json NULL COMMENT '合同相关附件[{type\": \"pdf\",\"doc_type\":6,\"doc_names\":\"6bdjldhmv0.pdf\",\"origin_name\":\"华夏授权书.pdf\",\"catalog\": \"prjdoc\",\"thumbs\":[...]}...]',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '投资项目结算表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pro_investment_settlement
-- ----------------------------
INSERT INTO `pro_investment_settlement` VALUES (1, 'GT2017007', '风险投资', 60000.00, 1, 1, 2, '[\"2018-07-18\", \"2019-07-18\", \"2020-07-18\", \"2019-06-02\"]', '风险投资妖猫传', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容...\"}]', '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}, {\"type\": \"image\", \"thumbs\": [\"ehskqm5r3cdev0.png\"], \"catalog\": \"prjdoc\", \"doc_name\": \"ehskqm5r3cdev0.png\", \"doc_type\": 8, \"origin_name\": \"bg.png\"}]', '2019-04-19 15:08:30');
INSERT INTO `pro_investment_settlement` VALUES (3, 'GT2017007', '固定投资', 16000.00, 1, 0, 1, '[\"2018-12-20\", \"2019-2-20\", \"2019-5-20\"]', '每季度付一次款', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容\"}]', '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}]', '2019-04-19 15:08:30');
INSERT INTO `pro_investment_settlement` VALUES (5, 'GT20190321', '固定收益', 100.00, 0, 1, 2, '[\"2018-07-01\", \"2019-07-02\", \"2020-07-03\", \"2019-07-04\", \"2019-07-05\", \"2019-07-06\"]', '阿萨德阿萨达实打实大事大事大事 ', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容...\"}, {\"title\": \"阿萨达手打手打\", \"content\": \"阿萨德阿萨德阿萨德阿萨德\"}]', '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}, {\"type\": \"image\", \"thumbs\": [\"5k909c5rrpdev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"5k909c5rrpdev0.jpeg\", \"doc_type\": 8, \"origin_name\": \"timg.jpg\"}]', '2019-04-19 15:08:30');
INSERT INTO `pro_investment_settlement` VALUES (14, 'GT2018056', '风险投资', 50000.00, 1, 1, 1, '[\"2018-07-18\", \"2019-07-18\", \"2020-07-18\"]', '方式为风险投资', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容...\"}]', '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}, {\"type\": \"image\", \"thumbs\": [\"1ky6dy0hwqdev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"1ky6dy0hwqdev0.jpeg\", \"doc_type\": 8, \"origin_name\": \"timg (2).jpg\"}]', '2019-05-22 13:57:52');
INSERT INTO `pro_investment_settlement` VALUES (15, 'GT2018056', '保底分红', 60000.00, 0, 0, 1, '[\"2018-07-18\", \"2019-07-18\", \"2020-07-18\"]', '分账比', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容...\"}]', '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}]', '2019-05-22 13:57:52');
INSERT INTO `pro_investment_settlement` VALUES (16, 'GT2017007', '保底分红', 80000.00, 0, 0, 1, '[\"2018-07-18\", \"2019-07-18\", \"2020-07-18\"]', '分账比妖猫传', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容...\"}]', '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}]', '2019-05-22 14:03:20');
INSERT INTO `pro_investment_settlement` VALUES (21, 'GT20190315', '风险投资', 10000.00, 1, 1, 2, '[\"2018-07-18\", \"2019-07-18\", \"2020-07-18\"]', '投资流浪地球', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容...\"}, {\"title\": \"合同条款第二项\", \"content\": \"阿萨德阿萨德阿萨德\"}]', '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}]', '2019-05-22 14:44:32');
INSERT INTO `pro_investment_settlement` VALUES (22, 'GT20190315', '保底分红', 80000.00, 0, 0, 2, '[\"2018-07-18\", \"2019-07-18\", \"2020-07-18\"]', '分账比妖猫传', '[{\"title\": \"合同条款第一项\", \"content\": \"第一项内容...\"}]', '[{\"type\": \"pdf\", \"thumbs\": [\"harw7vxe8dev0.jpeg\"], \"catalog\": \"prjdoc\", \"doc_name\": \"6bdjldhmiydev0.pdf\", \"doc_type\": \"4\", \"origin_name\": \"《西虹市首富》给华夏授权书.pdf\"}]', '2019-05-22 14:44:32');
INSERT INTO `pro_investment_settlement` VALUES (23, 'GT20190315', '固定收益', 80000.00, 1, 1, 1, '[\"2019-06-06\", \"2019-06-23\"]', 'qerqweqweqw', '[{\"title\": \"请问请问群翁qw\", \"content\": \"驱蚊器翁\"}]', '[]', '2019-06-04 16:00:05');
INSERT INTO `pro_investment_settlement` VALUES (24, 'GT20190321', '保本分红', 0.00, 1, 1, 1, '[\"2019-06-01\", \"2019-06-02\"]', '安慰我', '[{\"title\": \"为w\", \"content\": \"为为\"}]', '[{\"type\": \"image\", \"thumbs\": [\"ej1q5sa1fmdev0.png\"], \"catalog\": \"prjdoc\", \"doc_name\": \"ej1q5sa1fmdev0.png\", \"doc_type\": 8, \"origin_name\": \"bg.png\"}]', '2019-06-05 14:02:29');
INSERT INTO `pro_investment_settlement` VALUES (25, 'GT20190321', '风险投资', 0.00, NULL, NULL, 1, '[\"\"]', '', '[]', '[]', '2019-06-05 14:03:16');

SET FOREIGN_KEY_CHECKS = 1;
