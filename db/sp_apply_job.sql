DELIMITER $$

DROP PROCEDURE IF EXISTS `bookstore_stage`.`sp_apply_job`$$

CREATE PROCEDURE `bookstore_stage`.`sp_apply_job`(
    job_id INT
)
    BEGIN
    
    INSERT INTO `bookstore`.`code` (`type`, `name`, `value`)
    SELECT `type`, `name`, `value`
    FROM `bookstore_stage`.raw_code rc
    WHERE rc.job_id = job_id;

    INSERT INTO `bookstore`.publisher (publisher_id, `name`, date_added)
    SELECT publisher_id, `name`, NOW()
    FROM raw_publisher rp
    WHERE rp.job_id = job_id;
    
    INSERT INTO `bookstore`.book 
    (book_id, title, publisher_id, isbn, class, author)
    SELECT book_id, title, publisher_id, isbn, class, author
    FROM raw_book rb
    WHERE rb.job_id = job_id;
    
    INSERT INTO `bookstore`.book_tag
    (book_id, tag_type, tag_name, tag_value, date_added)
    SELECT book_id, 1, tag_name, tag_value, NOW()
    FROM raw_tag rt
    WHERE rt.job_id = job_id;
    
    END$$

DELIMITER ;