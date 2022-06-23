function task4Plot(maxMatrixSize)
    iterationsNoShiftsVector = zeros(maxMatrixSize);
    iterationsShiftsVector = zeros(maxMatrixSize);
    for i = 1 : maxMatrixSize
        [~, iterationsNoShifts, ~, ~, iterationsShifts, ~] = task4(matrix4(i));
        iterationsNoShiftsVector(i) = iterationsNoShifts;
        iterationsShiftsVector(i) = iterationsShifts;
    end
    nexttile
    plot(iterationsNoShiftsVector, '.');
    title('Number of iterations for different sizes of matrices for no shift method');
    xlabel('Size of matrix A');
    ylabel('Number of iterations');
    nexttile
    plot(iterationsShiftsVector, '.');
    title('Number of iterations for different sizes of matrices for shift method');
    xlabel('Size of matrix A');
    ylabel('Number of iterations');
end