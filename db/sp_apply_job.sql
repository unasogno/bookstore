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
    
    END$$

DELIMITER ;