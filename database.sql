-- Adminer 4.1.0 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `anime`;
CREATE TABLE `anime` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` set('TV','Movie','Special','OVA','ONA') COLLATE utf8_unicode_ci NOT NULL,
  `ep_watched` smallint(5) unsigned DEFAULT NULL,
  `ep_total` smallint(5) unsigned DEFAULT NULL,
  `status` set('complete','on hold','dropped','watching','plan to watch') COLLATE utf8_unicode_ci NOT NULL,
  `date_started` date DEFAULT NULL,
  `date_finished` date DEFAULT NULL,
  `animedb_id` mediumint(8) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `animedb_id` (`animedb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DELIMITER ;;

CREATE TRIGGER `anime_bi` BEFORE INSERT ON `anime` FOR EACH ROW
BEGIN
    DECLARE x SMALLINT;
    SELECT ep_total INTO x FROM anime WHERE id = NEW.id;
    IF x != 0 AND NEW.ep_watched > x THEN
        SET NEW.ep_watched = x;
    END IF;
END;;

CREATE TRIGGER `anime_bu` BEFORE UPDATE ON `anime` FOR EACH ROW
BEGIN
    DECLARE x SMALLINT;
    SELECT ep_total INTO x FROM anime WHERE id = NEW.id;
    IF x != 0 AND NEW.ep_watched > x THEN
        SET NEW.ep_watched = x;
    END IF;
END;;

DELIMITER ;

DROP TABLE IF EXISTS `manga`;
CREATE TABLE `manga` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` set('Manga','One Shot','Novel') COLLATE utf8_unicode_ci NOT NULL,
  `ch_read` smallint(5) unsigned NOT NULL,
  `ch_total` smallint(5) unsigned NOT NULL,
  `vol_read` smallint(5) unsigned NOT NULL,
  `vol_total` smallint(5) unsigned NOT NULL,
  `status` set('complete','on hold','dropped','reading','plan to read') COLLATE utf8_unicode_ci NOT NULL,
  `date_started` date DEFAULT NULL,
  `date_finished` date DEFAULT NULL,
  `mangadb_id` mediumint(8) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mangadb_id` (`mangadb_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- 2014-06-19 05:28:53
