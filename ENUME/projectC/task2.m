
function task2()
    [ordinaryDifferentialEquations, initialValues, interval, algorithms] = initialize();
    solveAndPrintODEs(algorithms, ordinaryDifferentialEquations, initialValues, interval);
    [result, sizes, errors] = solveAndPlotODEAutomatic(ordinaryDifferentialEquations, initialValues, interval);
    plotStatistics(result, sizes, errors);
    plotComparisonToMatlabFunction(ordinaryDifferentialEquations, interval, initialValues);
end

function [ordinaryDifferentialEquations, initialValues, interval, algorithms] = initialize()
    ordinaryDifferentialEquations = {
        @(x) x(2) + x(1) * (0.5 - x(1)^2 - x(2)^2);
        @(x) -x(1) + x(2) * (0.5 - x(1)^2 - x(2)^2)
    };
    initialValues = [8; 9];
    interval = [0; 15];
    
    algorithms = {
        'RK4 algorithm', @RK4, [0.01, 0.011];
        'Adams PC algorithm', @AdamsPCMethod, [0.002, 0.013]
    };
end

function solveAndPrintODEs(algorithms, ordinaryDifferentialEquations, initialValues, interval)
    for algorithm = 1 : 2
        [algorithmName, algorithmFunction, stepSizes] = algorithms{algorithm, :};
        stepResults = solveForEachStep(stepSizes, ordinaryDifferentialEquations, initialValues, interval, algorithmFunction);
        plotAgainstTime(ordinaryDifferentialEquations, algorithmName, stepResults);
        plotAgainst(algorithmName, stepResults);

    end
end

function stepResults = solveForEachStep(stepSizes, ordinaryDifferentialEquations, initialValues, interval, algorithmFunction)
    stepResults = cell(size(stepSizes, 2), 3);
    stepNames = {'Optimal Step Size', 'Slightly Larger Step Size'};
    for stepNumber = 1:size(stepSizes, 2)
        result = algorithmFunction(ordinaryDifferentialEquations, initialValues, interval, stepSizes(stepNumber));
        stepResults(stepNumber, :) = {stepSizes(stepNumber), stepNames{stepNumber}, result};
    end
end

function beginPlot()
    figure; 
    grid on; 
    hold on;
end

function plotAgainstTime(ordinaryDifferentialEquations, algorithmName, stepResults)
    for equationNumber = 1:size(ordinaryDifferentialEquations, 1)
        beginPlot();

        title([algorithmName, ', x_', num2str(equationNumber), ' ODE']);

        for stepresult = stepResults'
            plot(stepresult{3}(1, :), stepresult{3}(equationNumber + 1, :));
        end

        hold off;
        legend(stepResults{:, 2});
    end
end

function plotAgainst(algorithmName, stepResults)
    beginPlot();
    title([algorithmName, ' trajectory plot (x_2 compared to x_1)']);
    for stepresult = stepResults'
        plot(stepresult{3}(2, :), stepresult{3}(3, :));
    end
    hold off;
    legend(stepResults{:, 2});
%    %print(['report/', func2str(algfunc), 'traj'], '-dpdf');
end

function [result, sizes, errors] = solveAndPlotODEAutomatic(ordinaryDifferentialEquations, initialValues, interval)
    [result, sizes, errors] = solveRKAutomatic(ordinaryDifferentialEquations, initialValues, interval);
    plotTrajectory(result);
end

function [result, sizes, errors] = solveRKAutomatic(ordinaryDifferentialEquations, initialValues, interval)
    initialStepSize = 1e-5;
    relativeEpsilon = 1e-9;
    absoluteEpsilon = 1e-9;
    [result, sizes, errors] = RK4Automatic(ordinaryDifferentialEquations, initialValues, interval, initialStepSize, relativeEpsilon, absoluteEpsilon);
end

function plotTrajectory(result)
    figure;
    plot(result(2, :), result(3, :));
    grid on;
    title('RK4 with auto step trajectory plot (x_2 against x_1)');
end

function plotStatistics(result, sizes, errors)
    stats = {
        "RK4 with auto step step size", "rk4sizes", sizes;
        "RK4 with auto step approximation error", "rk4errors", errors
    };
    for stat = stats'
        figure;
        plot(result(1, 2:(end - 1)), stat{3});
        grid on;
        title(stat{1});
    end
end

function plotComparisonToMatlabFunction(ordinaryDifferentialEquations, interval, initialValues) 
    % compare results with ODE45
    odefun = @(t, x) [ ordinaryDifferentialEquations{1}(x); ordinaryDifferentialEquations{2}(x) ];
    odeoptions = odeset('RelTol', 10e-10, 'AbsTol', 10e-10);
    [~, x] = ode45(odefun, interval, initialValues, odeoptions);
    figure;
    plot(x(:, 1), x(:, 2));
    grid on;
    title('ODE45 trajectory plot (x_2 against x_1)');
end