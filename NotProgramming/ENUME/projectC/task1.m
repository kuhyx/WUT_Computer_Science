function task1(polynomialDegree)
    for currentPolynomialDegree = 0 : polynomialDegree
        dataPoints = functionDataPoints();
        % obtain LSPSolutions of approximating polynomial
        [LSPSolutions, error, conditionNumber] = approximate(dataPoints, currentPolynomialDegree);
        displayInfo(currentPolynomialDegree, error, conditionNumber);
        plotGraph(currentPolynomialDegree, dataPoints, LSPSolutions)
    end
end

function displayInfo(currentPolynomialDegree, error, conditionNumber)
    disp("Current Polynomial Degree:");
    disp(currentPolynomialDegree);
    disp("Error: ");
    disp(error);
    disp("Condition number of Gram's Matrix: ");
    disp(conditionNumber);
end

function plotGraph(currentPolynomialDegree, dataPoints, LSPSolutions)
    figure;
    grid on;
    hold on;
    plotDataPoints(currentPolynomialDegree, dataPoints);
    plotApproximation(dataPoints, LSPSolutions);
    hold off;
end

function plotDataPoints(currentPolynomialDegree, dataPoints)
    title(['Polynomial approximation of the funtion using: ', num2str(currentPolynomialDegree), ' degree']);
    scatter(dataPoints(:, 1), dataPoints(:, 2), 72, 'x');
end

function plotApproximation(dataPoints, LSPSolutions)
    x = dataPoints(1):0.05:dataPoints(end, 1);
    y = valueApproximationAtx(LSPSolutions, x);
    plot(x, y);
end


% find the approximating polynomial of the given degree
function [LSPSolutions, error, conditionNumber] = approximate(dataPoints, polydeg)
    % initialize A matrix
    A = zeros(size(dataPoints, 1), polydeg + 1);
    
    A = calculateACells(dataPoints, A);
    LSPSolutions = solveLSP(A, dataPoints);

    % Calculate error of solution
    error = norm(dataPoints(:, 2) - A * LSPSolutions);
    % Calculate condition number of Gram's matrix
    GramsMatrix = A' * A;
    conditionNumber = cond(GramsMatrix);
end

function Matrix = calculateACells(dataPoints, Matrix)
    for row = 1 : size(Matrix, 1)
        for column = 1 : size(Matrix, 2)            
            Matrix(row, column) = dataPoints(row, 1) ^ (column - 1);
        end
    end
end

function solutions = solveLSP(Matrix, dataPoints)
    [Q, eqsys, invqtq] = QRDecomposition(Matrix);
    eqsys(:, end + 1) = invqtq * Q' * dataPoints(:, 2);
    solutions = backSubstitution(eqsys);
end

% evaluate the value of an approximation at the given x
function arrayOfValues = valueApproximationAtx(LSPSolutions, arrayOfArguments)
    arrayOfValues = zeros(1, size(arrayOfArguments, 2));
    arrayOfValues = calculateArrayofValues(arrayOfArguments, arrayOfValues, LSPSolutions);
end

function arrayOfValues = calculateArrayofValues(arrayOfArguments, arrayOfValues, LSPSolutions)
    for x = 1 : size(arrayOfArguments, 2)
        for i = 1 : size(LSPSolutions, 1)
            arrayOfValues(x) = arrayOfValues(x) + LSPSolutions(i) * arrayOfArguments(x) ^ (i - 1);
        end
    end
end
