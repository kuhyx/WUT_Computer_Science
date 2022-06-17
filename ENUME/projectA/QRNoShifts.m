function [eigenValues, whichIterationAreWeOn, Matrix] = QRNoShifts(Matrix)

    [whichIterationAreWeOn, threshold, startingMatrix, matlabEigen] = initializeValues(Matrix);
    [Matrix, whichIterationAreWeOn] = QRNoShiftsLoop(threshold, Matrix, whichIterationAreWeOn);
    eigenValues = diag(Matrix)';
    %displayResults(eigenValues, whichIterationAreWeOn, Matrix, startingMatrix, matlabEigen);
end

function [Matrix, whichIterationAreWeOn] = QRNoShiftsLoop(threshold, Matrix, whichIterationAreWeOn)
    while threshold > 1e-6
        [Matrix, whichIterationAreWeOn, threshold] = QRNoShiftsInsideLoop(Matrix, whichIterationAreWeOn);
    end
end

function [Matrix, whichIterationAreWeOn, threshold] = QRNoShiftsInsideLoop(Matrix, whichIterationAreWeOn)
    [Q, R] = gramSchmidtAlgorithm(Matrix);
    Matrix = R * Q;
    whichIterationAreWeOn = whichIterationAreWeOn + 1;
    
    % iterate until all non-diagonal elements are below the threshold
    matrixWithoutDiagonal = Matrix - diag(diag(Matrix)); % first diag converts Matrix 
    % into vector consisting of values on the diagonal of matrix, 
    % second diag converts this vector into matrix with zeros on
    % everything except diagonal
    % If we substract it from Matrix we get original Matrix with zeros
    % on a diagonal
    threshold = max(max(abs(matrixWithoutDiagonal)));
    % first max returns vector of elements 
    % second max returns max element from this vector
end

function displayResults(eigenValues, whichIterationsAreWeOn, Matrix, startingMatrix, matlabEigen)
    disp("How many iterations it took:")
    disp(whichIterationsAreWeOn)
    disp("Starting Matrix:")
    disp(startingMatrix)
    disp("Final Matrix:")
    disp(Matrix)
    disp("eig(Matrix) eigen values:")
    disp(matlabEigen)
    disp("Our eigen values:")
    disp(eigenValues);
end

function [whichIterationAreWeOn, threshold, startingMatrix, matlabEigen] = initializeValues(Matrix)
    whichIterationAreWeOn = 0;
    threshold = inf;
    startingMatrix = Matrix;
    matlabEigen = eig(Matrix);
end

% performs QR or QRdash decomposition of a matrix
function [Q, R] = gramSchmidtAlgorithm(Matrix)
    [columns, Q, R, d] = initializeGramSchmid(Matrix);
    [Q, R] = factorizeColumnsOfQ(columns, Q, Matrix, R, d);
    [Q, R] = normalizeColumns(columns, Q, R);
end

function [columns, Q, R, d] = initializeGramSchmid(Matrix)
    % We start with empty matrices
    [rows, columns] = size(Matrix);
    Q = zeros(rows, columns);
    R = zeros(columns, columns);
    d = zeros(1, columns);
end

function [Q, R] = factorizeColumnsOfQ(columns, Q, Matrix, R, d)
    for i = 1 : columns 
        Q(:, i) = Matrix(:, i);
        R(i, i) = 1;
        d(i) = Q(:, i)' * Q(:, i);
        for i2 = i + 1 : columns 
            R(i, i2) = (Q(:, i)' * Matrix(:, i2)) / d(i);
            Matrix(:, i2) = Matrix(:, i2) - R(i, i2) * Q(:, i);
        end
    end
end

function [Q, R] = normalizeColumns(columns, Q, R)
    for i = 1 : columns
        dd = norm(Q(:, i));
        Q(:, i) = Q(:, i) / dd;
        R(i, i:columns) = R(i, i : columns) * dd;
    end
end