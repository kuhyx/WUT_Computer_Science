function plotErrorsGaussian(maxMatrixSize)

    errorsA = zeros(maxMatrixSize);
    errorsB = zeros(maxMatrixSize);
    errorsAR = zeros(maxMatrixSize);
    errorsBR = zeros(maxMatrixSize);
    for i = 1 : maxMatrixSize
        [~, errorBeforeResidualCorrection, errorAfterResidualCorrection] = indicatedMethod(matrixA(i), vectorA(i));
        errorsA(i) = errorBeforeResidualCorrection;
        errorsAR(i) = errorAfterResidualCorrection;
        [~, errorBeforeResidualCorrection, errorAfterResidualCorrection] = indicatedMethod(matrixB(i), vectorB(i));
        errorsB(i) = errorBeforeResidualCorrection;
        errorsBR(i) = errorAfterResidualCorrection;
    end
    nexttile
    plot(errorsA, '.');
    title('Errors before residual correction for task 2a:');
    xlabel('Size of matrix A');
    ylabel('Errors');
    nexttile
    plot(errorsAR, '.');
    title('Errors after residual correction for task 2a:');
    xlabel('Size of matrix A');
    ylabel('Errors');
    nexttile
    plot(errorsB, '.');
    title('Errors before residual correction for task 2b:');
    xlabel('Size of matrix A');
    ylabel('Errors');
    nexttile
    plot(errorsBR, '.');
    title('Errors after residual correction for task 2b:');
    xlabel('Size of matrix A');
    ylabel('Errors');
   
end