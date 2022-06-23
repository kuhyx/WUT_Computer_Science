interval = [-5, 10];
rootBrackets = rootBracketing(@taskFunction, interval(1), interval(2));

% printGraph(@taskFunction, 'Newton', @newtonMethod, interval, rootBrackets, 'Approximate zeros of function for method of ');
printGraph(@polynomial, 'Newton', @newtonMethod, interval, rootBrackets, 'Approximate zeros of function for method of ');    

function y = taskFunction(x)
    y = -2.1 + 0.3*x - x*exp(1)^(-x);
end

function y = polynomial(x)
    y = -2 * x^4 + 12 * x^3 + 4* x^2 + 1 * x + 3;
end

function [zero, iterations] = newtonMethod(taskFunction, a, b, tolerance)
    [iterations, iteration, zero] = initialize(a, b);
    [zero, iterations] = newtonLoop(iterations, iteration, zero, a, b, tolerance, taskFunction);
end

function [iterations, step, zero] = initialize(a, b)
    iterations = double.empty(2, 0);
    step = sqrt(eps);
    zero = (a + b) / 2;
    iterations(:, size(iterations, 2) + 1) = [zero, taskFunction(zero)];
end

function [zero, iterations] = newtonLoop(iterations, iteration, zero, a, b, tolerance, taskFunction)
    while abs(taskFunction(zero)) > tolerance
        [zero, iterations] = insideLoop(taskFunction, zero, iteration, iterations, a, b);
    end
end

function [zero, iterations] = insideLoop(taskFunction, zero, iteration, iterations, a, b)
    [zero, iterations] = calculateZeroIterations(taskFunction, zero, iteration, iterations);
    checkForDivergence(zero, a, b);
end

function [zero, iterations] = calculateZeroIterations(taskFunction, zero, iteration, iterations)
    derivative = (taskFunction(zero + iteration) - taskFunction(zero - iteration)) / (2 * iteration);
    zero = zero - taskFunction(zero) / derivative;
    iterations(:, size(iterations, 2) + 1) = [zero, taskFunction(zero)];
end

function checkForDivergence(zero, a, b)
    if zero < a || zero > b
        error('Divergent iteration');
    end
end
