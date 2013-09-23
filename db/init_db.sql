CREATE USER 'bookstore_admin'@'127.0.0.1' IDENTIFIED BY '1234';
-- GRANT ALL PRIVILEGES ON bookstore_stage.* TO 'bookstore_admin'@'127.0.0.1';
GRANT ALL PRIVILEGES ON bookstore.* TO 'bookstore_admin'@'127.0.0.1';
FLUSH PRIVILEGES;

CREATE USER 'bookstore_api'@'127.0.0.1' IDENTIFIED BY '1234';
GRANT INSERT, SELECT, UPDATE, DELETE, CREATE TEMPORARY TABLES, EXECUTE 
	ON bookstore.*
	TO 'bookstore_api'@'127.0.0.1';
FLUSH PRIVILEGES;

USE bookstore;

INSERT INTO CODE 
(`type`, `name`, `value`, date_added) 
VALUES 
(0, 'code type', 0, NOW()),
(0, 'book status', 1, NOW()),
(0, 'order status', 2, NOW()),
(0, 'order item status', 3, NOW()),
(0, 'user status', 4, NOW()),
(0, 'case status', 5, NOW()),
(0, 'tag type', 6, NOW()),
(1, 'available', 0, NOW()),
(1, 'out of stock', 1, NOW()),
(4, 'active', 0, NOW()),
(4, 'suspended', 1, NOW());
