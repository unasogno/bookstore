use bookstore;

insert into code (`type`, name, `value`, date_added) 
values 
(0, 'code type', 0, NOW()),
(0, 'book status', 1, NOW()),
(0, 'order status', 2, NOW()),
(0, 'order item status', 3, NOW());