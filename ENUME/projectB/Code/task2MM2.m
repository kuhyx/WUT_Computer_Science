interval = [-5, 10];
rootBrackets = rootBracketing(@polynomial, interval(1), interval(2));

printGraph(@polynomial, 'MM2', @mm2, interval, rootBrackets, 'Approximate zeros of function for method of ');
    
printComplexGraph(@polynomial, 'MM2', @mm2, [-1 - i, 1 + i], 'Aproximate complex roots of polynomial');

% the polynomial function for task 2
function y = polynomial(x)
    y = -2 * x^4 + 12 * x^3 + 4* x^2 + 1 * x + 3;
end

% find roots of polynomial using MM2
function [approximation, iterations] = mm2(polynomial, a, b, tolerance)
    [approximation, iterations] = initialize(a, b, polynomial);
    [approximation, iterations] = mm2Loop(approximation, iterations, polynomial, tolerance);
end

function [approximation, iterations] = initialize(a, b, polynomial)
    approximation = (a + b) / 2;
    iterations = [approximation; polynomial(approximation)];
end

function [approximation, iterations] = mm2Loop(approximation, iterations, polynomial, tolerance)
    while abs(polynomial(approximation)) > tolerance
       [approximation, iterations] = insideLoop(approximation, polynomial, iterations);
    end
end

function [approximation, iterations] = insideLoop(approximation, polynomial, iterations)
        [a, b, c] = getABC(approximation, polynomial);
        [zPlus, zMinus] = findRoots(a, b, c);
        newApproximation = chooseNewApproximation(zPlus, zMinus, approximation);
        [approximation, iterations] = updateApproximations(newApproximation, iterations, polynomial);
end

function [a, b, c] = getABC(approximation, polynomial)
    c = polynomial(approximation);
    b = derivative(polynomial, approximation, 1);
    a = derivative(polynomial, approximation, 2) / 2;
end

function [zPlus, zMinus] = findRoots(a, b, c)
    zPlus = -2 * c / (b + sqrt(b ^ 2 - 4 * a * c));
    zMinus = -2 * c / (b - sqrt(b ^ 2 - 4 * a * c));
end

function newApproximation = chooseNewApproximation(zPlus, zMinus, approximation)
    if abs(zPlus) < abs(zMinus)
        newApproximation = approximation + zPlus;
    else
        newApproximation = approximation + zMinus;
    end
end

function [approximation, iterations] = updateApproximations(newApproximation, iterations, polynomial)
    approximation = newApproximation;
    iterations(:, size(iterations, 2) + 1) = [approximation, polynomial(approximation)];
end

% calculate the nth derivative of func at x
function y = derivative(function_, x, degree)
    if degree == 0
        y = function_(x);
        return
    end

    step = sqrt(eps);
    y = (derivative(function_, x + step, degree - 1) - derivative(function_, x - step, degree - 1)) / (2 * step);
end
