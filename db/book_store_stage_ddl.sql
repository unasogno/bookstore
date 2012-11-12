
CREATE DATABASE IF NOT EXISTS bookstore_stage 
	CHARACTER SET = gbk
	COLLATE = gbk_chinese_ci;

USE bookstore_stage;

-- 1
CREATE TABLE IF NOT EXISTS job
(
    job_id INT NOT NULL AUTO_INCREMENT,
    date_added DATETIME NOT NULL,
    date_modified 
        TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id)
) ENGINE = INNODB, CHARACTER SET = GBK;

-- 2
CREATE TABLE IF NOT EXISTS raw_book
(
    book_id INT NOT NULL AUTO_INCREMENT,
    job_id INT NOT NULL,
    publisher VARCHAR(200),
    `title` VARCHAR(200),
    `isbn` VARCHAR(20),
    `list_price` VARCHAR(20),
    publish_date VARCHAR(20),
    class VARCHAR(10),
    sheet_numbers VARCHAR(10),
    folio VARCHAR(10),
    print_type VARCHAR(10),
    author VARCHAR(200),
    barcode VARCHAR(20),
    comments VARCHAR(200),
    publisher_id INT,
    PRIMARY KEY(book_id)
) ENGINE = INNODB, CHARACTER SET = GBK;

-- 3
CREATE TABLE IF NOT EXISTS raw_tag
(
    tag_id INT NOT NULL AUTO_INCREMENT,
    job_id INT NOT NULL,
    book_id INT NOT NULL,
    tag_name VARCHAR(200) NOT NULL,
    tag_value VARCHAR(200) NOT NULL,
    PRIMARY KEY (tag_id)
) ENGINE = INNODB, CHARACTER SET = GBK;

-- 4
CREATE TABLE IF NOT EXISTS raw_code
(
    `job_id` INT NOT NULL,
    `type` INT(3),
    `name` VARCHAR(100),
    `value` INT(3),
    date_added DATETIME NOT NULL,
    date_modified TIMESTAMP 
        DEFAULT CURRENT_TIMESTAMP 
		  ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`type`, `value`)
) ENGINE = INNODB, CHARACTER SET = GBK;

-- 5
CREATE TABLE IF NOT EXISTS raw_publisher
(
    publisher_id INT NOT NULL AUTO_INCREMENT,
    job_id INT NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    date_added datetime NOT NULL,
    date_modified TIMESTAMP 
	     DEFAULT CURRENT_TIMESTAMP 
	     ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(publisher_id)
) ENGINE = INNODB, CHARACTER SET = GBK;