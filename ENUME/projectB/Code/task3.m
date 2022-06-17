interval = [-5, 10];
rootBrackets = rootBracketing(@polynomial, interval(1), interval(2));

printGraph(@polynomial, 'Laguerre', @laguerre, interval, rootBrackets, 'Approximate zeros of function for method of ');
     
printComplexGraph(@polynomial, 'Laguerre', @laguerre, [-1 - i, 1 + i], 'Aproximate complex roots of polynomial');

function y = polynomial(x)
    y = -2 * x^4 + 12 * x^3 + 4* x^2 + 1 * x + 3;
end

function [zero, iterations] = laguerre(polynomial, a, b, tolerance)
    [degree, zero, iterations] = initialize(a, b, polynomial);
    [zero, iterations] = laguerreLoop(polynomial, zero, tolerance, iterations, degree);

end

function [degree, zero, iterations] = initialize(a, b, polynomial)
    degree = 4;
    zero = (a + b) / 2;
    iterations = [zero; polynomial(zero)];
end

function [zero, iterations] = laguerreLoop(polynomial, zero, tolerance, iterations, degree)
    while abs(polynomial(zero)) > tolerance
        [iterations, zero] = insideLoop(polynomial, zero, degree, iterations);
    end
end

function [iterations, zero] = insideLoop(polynomial, zero, degree, iterations)
    [derrivative0, derrivative1, derrivative2] = calculateDerrivatives(polynomial, zero);
    [zPlus, zMinus] = calculateZ(degree, derrivative0, derrivative1, derrivative2);
    newZero = chooseNewZero(zPlus, zMinus, zero);
    [zero, iterations] = updateZeros(newZero, iterations, polynomial);
end

function [derrivative0, derrivative1, derrivative2] = calculateDerrivatives(polynomial, zero)
    derrivative0 = polynomial(zero);
    derrivative1 = derivative(polynomial, zero, 1);
    derrivative2 = derivative(polynomial, zero, 2);
end

function [zPlus, zMinus] = calculateZ(degree, derrivative0, derrivative1, derrivative2)
    expressionUnderSquareRoot = (degree - 1) * ((degree - 1) * derrivative1 ^ 2 - degree * derrivative0 * derrivative2);
    lagsqrt = sqrt(expressionUnderSquareRoot);

    zPlus = degree * derrivative0 / (derrivative1 + lagsqrt);
    zMinus = degree * derrivative0 / (derrivative1 - lagsqrt);
end

function newZero = chooseNewZero(zPlus, zMinus, zero)    
    if abs(zPlus) < abs(zMinus)
        newZero = zero - zPlus;
    else
        newZero = zero - zMinus;
    end
end

function [zero, iterations] = updateZeros(newZero, iterations, polynomial)
    zero = newZero;
    iterations(:, size(iterations, 2) + 1) = [zero, polynomial(zero)];
end

function y = derivative(function_, x, degree)
    if degree == 0
        y = function_(x);
        return
    end

    step = sqrt(eps);
    y = (derivative(function_, x + step, degree - 1) - derivative(function_, x - step, degree - 1)) / (2 * step);
end
