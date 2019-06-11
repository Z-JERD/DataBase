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

 Date: 11/06/2019 15:22:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pro_secondary_settle_task
-- ----------------------------
DROP TABLE IF EXISTS `pro_secondary_settle_task`;
CREATE TABLE `pro_secondary_settle_task`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务名称',
  `creator_id` bigint(20) NULL DEFAULT NULL COMMENT '任务创建人id',
  `amend` int(10) NOT NULL DEFAULT 0 COMMENT '该任务中的结算数据是否有更新 0:未更新 1:更新',
  `start_date` date NULL DEFAULT NULL COMMENT '结算开始日期',
  `end_date` date NULL DEFAULT NULL COMMENT '结算结束日期',
  `status` int(10) NULL DEFAULT 1 COMMENT '1 任务创建成功 2 等待确认 3 确认完成 4 结算完成',
  `settle_feedback` int(10) NULL DEFAULT 0 COMMENT '结算中心反馈结果 0:不通过 1 审核通过',
  `invalid` int(10) NOT NULL DEFAULT 0 COMMENT '标记删除 0：未删除 1：删除',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_modify` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最后修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '结算任务表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pro_secondary_settle_task
-- ----------------------------
INSERT INTO `pro_secondary_settle_task` VALUES (24, '测试', 1, 0, '2019-06-11', '2019-07-16', 2, 0, 0, '2019-06-10 13:55:26', '2019-06-10 16:06:58');

SET FOREIGN_KEY_CHECKS = 1;
