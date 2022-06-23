function x = gaussSeidelMethod(Matrix, Vector)
    [L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, flag, Rows] = initializeValues(Matrix);
    [x, whichIterationAreWeOn, demandedTolerance] = jacobiLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector, flag, Rows);
    dispFinalResults(x, demandedTolerance, whichIterationAreWeOn, Matrix, Vector);
end

function [L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, flag, Rows] = initializeValues(Matrix)
    [Rows, ~] = size(Matrix);
    [L, D, U] = decomposeMatrix(Matrix);
    initial_x = zeros(Rows, 1);
    whichIterationAreWeOn = 0;
    demandedTolerance = 10e-10; % as per task description
    flag = 0;
end

function [L, D, U] = decomposeMatrix(Matrix)
    D = diag(diag(Matrix));
    U = triu(Matrix, 1); % Generates upper triangular part of matrix
    % where the second variable denotes on which diagonal of matrix should we
    % start
    L = tril(Matrix, -1); % Generates lower triangular part of matrix
    % where the second variable denotes on which diagonal of matrix should we
    % start
end

function [x, whichIterationAreWeOn, demandedTolerance]  = jacobiLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector, flag, Rows)
    while flag ~= 1 % flag denotes whether norm(Matrix*x-Vector) <= demandedTolerance
        [x, whichIterationAreWeOn, demandedTolerance, flag, initial_x] = jacobiInsideLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector, Rows);
    end
end

function [x, whichIterationAreWeOn, demandedTolerance, flag, initial_x] = jacobiInsideLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector, Rows)
    x = jacobiEquation(D, L, U, initial_x, Vector);
    [flag, demandedTolerance] = checkError(x, initial_x, demandedTolerance, Matrix, Vector);
    [initial_x, whichIterationAreWeOn] = endOfLoop(x, whichIterationAreWeOn);
end

function x = jacobiEquation(D, L, U, initial_x, Vector, Rows)
    W = U*initial_x - Vector;
    x(1, 1) = -W(1, 1) / D(1,1);
    for i = 2 : Rows
        x(i, 1) = calculateNominator(i, L, x, W) / D(i, i);
    end
end

function nominator = calculateNominator(i, L, x, W)
    nominator = 0;
    for j = 1 : i - 1
    nominator = nominator + L(i, j) * x(j);
    end
    nominator = - nominator - W(j + 1, 1);
end

function [flag, demandedTolerance] = checkError(x, initial_x, demandedTolerance, Matrix, Vector)
    flag = 0;
    currentError = norm(x - initial_x);
    if currentError <= demandedTolerance
        currentError = norm(Matrix*x-Vector);

        if currentError <= demandedTolerance % if sequence as per textbook
            flag = 1;
        else 
            demandedTolerance = demandedTolerance * 2; % arbitrary value
        end
    end
end

function [initial_x, whichIterationAreWeOn, flag] = endOfLoop(x, whichIterationAreWeOn)
    initial_x = x;
    whichIterationAreWeOn = whichIterationAreWeOn + 1;
    flag = 0;
end
 
function dispFinalResults(x, demandedTolerance, whichIterationAreWeOn, Matrix, Vector)
    disp("Final demandedTolerance");
    disp(demandedTolerance);
    disp("Final Iteration: ");
    disp(whichIterationAreWeOn);
    disp("Error:");
    disp(norm(Matrix*x - Vector));
    disp("A\b error:");
    disp(norm(Matrix * (Matrix\Vector) - Vector));
end