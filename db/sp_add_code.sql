DELIMITER $$

DROP PROCEDURE IF EXISTS `bookstore_stage`.`sp_add_code`$$

CREATE PROCEDURE `bookstore_stage`.`sp_add_code`(
    job_id INT,    
    `type` INT,
    `name` VARCHAR(100)
)
    BEGIN
    SET @code_count = 
	(
        SELECT COUNT(1)
        FROM `raw_code` c
        WHERE c.`name` = `name`
    );
	 
    IF @code_count = 0 THEN
        SET @max_id = 
	    (
            SELECT MAX(`VALUE`) 
            FROM `raw_code` c
            WHERE c.`type` = `type`
        );
        
        INSERT INTO `raw_code` 
        (job_id, `type`, `name`, `value`, date_added) 
        VALUES 
        (job_id, `type`, `name`, IFNULL(@max_id, 0) + 1, NOW());
        
	END IF;
	
    SELECT `type`, `name`, `value`
	FROM `raw_code` c
	WHERE c.`type` = `type`
	AND c.`name` = `name`;
	 
    END$$

DELIMITER ;