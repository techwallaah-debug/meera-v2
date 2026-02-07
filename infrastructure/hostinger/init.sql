-- Initial database setup script
-- This runs automatically when MySQL container starts for the first time

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS social_commerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE social_commerce;

-- Set timezone
SET time_zone = '+05:30';

-- Create indexes for performance (will be created by services, but can pre-create here)
-- The actual tables will be created by SQLAlchemy models

-- Grant permissions
-- GRANT ALL PRIVILEGES ON social_commerce.* TO 'admin'@'%';
-- FLUSH PRIVILEGES;
