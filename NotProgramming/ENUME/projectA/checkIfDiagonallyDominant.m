function d = checkIfDiagonallyDominant(Matrix)
    d = 1;
    [Rows, ~] = size(Matrix);
    for i = 1 : Rows
        rowsSum = 0;
        for j = 1 : Rows
            rowsSum = rowsSum + abs(Matrix(i, j));
        end
        rowsSum = rowsSum - Matrix(i, i);
        if Matrix(i, i) <= rowsSum
            d = 0;
            break
        end
    end
end