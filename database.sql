CREATE DATABASE audcon_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'audcon_dev'@'%' IDENTIFIED BY 'audcon_dev_123';
GRANT ALL PRIVILEGES ON audcon_dev.* To 'audcon_dev'@'%';
USE audcon_Dev;

CREATE TABLE `media` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `isdeleted` int(11) DEFAULT NULL,
  `media_file_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_fsize` bigint(20) NOT NULL,
  `media_format` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_streams_count` smallint(6) NOT NULL,
  `media_a_streams_count` smallint(6) NOT NULL,
  `media_v_streams_count` smallint(6) NOT NULL,
  `media_s_streams_count` smallint(6) NOT NULL,
  `media_o_streams_count` smallint(6) NOT NULL,
  `media_a_codec` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_a_sample_fmt` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_a_sample_rate` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_a_channels` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_a_channel_layout` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_a_bitrate` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_full_meta` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `isdeleted` int(11) DEFAULT NULL,
  `media_file_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_output_file_path` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_output_ffmpeg_params` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `media_converted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `run_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `isdeleted` int(11) DEFAULT NULL,
  `service` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `params` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
