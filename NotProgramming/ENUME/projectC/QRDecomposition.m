function [Q, R, QTQInverse] = QRDecomposition(A)
    [Q, R, QTQInverse, upperLoopLimit] = initialize(A);
    [Q, R, QTQInverse] = GramSchmidtAlgorithm(A, Q, R, QTQInverse, upperLoopLimit);
end

function [Q, R, QTQInverse, upperLoopLimit] = initialize(Matrix)
    Q = zeros(size(Matrix));
    upperLoopLimit = size(Matrix, 2);
    R = eye(upperLoopLimit);
    QTQInverse = zeros(upperLoopLimit);
end

function [Q, R, QTQInverse] = GramSchmidtAlgorithm(A, Q, R, QTQInverse, upperLoopLimit)
    for column = 1 : upperLoopLimit
        [Q, R, QTQInverse, A] = GramSchmidtAlgorithmOuterLoop(upperLoopLimit, A, Q, R, QTQInverse, column);
    end
end

function [Q, R, QTQInverse, A] = GramSchmidtAlgorithmOuterLoop(upperLoopLimit, A, Q, R, QTQInverse, column)

    [columnDotProduct, QTQInverse, Q] = calculateColumnDotProduct(A, column, Q, QTQInverse);
    [R, A] = orthogonalizeFurther(column, A, columnDotProduct, Q, R, upperLoopLimit);
end

function [columnDotProduct, QTQInverse, Q] = calculateColumnDotProduct(A, column, Q, QTQInverse)
    Q(:, column) = A(:, column);
    
    columnDotProduct = dot(Q(:, column), Q(:, column));
    QTQInverse(column, column) = 1 / columnDotProduct;
end

function [R, A] = orthogonalizeFurther(column, A, columnDotProduct, Q, R, upperLoopLimit)
    for next = (column + 1): upperLoopLimit
        R(column, next) = dot(Q(:, column), A(:, next)) / columnDotProduct;
        A(:, next) = A(:, next) - R(column, next) * Q(:, column);
    end
end