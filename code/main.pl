% month_days(Month, DaysInMonth, DaysBeforeMonth) 
% returns the number of days in Month and the number of days it takes to reach that date in year 2023
% prolog works by defining facts and rules and when queried about them returns values
% it works different from functional programming in this  aspect since it 
% doesn't just follow instruction it returns output based on world state
month_days('01', 31, 0).
month_days('02', 28, 31).
month_days('03', 31, 59).
month_days('04', 30, 90).
month_days('05', 31, 120).
month_days('06', 30, 151).
month_days('07', 31, 181).
month_days('08', 31, 212).
month_days('09', 30, 243).
month_days('10', 31, 273).
month_days('11', 30, 304).
month_days('12', 31, 334).

% day_of_year(Date, DayOfYear) converts a date to day of year number later used to calculate interval
% It also checks if number of days given by user is smaller or equal to number of days in the given month and if no then it gives fail
day_of_year(Date, DayOfYear) :-
  atom_chars(Date, Chars),
  append(DayChars, MonthChars, Chars),
  atom_chars(Day, DayChars),
  atom_chars(Month, MonthChars),
  month_days(Month, DaysInMonth, MonthDays),
  atom_number(Day, DayNumber),
  ((DayNumber =< DaysInMonth, DayNumber > 0) -> DayOfYear is MonthDays + DayNumber) ; fail.

% interval(Date1, Date2) prints the number of days between Date1 and Date2
% We always expect date to be in format ddmm where 'd' stands for day and 'm' stands for month
% if the month or day is just a single digit we expecte there to be zero in front 
% (like 0505 for 5th of may or 1105 for 11th of may or 0511 for 5th of november)
% write(Interval) prints out result, nl writes newline to make output conform to project requirements as much as possible
interval(Date1, Date2) :-
  (day_of_year(Date1, DayOfYear1), day_of_year(Date2, DayOfYear2) ->
    Interval is abs(DayOfYear2 - DayOfYear1),
    write(Interval), nl
  ;
    write('Invalid input.'), nl, fail
  ).