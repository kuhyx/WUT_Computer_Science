function plotIterations()
    maxMatrixSize = 500;
    iterationsJ = zeros(maxMatrixSize);
    iterationsG = zeros(maxMatrixSize);
    for i = 1 : maxMatrixSize
        [~, ~, whichIterationAreWeOnJ, whichIterationAreWeOnG] = iterative(matrixA(i), vectorA(i));
        iterationsJ(i) = whichIterationAreWeOnJ;
        iterationsG(i) = whichIterationAreWeOnG;
    end
    nexttile
    plot(iterationsJ, '.');
    title('Number of iterations for different sizes of matrices for Jacobi method');
    xlabel('Size of matrix A');
    ylabel('Number of iterations');
    nexttile
    plot(iterationsG, '.');
    title('Number of iterations for different sizes of matrices for Gauss-Seidel method');
    xlabel('Size of matrix A');
    ylabel('Number of iterations');
   
end