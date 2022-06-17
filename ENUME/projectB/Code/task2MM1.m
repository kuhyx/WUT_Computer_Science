interval = [-5, 10];
rootBrackets = rootBracketing(@polynomial, interval(1), interval(2));

printGraph(@polynomial, 'MM1', @mm1, interval, rootBrackets, 'Approximate zeros of function for method of ');
     
printComplexGraph(@polynomial, 'MM1', @mm1, [-1 - i, 1 + i], 'Aproximate complex roots of polynomial');

function y = polynomial(x)
    y = -2 * x^4 + 12 * x^3 + 4* x^2 + 1 * x + 3;
end

function [approximation, iterations] = mm1(polynomial, a, b, tolerance)
    [approximation, approximationValue, iterations] = initialize(a, b, polynomial);
    [approximation, iterations] = mm1Loop(approximation, tolerance, approximationValue, iterations, polynomial);
end

function [approximation, approximationValue, iterations] = initialize(a, b, polynomial)
    approximation = [a, b, (a + b) / 2];
    approximationValue = arrayfun(polynomial, approximation);
    iterations = [approximation(3); polynomial(approximation(3))];
end

function [approximation, iterations] = mm1Loop(approximation, tolerance, approximationValue, iterations, polynomial)
    while abs(polynomial(approximation(3))) > tolerance
        [approximation, approximationValue, iterations] = insideLoop(approximation, approximationValue, polynomial, iterations);
    end
end

function [approximation, approximationValue, iterations] = insideLoop(approximation, approximationValue, polynomial, iterations)
    equationsSystem = createEquationSystem(approximation, approximationValue);
    [zPlus, zMinus] = rootsOfQuadraticFormula(equationsSystem, approximationValue);
    [approximation, approximationValue, iterations] = updateApproximations(zPlus, zMinus, approximation, iterations, polynomial);
end

function equationsSystem = createEquationSystem(approximation, approximationValue)
    [z0, z1, difference0, difference1] = initializeEquationSystem(approximation, approximationValue);
    equationsSystem = solveEquationSystem(z0, difference0, z1, difference1);
end

function [zPlus, zMinus] = rootsOfQuadraticFormula(equationsSystem, approximationValue)
    [a, b, c] = createApproximatedQuadraticFormula(equationsSystem, approximationValue);
    [zPlus, zMinus] = findRootsOfQuadraticFormula(a, b, c);
end

function [approximation, approximationValue, iterations] = updateApproximations(zPlus, zMinus, approximation, iterations, polynomial)
    newApproximation = chooseNewRoot(zPlus, zMinus, approximation);
    iterations = addZeroToIterationVector(newApproximation, iterations, polynomial);
    worstApproximationIndex = getWorstApproximationIndex(approximation, newApproximation);
    [approximation, approximationValue] = deleteWorstApproximation(worstApproximationIndex, approximation, polynomial, newApproximation);
end

function [z0, z1, difference0, difference1] = initializeEquationSystem(approximation, approximationValue)
    z0 = approximation(1) - approximation(3);
    z1 = approximation(2) - approximation(3);
    difference0 = approximationValue(1) - approximationValue(3);
    difference1 = approximationValue(2) - approximationValue(3);
end

function equationsSystem = solveEquationSystem(z0, difference0, z1, difference1)
    equationsSystem = [z0 ^ 2, z0, difference0; z1 ^ 2, z1, difference1];
    reductor = equationsSystem(2, 1) / equationsSystem(1, 1);
    equationsSystem(2, :) = equationsSystem(2, :) - reductor * equationsSystem(1, :);
    equationsSystem(2, 1) = 0;
    equationsSystem(2, :) = equationsSystem(2, :) ./ equationsSystem(2, 2);
    equationsSystem(1, :) = equationsSystem(1, :) - equationsSystem(1, 2) * equationsSystem(2, :);
    equationsSystem(1, :) = equationsSystem(1, :) ./ equationsSystem(1, 1);
end

function [a, b, c] = createApproximatedQuadraticFormula(equationsSystem, approximationValue)
    a = equationsSystem(1, 3);
    b = equationsSystem(2, 3);
    c = approximationValue(3);
end

function [zPlus, zMinus] = findRootsOfQuadraticFormula(a, b, c)
    zPlus = -2 * c / (b + sqrt(b ^ 2 - 4 * a * c));
    zMinus = -2 * c / (b - sqrt(b ^ 2 - 4 * a * c));
end

function newApproximation = chooseNewRoot(zPlus, zMinus, approximation)
    if abs(zPlus) < abs(zMinus)
        newApproximation = approximation(3) + zPlus;
    else
        newApproximation = approximation(3) + zMinus;
    end
end

function iterations = addZeroToIterationVector(newApproximation, iterations, polynomial)
    zero = newApproximation;
    iterations(:, size(iterations, 2) + 1) = [zero, polynomial(zero)];
end

function worstApproximationIndex = getWorstApproximationIndex(approximation, newApproximation)
    worstApproximationIndex = -1;
    worstApproximationDifference = 0;
    for i = 1:size(approximation, 2)
        diff = abs(approximation(i) - newApproximation);
        if diff > worstApproximationDifference
            worstApproximationIndex = i;
            worstApproximationDifference = diff;
        end
    end
end

function [approximation, approximationValue] = deleteWorstApproximation(worstApproximationIndex, approximation, polynomial, newApproximation)
    approximation(worstApproximationIndex) = [];
    approximation(3) = newApproximation;
    approximationValue = arrayfun(polynomial, approximation);
end