function [x_j, x_g, whichIterationAreWeOnJ, whichIterationAreWeOnG] = iterative(Matrix, Vector)
    [L, D, U, initial_x, whichIterationAreWeOnJ, whichIterationAreWeOnG, demandedToleranceJ, demandedToleranceG, flag, Rows] = initializeValues(Matrix);
    [x_j, whichIterationAreWeOnJ, demandedToleranceJ] = jacobiLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOnJ, demandedToleranceJ, Vector, flag);
    [x_g, whichIterationAreWeOnG, demandedToleranceG] = gaussSeidelLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOnG, demandedToleranceG, Vector, flag, Rows);
    dispFinalResults(x_j, x_g, demandedToleranceJ, demandedToleranceG, whichIterationAreWeOnJ, whichIterationAreWeOnG, Matrix, Vector);
end

function [L, D, U, initial_x, whichIterationAreWeOnJ, whichIterationAreWeOnG, demandedToleranceJ, demandedToleranceG, flag, Rows] = initializeValues(Matrix)
    [Rows, ~] = size(Matrix);
    [L, D, U] = decomposeMatrix(Matrix);
    initial_x = zeros(Rows, 1);
    whichIterationAreWeOnJ = 0;
    whichIterationAreWeOnG = 0;
    demandedToleranceJ = 10e-10; % as per task description
    demandedToleranceG = 10e-10; % as per task description
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

function [x_j, whichIterationAreWeOn, demandedTolerance]  = jacobiLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector, flag)
    while flag ~= 1 % flag denotes whether norm(Matrix*x_g-Vector) <= demandedTolerance
        [x_j, whichIterationAreWeOn, demandedTolerance, flag, initial_x] = jacobiInsideLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector);
    end
end

function [x_g, whichIterationAreWeOn, demandedTolerance]  = gaussSeidelLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector, flag, Rows)
    while flag ~= 1 % flag denotes whether norm(Matrix*x_g-Vector) <= demandedTolerance
        [x_g, whichIterationAreWeOn, demandedTolerance, flag, initial_x] = gaussiInsideLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector, Rows);
    end
end

function [x_j, whichIterationAreWeOn, demandedTolerance, flag, initial_x] = jacobiInsideLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector)
    x_j = jacobiEquation(D, L, U, initial_x, Vector);
    [flag, demandedTolerance] = checkError(x_j, initial_x, demandedTolerance, Matrix, Vector);
    [initial_x, whichIterationAreWeOn] = endOfLoop(x_j, whichIterationAreWeOn);
end

function [x_j, whichIterationAreWeOn, demandedTolerance, flag, initial_x] = gaussiInsideLoop(Matrix, L, D, U, initial_x, whichIterationAreWeOn, demandedTolerance, Vector, Rows)
    x_j = gaussSeidelEquation(D, L, U, initial_x, Vector, Rows);
    [flag, demandedTolerance] = checkError(x_j, initial_x, demandedTolerance, Matrix, Vector);
    [initial_x, whichIterationAreWeOn] = endOfLoop(x_j, whichIterationAreWeOn);
end

function x = jacobiEquation(D, L, U, initial_x, Vector)
    x = - D \ ( L + U ) * initial_x + D \ Vector; % As per formula
    % We will be using D \ Vector and D \ ( ) instead of inverseD since
    % this is faster according to matlab
end

function x_g = gaussSeidelEquation(D, L, U, initial_x, Vector, Rows)
    W = U*initial_x - Vector;
    x_g(1, 1) = -W(1, 1) / D(1,1);
    for i = 2 : Rows
        x_g(i, 1) = calculateNominator(i, L, x_g, W) / D(i, i);
    end
end

function nominator = calculateNominator(i, L, x_g, W)
    nominator = 0;
    for j = 1 : i - 1
    nominator = nominator + L(i, j) * x_g(j);
    end
    nominator = - nominator - W(j + 1, 1);
end

function [flag, demandedTolerance] = checkError(x_g, initial_x, demandedTolerance, Matrix, Vector)
    flag = 0;
    currentError = norm(x_g - initial_x);
    if currentError <= demandedTolerance
        currentError = norm(Matrix*x_g-Vector);

        if currentError <= demandedTolerance % if sequence as per textbook
            flag = 1;
        else 
            demandedTolerance = demandedTolerance * 1; % arbitrary value
        end
    end
end

function [initial_x, whichIterationAreWeOn, flag] = endOfLoop(x_g, whichIterationAreWeOn)
    initial_x = x_g;
    whichIterationAreWeOn = whichIterationAreWeOn + 1;
    flag = 0;
end
 
function dispFinalResults(x_j, x_g, demandedToleranceJ, demandedToleranceG, whichIterationAreWeOnJ, whichIterationAreWeOnG, Matrix, Vector)
    disp("Final demandedTolerance for Jacobi method");
    disp(demandedToleranceJ);
    disp("Final demandedTolerance for Gaussian-Seidel method:");
    disp(demandedToleranceG);
    disp("Final Iteration for Jacobi method: ");
    disp(whichIterationAreWeOnJ);
    disp("Final Iteration for Gaussian-Seidel method: ");
    disp(whichIterationAreWeOnG);
    disp("Error for Jacobi method:");
    disp(norm(Matrix*x_j - Vector));
    disp("Error for Gaussian-Seidel method:");
    disp(norm(Matrix*x_g - Vector));
    disp("A\b error:");
    disp(norm(Matrix * (Matrix\Vector) - Vector));
    disp("Answer for Jacobi method: ");
    disp(x_j);
    disp("Answer for Gaussian-Seidel method: ");
    disp(x_g);
end