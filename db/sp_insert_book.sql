DROP PROCEDURE IF EXISTS `bookstore`.`sp_insert_book`;

DELIMITER $$

CREATE PROCEDURE `bookstore`.`sp_insert_book`(
    supplier VARCHAR(32),
    discount DECIMAL(5,2),
    publisher VARCHAR(32),
    `title` VARCHAR(200),
    `isbn` VARCHAR(20),
    `list_price` DECIMAL(10,2),
    publish_year SMALLINT,
    publish_month TINYINT,
    `edition` VARCHAR(32),
    class VARCHAR(10),
    sheet_numbers DECIMAL(10,3),
    folio INT(3),
    print_type VARCHAR(32),
    `size` SMALLINT,
    author VARCHAR(200),
    audience VARCHAR(32),
    phonetic VARCHAR(32)
)
    proc:BEGIN
    
    SET @book_id = (SELECT book_id FROM book WHERE  `book`.`isbn` = `isbn`);
    
    IF @book_id IS NOT NULL THEN
	SELECT 0, @book_id;
	LEAVE proc;
    END IF;
    
    SET @publisher_id = (SELECT `publisher_id` FROM publisher WHERE `name` = `publisher`);
    
    IF @publisher_id IS NULL THEN
	INSERT INTO publisher (`name`, date_added) VALUES (publisher, NOW());
	SET @publisher_id = LAST_INSERT_ID();
    END IF;
    
    INSERT INTO book 
	(`publisher_id`, `title`, `isbn`, `list_price`, 
	`publish_year`, `publish_month`, `class`, 
	`sheet_numbers`, `folio`, `print_type`, `author`, 
	date_added) 
	VALUES 
	(@publisher_id, `title`, `isbn`, `list_price`, 
	`publish_year`, `publish_month`, `class`, 
	`sheet_numbers`, `folio`, `print_type`, `author`,
	NOW());
    SET @book_id = LAST_INSERT_ID();
	
    SET @supplier_id = (
	SELECT `supplier_id` FROM supplier WHERE `name` = supplier);
    IF @supplier_id IS NULL THEN
	INSERT INTO supplier (`name`, date_added) VALUES (supplier, NOW());
	SET @supplier_id = LAST_INSERT_ID();
    END IF;
    
    INSERT INTO supply (supplier_id, book_id, discount, date_added) 
	VALUES (@supplier_id, @book_id, discount, NOW());

    INSERT INTO book_tag (book_id, tag_type, tag_name, tag_value, date_added) 
	VALUES (@book_id, 1, 'audience', audience, NOW());
    INSERT INTO book_tag (book_id, tag_type, tag_name, tag_value, date_added) 
	VALUES (@book_id, 1, 'phonetic', phonetic, NOW());
    
    SELECT 1, @book_id;
    END$$

DELIMITER ;