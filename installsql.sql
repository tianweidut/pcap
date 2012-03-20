drop database dbPcap2;
create database dbPcap2;
use dbPcap2;
CREATE TABLE `text2` (
  `id` BIGINT(20)  NOT NULL AUTO_INCREMENT,
  `srcPort` VARCHAR(20)  DEFAULT NULL,
  `dstPort` VARCHAR(20)  DEFAULT NULL,
  `protocol` VARCHAR(10)  DEFAULT NULL,
  `dstIp` VARCHAR(50)  DEFAULT NULL,
  `srcIp` VARCHAR(50)  DEFAULT NULL,
  `data` LONGTEXT DEFAULT NULL,
  PRIMARY KEY (`id`)
);
