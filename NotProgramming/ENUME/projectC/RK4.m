% solve ODE system using RK4 with constant step size
function [x, derivativesTable] = RK4(equations, initialValues, interval, stepSize, maxSteps)
    x = initialValues;

    derivativesTable = buildDerivatiesTable(x, equations);
    
    % Calculate stepCount
    stepCount = ceil((interval(2) - interval(1)) / stepSize);
    if nargin == 5
        stepCount = min(stepCount, maxSteps - 1);
    end % IF we include max steps in our function input
    % (nargin is number of arguments in input)
    % then choose smaller number between maxSteps and stepCount and choose
    % it for stepCount

    [x, derivativesTable] = rk4Loop(x, stepCount, stepSize, equations, derivativesTable);

    
    % append arguments to output
    x = [interval(1):stepSize:(stepCount * stepSize); x];
end

function derivativesTable = buildDerivatiesTable(x, equations)
    derivativesTable = zeros(size(x));
    for eqnum = 1:size(equations, 1)
        derivativesTable(eqnum, 1) = equations{eqnum}(x(:, 1));
    end
end

function [x, derivativesTable] = rk4Loop(x, stepCount, stepSize, equations, derivativesTable)
    for step = 1 : stepCount
        [x, derivativesTable] = rk4stepLoop(x, step, equations, stepSize, derivativesTable);
    end
end

function [x, derivativesTable] = rk4stepLoop(x, step, equations, stepSize, derivativesTable)
    stepValue = x(:, step);
    [x, derivativesTable] = equationsLoop(x, equations, stepValue, stepSize, step, derivativesTable);
end

function [x, derivativesTable] = equationsLoop(x, equations, stepValue, stepSize, step, derivativesTable)
    for equationNumber = 1 : 2
        Phi = RK4Phi(equations{equationNumber}, stepValue, stepSize);
        x(equationNumber, step + 1) = x(equationNumber, step) + stepSize * Phi;
        
        derivativesTable(equationNumber, step + 1) = equations{equationNumber}(x(:, step + 1));
    end
end