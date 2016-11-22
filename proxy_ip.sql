DROP TABLE IF EXISTS `proxy_ip`;
CREATE TABLE `proxy_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) NOT NULL,
  `port` char(5) NOT NULL,
  `http_type` varchar(5) DEFAULT NULL,
  `position` varchar(45) NOT NULL,
  `speed` double(4,3) NOT NULL,
  `connect_time` double(4,3) NOT NULL,
  `check_time` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;