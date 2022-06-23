function solution = backSubstitution(Matrix)
    Columns = size(Matrix, 1);
    Matrix = backSubstitutionOuterLoop(Matrix, Columns);
    % rightmost column of the Matrix is now our result
    solution = Matrix(:, size(Matrix, 2));
end

function Matrix = backSubstitutionOuterLoop(Matrix, Columns)
    for k = Columns : -1 : 1
        % Diagonal coefficients of matrix need to be equal to 1
        Matrix(k, :) = Matrix(k, :) / Matrix(k, k);
        Matrix = eliminateFactors(Matrix, k);
    end
end

function Matrix = eliminateFactors(Matrix, k)
    for row = (k - 1) : -1 : 1
        Matrix(row, :) = Matrix(row, :) - Matrix(k, :) * (Matrix(row, k) / Matrix(k, k));
    end
end
