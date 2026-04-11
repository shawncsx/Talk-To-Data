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
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
