-- Talk to Data SQL database schema
-- Created on: 2026-04-10

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS talktodata CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE talktodata;

-- Create data_sources table to store data source information
CREATE TABLE IF NOT EXISTS data_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('mysql', 'sqlite') NOT NULL,
    connection_string TEXT NOT NULL,
    -- MySQL specific fields
    mysql_host VARCHAR(255),
    mysql_port INT DEFAULT 3306,
    mysql_database VARCHAR(255),
    mysql_username VARCHAR(255),
    mysql_password VARCHAR(255),
    -- SQLite specific fields
    sqlite_path TEXT,
    -- Vector database path
    vector_db_path VARCHAR(255),
    -- Default data source flag
    is_default BOOLEAN DEFAULT FALSE,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create metadata_tables table to store table information for each data source
CREATE TABLE IF NOT EXISTS metadata_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_source_id INT NOT NULL,
    database_name VARCHAR(255),
    table_name VARCHAR(255) NOT NULL,
    table_description TEXT,
    table_ddl TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Foreign key to data_sources table
    FOREIGN KEY (data_source_id) REFERENCES data_sources(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `metadata_columns` (
  `id` int NOT NULL AUTO_INCREMENT,
  `table_id` int NOT NULL,
  `column_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data_type` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `column_description` text COLLATE utf8mb4_unicode_ci,
  `is_primary_key` tinyint(1) DEFAULT '0',
  `is_nullable` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `table_id` (`table_id`),
  CONSTRAINT `metadata_columns_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `metadata_tables` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci

