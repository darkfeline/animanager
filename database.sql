-- Adminer 4.1.0 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';

CREATE DATABASE `anime` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `anime`;

DROP TABLE IF EXISTS `anime`;
CREATE TABLE `anime` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` set('TV','Movie','Special','OVA','ONA') COLLATE utf8_unicode_ci NOT NULL,
  `ep_total` smallint(5) unsigned DEFAULT NULL,
  `animedb_id` mediumint(8) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `animedb_id` (`animedb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP VIEW IF EXISTS `anime_full`;
CREATE TABLE `anime_full` (`id` int(10) unsigned, `name` varchar(255), `type` set('TV','Movie','Special','OVA','ONA'), `status` set('complete','on hold','dropped','watching','plan to watch'), `ep_watched` smallint(5) unsigned, `ep_total` smallint(5) unsigned, `date_started` date, `date_finished` date, `animedb_id` mediumint(8) unsigned);


DROP TABLE IF EXISTS `manga`;
CREATE TABLE `manga` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` set('Manga','One Shot','Novel') COLLATE utf8_unicode_ci NOT NULL,
  `ch_total` smallint(5) unsigned NOT NULL,
  `vol_total` smallint(5) unsigned NOT NULL,
  `mangadb_id` mediumint(8) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mangadb_id` (`mangadb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP VIEW IF EXISTS `manga_full`;
CREATE TABLE `manga_full` (`id` int(10) unsigned, `name` varchar(255), `type` set('Manga','One Shot','Novel'), `status` set('complete','on hold','dropped','reading','plan to read'), `ch_read` mediumint(8) unsigned, `ch_total` smallint(5) unsigned, `vol_read` mediumint(8) unsigned, `vol_total` smallint(5) unsigned, `date_started` date, `date_finished` date, `mangadb_id` mediumint(8) unsigned);


DROP TABLE IF EXISTS `myanime`;
CREATE TABLE `myanime` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ep_watched` smallint(5) unsigned NOT NULL DEFAULT '0',
  `status` set('complete','on hold','dropped','watching','plan to watch') COLLATE utf8_unicode_ci NOT NULL,
  `date_started` date DEFAULT NULL,
  `date_finished` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `myanime_ibfk_1` FOREIGN KEY (`id`) REFERENCES `anime` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `mymanga`;
CREATE TABLE `mymanga` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ch_read` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `vol_read` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `status` set('complete','on hold','dropped','reading','plan to read') COLLATE utf8_unicode_ci NOT NULL,
  `date_started` date DEFAULT NULL,
  `date_finished` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `mymanga_ibfk_1` FOREIGN KEY (`id`) REFERENCES `manga` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `anime_full`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `anime_full` AS select `anime`.`id` AS `id`,`anime`.`name` AS `name`,`anime`.`type` AS `type`,`myanime`.`status` AS `status`,`myanime`.`ep_watched` AS `ep_watched`,`anime`.`ep_total` AS `ep_total`,`myanime`.`date_started` AS `date_started`,`myanime`.`date_finished` AS `date_finished`,`anime`.`animedb_id` AS `animedb_id` from (`anime` left join `myanime` on((`myanime`.`id` = `anime`.`id`)));

DROP TABLE IF EXISTS `manga_full`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `manga_full` AS select `manga`.`id` AS `id`,`manga`.`name` AS `name`,`manga`.`type` AS `type`,`mymanga`.`status` AS `status`,`mymanga`.`ch_read` AS `ch_read`,`manga`.`ch_total` AS `ch_total`,`mymanga`.`vol_read` AS `vol_read`,`manga`.`vol_total` AS `vol_total`,`mymanga`.`date_started` AS `date_started`,`mymanga`.`date_finished` AS `date_finished`,`manga`.`mangadb_id` AS `mangadb_id` from (`manga` join `mymanga` on((`mymanga`.`id` = `manga`.`id`)));

-- 2014-05-06 05:13:34
