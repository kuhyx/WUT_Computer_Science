--Maciej Domanski 303853 - EDABA Lab 3
----------------------- INSERT TRIGGER -----------------------

-- Run before/after trigger
-- show club which budget was affected by inserting or deleting new/old player
select * from club where id = 1
-- show player who is inserted and by that affects club budget
select * from player where id = 1000000

-- Run to create trigger
-- after inserting a player increase club budget by player value
CREATE OR REPLACE trigger insert_player_trigger after insert on player
for each row
begin
    update club
    set budget = budget + :NEW.transfer_value
    where :NEW.club_id = id;
end;

-- Run to trigger trigger
-- insert
insert into player
values(1000000, 5, 'striker', 3, 'valid', 5, 35, 1000, 20000000, 1)

----------------------- UPDATE TRIGGER -----------------------

-- Run before/after trigger
-- show competition where prize was updated which later changes club reputation
select * from competition where id = 1
-- show club affected by update trigger when affected competition prize is high enough
select * from club where competition_id = 1

-- Run to create trigger
-- updates club reputation if the competition the club is taking part in has high enough prize value
CREATE OR REPLACE trigger update_trigger after update on competition
for each row
begin
    update club
    set reputation = 5
    where 200000 < :NEW.prize AND :NEW.id = competition_id;
end;

-- Run to trigger trigger
-- update
update competition
set prize = 1234567
where id = 1;


----------------------- DELETE TRIGGER -----------------------

-- Run before/after trigger
-- show club which budget was affected by inserting or deleting new/old player
select * from club where id = 1
-- select player who is deleted and by that affects club budget
select * from player where id = 1000000

-- Run to create trigger
-- after deleting a player decrease club budget by player value
CREATE OR REPLACE trigger delete_player_trigger after delete on player
for each row
begin
    update club
    set budget = budget - :OLD.transfer_value
    where :OLD.club_id = id;
end;

-- Run to trigger trigger
-- delete
delete from player
where id = 1000000

