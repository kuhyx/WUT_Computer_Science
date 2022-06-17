% finds the eigenValues of a matrix using QR with shifts
function [eigenValues, whatIterationAreWeOn, Matrix] = QRShifts(Matrix)
    eigenFromMatlab = eig(Matrix);
    initialMatrix = Matrix;
    [eigenValues, whatIterationAreWeOn, matrixSize, minThreshold] = initiateValues(Matrix);
    [Matrix, whatIterationAreWeOn, eigenValues] = QRShiftLoop(matrixSize, Matrix, eigenValues, minThreshold, whatIterationAreWeOn);
    dispResults(eigenValues, Matrix, whatIterationAreWeOn, eigenFromMatlab, initialMatrix);
end 

function [eigenValues, whatIterationAreWeOn, matrixSize, minThreshold] = initiateValues(Matrix)
    eigenValues = double.empty(1, 0);
    whatIterationAreWeOn = 0;
    matrixSize = size(Matrix, 1);
    minThreshold = 1e-6;
end

function [Matrix, whatIterationAreWeOn, eigenValues] = QRShiftLoop(matrixSize, Matrix, eigenValues, minThreshold, whatIterationAreWeOn)
    while matrixSize >= 2
        flag = 0;
        [Matrix, matrixSize, whatIterationAreWeOn, eigenValues] = findEigenValue(Matrix, matrixSize, whatIterationAreWeOn, eigenValues, minThreshold, flag);
        [matrixSize, Matrix] = deflateMatrix(Matrix, matrixSize);
    end
    eigenValues(size(eigenValues, 2) + 1) = Matrix(1, 1);
end

function [Matrix, matrixSize, whatIterationAreWeOn, eigenValues] = findEigenValue(Matrix, matrixSize, whatIterationAreWeOn, eigenValues, minThreshold, flag)
    while flag == 0
        eigenValueCorner = getEigenValueFromCorner(Matrix, matrixSize);
        [Matrix, whatIterationAreWeOn] = shiftAndIterate(matrixSize, Matrix, eigenValueCorner, whatIterationAreWeOn);
        [flag, eigenValues] = thresholdBreached(Matrix, matrixSize, minThreshold, eigenValues);
    end
end

function eigenValueCorner = getEigenValueFromCorner(Matrix, matrixSize)
    corner = Matrix((matrixSize - 1) : matrixSize, (matrixSize - 1) : matrixSize);
    % get 2 x 2 corner of the matrix
    eigenValueCorner = solveCharactersticEquation(corner);
end

function [Matrix, whatIterationAreWeOn] = shiftAndIterate(matrixSize, Matrix, eigenValueCorner, whatIterationAreWeOn)
    % shift and iterate algorithm
    identityMatrix = eye(matrixSize);
    Matrix = Matrix - identityMatrix * eigenValueCorner;
    [Q, R] = gramSchmidtAlgorithm(Matrix);
    Matrix = R * Q + identityMatrix * eigenValueCorner;
    whatIterationAreWeOn = whatIterationAreWeOn + 1;
end

function [matrixSize, Matrix] = deflateMatrix(Matrix, matrixSize)
    matrixSize = matrixSize - 1;
    Matrix = Matrix(1:matrixSize, 1:matrixSize);
end

function [flag, eigenValues] = thresholdBreached(Matrix, matrixSize, minThreshold, eigenValues)
    flag = 0;
    threshold = max(abs(Matrix(matrixSize, 1:(matrixSize - 1))));

     % once we zero the row (or rather get close enough to zero) exit loop
    if (threshold <= minThreshold)
        eigenValues(size(eigenValues, 2) + 1) = Matrix(matrixSize, matrixSize);
        flag = 1;
    end
end

% finds the eigenvalue of a 2x2 matrix that is closer to the lower right corner
function eigen = solveCharactersticEquation(Matrix)
    [eigenOne, eigenTwo] = calculateZeros(Matrix);
    eigen = valueCloserToLowerRightCorner(eigenOne, eigenTwo, Matrix);
end

function eigen = valueCloserToLowerRightCorner(eigenOne, eigenTwo, Matrix)
    if abs(Matrix(4) - eigenOne) < abs(Matrix(4) - eigenTwo)
        eigen = eigenOne;
    else
        eigen = eigenTwo;
    end
end

function [zeroOne, zeroTwo] = calculateZeros(Matrix)
    b = Matrix(1) + Matrix(4);
    ac = Matrix(1) * Matrix(4) - Matrix(2) * Matrix(3);
    delta = (b) ^ 2 - 4 * ac;
    % get delta of quadratic equation
    squareRootDelta = sqrt(delta);
    % square delta
    zeroOne = (b - squareRootDelta) / 2;
    zeroTwo = (b + squareRootDelta) / 2;
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

function dispResults(eigenValues, Matrix, whatIterationAreWeOn, eigenFromMatlab, initialMatrix)
    disp("Initial matrix: ");
    disp(initialMatrix);
    disp("Final matrix: ");
    disp(Matrix);
    disp("Number of iterations: ");
    disp(whatIterationAreWeOn);
    disp("Eigen values from eig(Matrix):");
    disp(eigenFromMatlab);
    disp("Our eigen values: ");
    disp(eigenValues);
end