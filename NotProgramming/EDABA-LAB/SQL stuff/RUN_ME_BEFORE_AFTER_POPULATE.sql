-- RUN NEXT 3 LINES BEFORE RUNNING POPULATE SCRIPT
alter table manager
    DISABLE constraint manager_club_fk;

alter table club
    DISABLE constraint club_manager_fk;
alter table club
    DISABLE constraint club_competition_fk;
-- RUN 3 LINES BEFORE RUNNING POPULATE SCRIPT



-- RUN NEXT 3 LINES AFTER RUNNING POPULATE SCRIPT
alter table manager
    ENABLE constraint manager_club_fk;

alter table club
    ENABLE constraint club_manager_fk;
alter table club
    ENABLE constraint club_competition_fk;
-- RUN LAST 3 LINES AFTER RUNNING POPULATE SCRIPT