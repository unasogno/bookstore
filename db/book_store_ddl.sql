CREATE DATABASE IF NOT EXISTS bookstore 
	CHARACTER SET = utf8
	COLLATE = utf8_general_ci;

USE bookstore;

-- 1
CREATE TABLE IF NOT EXISTS customer
(
  customer_id INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  comments VARCHAR(200),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(customer_id)
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 2
CREATE TABLE IF NOT EXISTS publisher
(
  publisher_id INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `code` VARCHAR(10),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(publisher_id)
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 3
CREATE TABLE IF NOT EXISTS supplier
(
  supplier_id INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL,
  address VARCHAR(200),
  phone_number VARCHAR(50),
  comments VARCHAR(200),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(supplier_id)
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 4
CREATE TABLE IF NOT EXISTS book
(
  book_id INT NOT NULL AUTO_INCREMENT,
  publisher_id INT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `isbn` VARCHAR(20),
  `list_price` DECIMAL(10,2) NOT NULL,
  publish_year SMALLINT NOT NULL,
  publish_month TINYINT NOT NULL,
  `edition` VARCHAR(32),
  class VARCHAR(10),
  sheet_numbers DECIMAL(10,3),
  folio INT(3) NOT NULL,
  print_type INT(3) NOT NULL,
  `size` SMALLINT,
  author VARCHAR(200),
  barcode VARCHAR(20),
  comments VARCHAR(200),
  `status` INT NOT NULL DEFAULT 0,
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(book_id),
  FOREIGN KEY(publisher_id) REFERENCES publisher(publisher_id) ON DELETE CASCADE
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 5
CREATE TABLE IF NOT EXISTS publisher_partner
(
  publisher_id INT NOT NULL,
  supplier_id INT NOT NULL,
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY(publisher_id)  REFERENCES publisher(publisher_id) ON DELETE CASCADE,
  FOREIGN KEY(supplier_id)  REFERENCES supplier(supplier_id) ON DELETE CASCADE
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 6
CREATE TABLE IF NOT EXISTS supply
(
  supplier_id INT NOT NULL,
  book_id INT NOT NULL,
  discount DECIMAL(4,3) NOT NULL DEFAULT 1,
  inventory INT NOT NULL DEFAULT -1,
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 7 
CREATE TABLE IF NOT EXISTS `order`
(
  order_id INT NOT NULL AUTO_INCREMENT,
  customer_id INT NOT NULL,
  `status` INT(3) NOT NULL,
  date_purchased DATETIME NOT NULL,
  date_shipped DATETIME,
  comments VARCHAR(200),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(order_id),
  FOREIGN KEY(customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 8
CREATE TABLE IF NOT EXISTS order_item
(
  order_item_id INT NOT NULL AUTO_INCREMENT,
  order_id INT NOT NULL,
  book_id INT NOT NULL,
  discount DECIMAL(4,3),
  quantity INT(5),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(order_item_id),
  FOREIGN KEY(order_id) REFERENCES `order`(order_id) ON DELETE CASCADE,
  FOREIGN KEY(book_id) REFERENCES book(book_id) ON DELETE CASCADE
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 9
CREATE TABLE IF NOT EXISTS `code`
(
  `type` INT(3),
  `name` VARCHAR(100),
  `value` INT(3),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`type`, `value`)
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 10
CREATE TABLE IF NOT EXISTS contact
(
  contact_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  qq VARCHAR(20),
  phone VARCHAR(20),
  cell_phone VARCHAR(20),
  email VARCHAR(100),
  comments VARCHAR(200),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (contact_id)
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 11
CREATE TABLE IF NOT EXISTS partner_contact
(
  contact_id INT NOT NULL,
  partner_type INT(3) NOT NULL,
  partner_id INT(3) NOT NULL,
  comments VARCHAR(200),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (contact_id, partner_type, partner_id)
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 12
CREATE TABLE IF NOT EXISTS `user`
(
  user_id INT NOT NULL AUTO_INCREMENT,
  user_name VARCHAR(20),
  surname VARCHAR(20) NOT NULL,
  firstname VARCHAR(20) NOT NULL,
  `password` VARCHAR(20) NOT NULL,
  email VARCHAR(256),
  phone_number VARCHAR(20),
  `status` INT NOT NULL DEFAULT 0,
  secret CHAR(32) NOT NULL,
  token VARCHAR(128),
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id)
)  ENGINE = INNODB, CHARACTER SET = utf8;

-- 13
CREATE TABLE IF NOT EXISTS book_tag
(
  tag_id INT NOT NULL AUTO_INCREMENT,
  book_id INT NOT NULL,
  tag_type INT(5) NOT NULL,
  tag_name VARCHAR(50) NOT NULL,
  tag_value VARCHAR(200) NOT NULL,
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP 
  	DEFAULT CURRENT_TIMESTAMP 
	ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (tag_id),
  FOREIGN KEY(book_id) REFERENCES book(book_id) ON DELETE CASCADE
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 14
CREATE TABLE IF NOT EXISTS book_index
(
  book_id INT NOT NULL,
  doc_id INT NOT NULL,
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(book_id, doc_id)
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 15
CREATE TABLE IF NOT EXISTS high_water_mark
(
  entity_id INT NOT NULL,
  app_id INT NOT NULL,
  time_stamp TIMESTAMP DEFAULT 0,
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  
  PRIMARY KEY(entity_id, app_id)
) ENGINE = INNODB, CHARACTER SET = utf8;

-- 16
CREATE TABLE IF NOT EXISTS `case`
(
  case_id INT NOT NULL AUTO_INCREMENT,
  customer_id INT NOT NULL,
  user_id INT NOT NULL,
  `status` INT NOT NULL,
  date_added DATETIME NOT NULL,
  date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (case_id)
) ENGINE = INNODB, CHARACTER SET = utf8;