interval = [-5, 10];
rootBrackets = rootBracketing(@taskFunction, interval(1), interval(2));

printGraph(@taskFunction, 'False Position', @falsePosition, interval, rootBrackets, 'Approximate zeros of function for method of ');
    
function y = taskFunction(x)
    y = -2.1 + 0.3*x - x*exp(1)^(-x);
end

function [zero, iterations] = falsePosition(taskFunction, a, b, tolerance)

    [iterations, lastTwoA, lastTwoB, i] = initialize();
    [zero, iterations, a, b, lastTwoA, lastTwoB] = firstTwoIterations(a, b, taskFunction, iterations, lastTwoA, lastTwoB);
    [zero, iterations] = falsePositionLoop(taskFunction, zero, tolerance, lastTwoA, lastTwoB, i, a, b, iterations);
end

function [iterations, lastTwoA, lastTwoB, i] = initialize()
    iterations = double.empty(2, 0);
    lastTwoA = double.empty(2, 0);
    lastTwoB = double.empty(2, 0);
    i = 0;
end

function [zero, iterations, a, b, lastTwoA, lastTwoB] = firstTwoIterations(a, b, taskFunction, iterations, lastTwoA, lastTwoB)
    for j = 1 : 2
        zero = (a*taskFunction(b) - b * taskFunction(a)) / (taskFunction(b) - taskFunction(a));
        iterations(:, size(iterations, 2) + 1) = [zero, taskFunction(zero)];
        if sign(taskFunction(a)) ~= sign(taskFunction(zero))
            b = zero;
        else
            a = zero;
        end
        lastTwoA(j) = a;
        lastTwoB(j) = b;
    end
end

function [zero, iterations] = falsePositionLoop(taskFunction, zero, tolerance, lastTwoA, lastTwoB, i, a, b, iterations)
    while abs(taskFunction(zero)) > tolerance
        [lastTwoA, i, a, lastTwoB, b, tolerance, zero, iterations] = insideLoop(lastTwoA, i, a, lastTwoB, b, tolerance, taskFunction, iterations);
    end
end

function [lastTwoA, i, a, lastTwoB, b, tolerance, zero, iterations] = insideLoop(lastTwoA, i, a, lastTwoB, b, tolerance, taskFunction, iterations)
    [lastTwoA, lastTwoB] = changeLastTwoAB(lastTwoA, lastTwoB, i, a, b);
    zero = calculateZero(lastTwoB, tolerance, a, b, lastTwoA, taskFunction);
    iterations(:, size(iterations, 2) + 1) = [zero, taskFunction(zero)];
    [a, b] = newSubInterval(taskFunction, a, b, zero);
end

function [lastTwoA, lastTwoB] = changeLastTwoAB(lastTwoA, lastTwoB, i, a, b)
    lastTwoA(mod(i, 2) + 1) = a;
    lastTwoB(mod(i, 2) + 1) = b;
end

function [zero] = calculateZero(lastTwoB, tolerance, a, b, lastTwoA, taskFunction)
    if(abs(lastTwoB(1) - lastTwoB(2)) < tolerance) 
        zero = (a*(taskFunction(b) / 2) - b * taskFunction(a)) / (taskFunction(b) / 2 - taskFunction(a));
    elseif (abs(lastTwoA(1) - lastTwoA(2)) < tolerance) 
        zero = (a*taskFunction(b) - b * (taskFunction(a) / 2)) / (taskFunction(b) - (taskFunction(a) / 2));
    else
        zero = (a*taskFunction(b) - b * taskFunction(a)) / (taskFunction(b) - taskFunction(a));
    end
end

function [a, b] = newSubInterval(taskFunction, a, b, zero)
    if sign(taskFunction(a)) ~= sign(taskFunction(zero))
        b = zero;
    else        
        a = zero;
    end
end

