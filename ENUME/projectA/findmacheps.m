macheps = 1;
while 1.0 + macheps / 2 > 1.0
    macheps = macheps/2;
end

format long; 
disp("Display calculated macheps:")
disp(macheps)
disp("Display actual eps:")
disp(eps)
disp("Display 2^(-52)")
disp(2^(-52))
disp("Display difference between calculated macheps and actual eps:")
disp(macheps - eps)
disp("Display difference between 2^(-52) and actual eps:")
disp(2^(-52) - eps)
disp("Display difference between calculated macheps and 2^(-52):")
disp(macheps - 2^(-52))
