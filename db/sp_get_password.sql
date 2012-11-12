delimiter $$

use `bookstore`$$

drop procedure if exists `bookstore`.`sp_get_password`$$

create procedure `bookstore`.`sp_get_password`
(
  identity varchar(256),
  id_type tinyint
)
  begin
  
    if id_type = 1 then
      select password from `user` where email = identity;
    elseif id_type = 2 then
      select password from `user` where phone_number = identity;
    else
      SIGNAL SQLSTATE '45000'
        set MESSAGE_TEXT = 'identity type is not supported';
    end if;

  end$$

delimiter;
