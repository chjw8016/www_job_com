SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for jobs
-- ----------------------------
DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `position_id` varchar(255) DEFAULT '',
  `position_name` varchar(255) DEFAULT '',
  `position_lables` varchar(255) DEFAULT '',
  `work_year` varchar(255) DEFAULT '',
  `salary` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT '',
  `education` varchar(255) DEFAULT '',
  `company_name` varchar(255) DEFAULT '',
  `industry_field` varchar(255) DEFAULT '',
  `finance_stage` varchar(255) DEFAULT '',
  `company_size` varchar(255) DEFAULT '',
  `updated_at` varchar(255) DEFAULT '',
  `time` varchar(255) DEFAULT '',
  `platform` varchar(255) DEFAULT '',
  `avg_salary` float(6,3) DEFAULT '0.000',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9623 DEFAULT CHARSET=utf8;
