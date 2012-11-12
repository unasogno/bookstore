CREATE USER 'bookstore_admin'@'127.0.0.1' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON bookstore_stage.* TO 'bookstore_admin'@'127.0.0.1';
GRANT ALL PRIVILEGES ON bookstore.* TO 'bookstore_admin'@'127.0.0.1';
FLUSH PRIVILEGES;

CREATE USER 'bookstore_api'@'127.0.0.1' IDENTIFIED BY '1234';
GRANT INSERT, SELECT, UPDATE, DELETE, CREATE TEMPORARY TABLES, EXECUTE 
	ON bookstore.*
	TO 'bookstore_api'@'127.0.0.1';
FLUSH PRIVILEGES;

use bookstore;

insert into code 
(`type`, name, `value`, date_added) 
values 
(0, 'code type', 0, NOW()),
(0, 'book status', 1, NOW()),
(0, 'order status', 2, NOW()),
(0, 'order item status', 3, NOW()),
(0, 'user status', 4, NOW()),
(0, 'case status', 5, NOW()),
(0, 'tag type', 6, NOW()),
(0, 'folio', 7, NOW()),
(0, 'print type', 8, NOW());
