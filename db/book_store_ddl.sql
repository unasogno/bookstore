CREATE DATABASE IF NOT EXISTS bookstore 
	CHARACTER SET = gbk
	COLLATE = gbk_chinese_ci;

-- 1
CREATE TABLE IF NOT EXISTS customer
(
  customer_id INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  comments VARCHAR(200),
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY(customer_id)
) ENGINE = INNODB;

-- 2
CREATE TABLE IF NOT EXISTS publisher
(
  publisher_id INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `code` VARCHAR(10),
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY(publisher_id)
);

-- 3
CREATE TABLE IF NOT EXISTS supplier
(
  supplier_id INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL,
  address VARCHAR(200),
  phone_number VARCHAR(50),
  comments VARCHAR(200),
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY(supplier_id)
);

-- 4
CREATE TABLE IF NOT EXISTS book
(
  book_id INT NOT NULL AUTO_INCREMENT,
  publisher_id INT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `isbn` VARCHAR(20),
  `list_price` DECIMAL(10,2),
  publish_date DATE,
  class VARCHAR(10),
  sheet_numbers DECIMAL(10,3),
  folio INT(3),
  print_type INT(3),
  author VARCHAR(200),
  barcode VARCHAR(20),
  comments VARCHAR(200),
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY(book_id),
  FOREIGN KEY(publisher_id) REFERENCES publisher(publisher_id) 
);

-- 5
CREATE TABLE IF NOT EXISTS publisher_partner
(
  publisher_id INT NOT NULL,
  supplier_id INT NOT NULL,
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  FOREIGN KEY(publisher_id)  REFERENCES publisher(publisher_id),
  FOREIGN KEY(supplier_id)  REFERENCES supplier(supplier_id)
);

-- 6
CREATE TABLE IF NOT EXISTS supply
(
  supplier_id INT NOT NULL,
  book_id INT NOT NULL,
  discount DECIMAL(4,3) NOT NULL DEFAULT 1,
  inventory INT NOT NULL DEFAULT -1
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null
);

-- 7 
CREATE TABLE IF NOT EXISTS `order`
(
  order_id INT NOT NULL AUTO_INCREMENT,
  customer_id INT NOT NULL,
  `status` INT(3) NOT NULL,
  date_added DATETIME NOT NULL,
  date_shipped DATETIME,
  comments VARCHAR(200),
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY(order_id),
  FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
);

-- 8
CREATE TABLE IF NOT EXISTS order_item
(
  order_item_id INT NOT NULL AUTO_INCREMENT,
  order_id INT NOT NULL,
  book_id INT NOT NULL,
  discount DECIMAL(4,3),
  quantity INT(5),
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY(order_item_id),
  FOREIGN KEY(order_id) REFERENCES `order`(order_id),
  FOREIGN KEY(book_id) REFERENCES book(book_id)
);

-- 9
CREATE TABLE IF NOT EXISTS `code`
(
  `type` INT(3),
  `name` VARCHAR(50),
  `value` INT(3)
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null
);

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
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY (contact_id)
);

-- 11
CREATE TABLE IF NOT EXISTS partner_contact
(
  contact_id INT NOT NULL,
  partner_type INT(3) NOT NULL,
  partner_id INT(3) NOT NULL,
  comments VARCHAR(200),
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY (contact_id, partner_type, partner_id)
);

-- 12
CREATE TABLE IF NOT EXISTS `user`
(
  user_id INT NOT NULL AUTO_INCREMENT,
  user_name VARCHAR(20),
  surname varchar(20) not null,
  firstname varchar(20) not null,
  `password` VARCHAR(20) NOT NULL,
  email varchar(256),
  phone_number varchar(20),
  `status` int not null default 0,
  secret char(32) not null,
  token varchar(128),
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY (user_id)
) ENGINE = INNODB;

-- 13
CREATE TABLE IF NOT EXISTS book_tag
(
  tag_id INT NOT NULL AUTO_INCREMENT,
  book_id INT NOT NULL,
  tag_type INT(5) NOT NULL,
  tag VARCHAR(200) NOT NULL,
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  PRIMARY KEY (tag_id),
  FOREIGN KEY(book_id) REFERENCES book(book_id)
);

-- 14
create table IF NOT EXISTS book_index
(
  book_id int not null,
  doc_id int not null,
  date_created datetime not null,
  date_modified datetime not null,
  primary key(book_id, doc_id)
);

-- 15
create table IF NOT EXISTS high_water_mark
(
  entity_id int not null,
  app_id int not null,
  time_stamp timestamp default 0,
  date_created datetime not null,
  date_modified datetime not null,
  primary key(entity_id, app_id)
);

-- 16
create table IF NOT EXISTS `case`
(
  case_id int not null auto_increment,
  customer_id int not null,
  user_id int not null,
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  date_created datetime not null,
  date_modified datetime not null,
  primary key (case_id)
) engine = INNODB, character set = gbk;
