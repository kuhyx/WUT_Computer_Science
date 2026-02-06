-- Author: Krzysztof Rudnicki
-- Student number: 307585

--=======================insert_trigger=======================

-- show data
-- show competition which reputation was affected by attendance of the newly inserted match
select * from competition where id = 1
-- show match who is inserted and by that affects competition reputation
select * from match where id = 1234567

-- create trigger
-- set competition reputation equal to max (5) reputation if the match in this competition was attended by at least 10k people, and to 1 otherwise
CREATE OR REPLACE trigger match_insert_trigger after insert on match
for each row
begin
    update competition
    set reputation = 5
    where id = :NEW.competition_id AND :NEW.attendance > 10000;
    
    update competition
    set reputation = 1
    where id = :NEW.competition_id AND :NEW.attendance < 10000;
end;

-- trigger trigger
-- insert
-- sufficient (at least 10k attendance) to change competition reputation
insert into match
values(1234567, 10, 5, 30000, 'sunny', 90, To_date(TRUNC(DBMS_RANDOM.VALUE(TO_CHAR(DATE '1900-01-01','J') ,TO_CHAR(DATE '2023-12-31','J'))), 'J'), 'referre', 1)

-- insufficient (less than 10k attendance) to change competition reputation
insert into match
values(1234567, 10, 5, 3000, 'sunny', 90, To_date(TRUNC(DBMS_RANDOM.VALUE(TO_CHAR(DATE '1900-01-01','J') ,TO_CHAR(DATE '2023-12-31','J'))), 'J'), 'referre', 1)

delete from match where id = 1234567

--=======================update_trigger=======================

-- Run before/after trigger
-- show club affected by update trigger when manager reputation influences club reputation
select * from club where manager_id = 1
-- show manager which update influences club reputation
select * from manager where id = 1


-- Run to create trigger
-- updates club reputation if the competition the club is taking part in has high enough prize value
CREATE OR REPLACE trigger update_maanger_trigger after update on manager
for each row
begin
    update club
    set reputation = :NEW.reputation
    where id = :NEW.club_id;
end;

-- Run to trigger trigger
-- update
-- update manager reputation to 1 and trigger update for club to set reputation to 1
update manager
    set reputation = 1
where id = 1;

-- update manager reputation to 5 and trigger update for club to set reputation to 5
update manager
    set reputation = 5
where id = 1;



--=======================delete_trigger=======================

-- show data
-- show competition which reputation was affected by attendance of the newly inserted match
select * from competition where id = 1
-- show match who is inserted and by that affects competition reputation
select * from match where id = 1234567

-- create trigger
-- set competition reputation equal to min (1) reputation if the match deleted from competition was attended by at least 10k people, and to 5 otherwise
CREATE OR REPLACE trigger match_delete_trigger after delete on match
for each row
begin
    update competition
    set reputation = 1
    where id = :OLD.competition_id AND :OLD.attendance > 10000;
end;

-- trigger trigger
-- insert
-- sufficient (at least 10k attendance) to change competition reputation
insert into match
values(1234567, 10, 5, 30000, 'sunny', 90, To_date(TRUNC(DBMS_RANDOM.VALUE(TO_CHAR(DATE '1900-01-01','J') ,TO_CHAR(DATE '2023-12-31','J'))), 'J'), 'referre', 1)

delete from match where id = 1234567

