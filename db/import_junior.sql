CREATE TABLE IF NOT EXISTS stage
(
  sn INT NOT NULL,
  isbn VARCHAR(30) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `number` INT(3),
  `list_price` DECIMAL(10,2),
  `publisher` VARCHAR(50),
  `publish_date` VARCHAR(20),
  `class` VARCHAR(10),
  `sheet_numbers` DECIMAL(10,3),
  `audience` VARCHAR(100),
  `discount` DECIMAL(4,3),
  `print_type` VARCHAR(10),
  `folio` INT(3),
  `author` VARCHAR(100),
  `provider` VARCHAR(100),
  `series` VARCHAR(100),
  `paper` VARCHAR(100),
  `sales_discount` DECIMAL(4,3),
  `sheet_price` DECIMAL(10,2)
);

LOAD DATA LOCAL INFILE 'D:\\Tmp\\junior.csv'
	INTO TABLE stage
	CHARACTER SET gbk
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	IGNORE 1 LINES;

SELECT * FROM stage LIMIT 10;
SELECT * FROM publisher;
SELECT * FROM supplier;
SELECT * FROM publisher_partner;
SELECT * FROM `code`;

/* 
  code: 
  print type = 1
  tag type = 2
*/
-- insert print type ()
INSERT INTO `code` (`type`, `name`, `value` )
	SELECT 1, `name`, @`row` := @`row` + 1 AS `row`
		FROM (SELECT @`row` := 0) r, 
		     (SELECT DISTINCT print_type AS `name` FROM stage ORDER BY `print_type`) c;
		     
-- insert tag type
INSERT INTO `code` (`type`, `name`, `value`) VALUES (2, N'受众', 1);


/* publisher */
INSERT INTO publisher (`name`) SELECT DISTINCT publisher FROM stage;

/* supplier */
INSERT INTO supplier (`name`) SELECT DISTINCT provider FROM stage;

/* book */
-- trim spaces
UPDATE stage SET publish_date = TRIM(publish_date);

-- 把yyyy.m替换成 yyyy-m
UPDATE stage SET publish_date = REPLACE(publish_date, '.', '-');

-- 把yyyy年, yyyy年m月, yyyy年m月d号, yyyy年m月d日格式的汉字替换成 -
UPDATE stage SET publish_date = REPLACE(publish_date, N'年', N'-');
UPDATE stage SET publish_date = REPLACE(publish_date, N'月', N'-');
UPDATE stage SET publish_date = REPLACE(publish_date, N'日', N'');
UPDATE stage SET publish_date = REPLACE(publish_date, N'号', N'');

-- 去掉多余的-
-- select * from stage where publish_date like '%-';
UPDATE stage 
	SET publish_date = LEFT(publish_date, LENGTH(publish_date) - 1) 
	WHERE publish_date LIKE '%-';

-- 格式为yyyy-m的串在后面加入-d
/*
SELECT  sn, `name`, publish_date, concat(publish_date, '-1'),
	locate('-', publish_date) as `first`, 
	locate('-', publish_date, LOCATE('-', publish_date) + 1) as `second` 
	FROM stage
	where LOCATE('-', publish_date, LOCATE('-', publish_date) + 1) = 0
	and LOCATE('-', publish_date) = 5;
*/

UPDATE stage SET publish_date = CONCAT(publish_date, '-1')
	WHERE LOCATE('-', publish_date, LOCATE('-', publish_date) + 1) = 0
	AND LOCATE('-', publish_date) = 5;

-- 格式为m-d-yyyy的串调整为yyyy-m-d
/*
SELECT  `name`, publish_date, 
	concat(
		right(publish_date, length(publish_date) - LOCATE('-', publish_date, LOCATE('-', publish_date) + 1)), 
		'-', 
		left(publish_date, LOCATE('-', publish_date, LOCATE('-', publish_date) + 1) - 1)
	) as normalzied,
	LOCATE('-', publish_date) AS `first`, 
	LOCATE('-', publish_date, LOCATE('-', publish_date) + 1) AS `second` 
	FROM stage
	WHERE LOCATE('-', publish_date, LOCATE('-', publish_date) + 1) > 0
	AND LOCATE('-', publish_date) <= 3;
*/

UPDATE stage SET publish_date =
	CONCAT(
		RIGHT(publish_date, LENGTH(publish_date) - LOCATE('-', publish_date, LOCATE('-', publish_date) + 1)), 
		'-', 
		LEFT(publish_date, LOCATE('-', publish_date, LOCATE('-', publish_date) + 1) - 1)
	)
	WHERE LOCATE('-', publish_date, LOCATE('-', publish_date) + 1) > 0
	AND LOCATE('-', publish_date) <= 3;

-- insert book
INSERT INTO book 
		(publisher_id, title, isbn, list_price, publish_date, 
		class, sheet_numbers, folio, print_type, author, comments)
	SELECT 
		p.publisher_id, s.name, s.isbn, s.list_price, DATE(publish_date), 
		LEFT(class, 1), sheet_numbers, folio, pt.`value` print_type, author, sn
	FROM stage s
	INNER JOIN publisher p
		ON s.publisher = p.name
	INNER JOIN (SELECT `name`, `value` FROM `code` WHERE `type` = 1) pt
		ON s.print_type = pt.name;

-- supply
INSERT INTO supply
	(supplier_id, book_id, discount, inventory)
	SELECT sp.supplier_id, b.book_id, st.discount, -1
		FROM stage st
		INNER JOIN supplier sp
			ON st.provider = sp.name
		INNER JOIN book b
			ON st.sn = b.comments;

