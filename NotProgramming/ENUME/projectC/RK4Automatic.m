function [x, sizes, errors] = RK4Automatic(equations, initialValues, interval, initialStepSize, relativeEpsilon, absoluteEpsilon)
    [functionArguments, x, sizes, errors, stepSize, step, flag] = Initialize(interval, initialValues, initialStepSize);
    [functionArguments, x, sizes, errors] = RK4AutomaticLoop(functionArguments, x, sizes, errors, stepSize, step, equations, relativeEpsilon, absoluteEpsilon, interval, flag);
    x = [functionArguments; x];
end

function [functionArguments, x, sizes, errors, stepSize, step, flag] = Initialize(interval, initialValues, initialStepSize)
    functionArguments = interval(1);
    x = initialValues;
    
    sizes = double.empty();
    errors = double.empty();
    
    stepSize = initialStepSize;
    step = 0;
    flag = 1;
end

function [functionArguments, x, sizes, errors] = RK4AutomaticLoop(functionArguments, x, sizes, errors, stepSize, step, equations, relativeEpsilon, absoluteEpsilon, interval, flag)
   while flag
       [functionArguments, x, sizes, errors, stepSize, step, interval, flag] = insideWhileLoop(functionArguments, x, sizes, errors, stepSize, step, equations, relativeEpsilon, absoluteEpsilon, interval, flag);
   end
end

function [functionArguments, x, sizes, errors, stepSize, step, interval, flag] = insideWhileLoop(functionArguments, x, sizes, errors, stepSize, step, equations, relativeEpsilon, absoluteEpsilon, interval, flag)
    [step, stepValue, x, functionArguments, flag] = calculateXandFunctionArguments(step, x, equations, stepSize, functionArguments, interval);
    if ~flag
        return;
    end
    [stepSize, errors] = calculateStepAndErrors(equations, stepValue, stepSize, x, step, relativeEpsilon, absoluteEpsilon, errors);
    sizes(step) = stepSize;

end

function [step, stepValue, x, functionArguments, flag] = calculateXandFunctionArguments(step, x, equations, stepSize, functionArguments, interval)
    [step, stepValue] = initializeSteps(step, x);
    x = equationsLoop(x, equations, stepValue, stepSize, step);
    [flag, functionArguments] = stopAlgorithm(functionArguments, stepSize, step, interval);
end

function [stepSize, errors] = calculateStepAndErrors(equations, stepValue, stepSize, x, step, relativeEpsilon, absoluteEpsilon, errors)
    stepValue = calculateNextStep(equations, stepValue, stepSize);
    [stepCorrectionFactor, errors] = calculateStepCorrection(stepValue, x, step, relativeEpsilon, absoluteEpsilon, errors);
    stepSize = 0.9 * stepCorrectionFactor * stepSize;
end

function [step, stepValue] = initializeSteps(step, x)
    step = step + 1;
    stepValue = x(:, step);
end

function x = equationsLoop(x, equations, stepValue, stepSize, step)
    for equationNumber = 1 : 2
        Phi = RK4Phi(equations{equationNumber}, stepValue, stepSize);
        x(equationNumber, step + 1) = x(equationNumber, step) + stepSize * Phi;
    end
end

function [flag, functionArguments] = stopAlgorithm(functionArguments, stepSize, step, interval)
    functionArguments(step + 1) = functionArguments(step) + stepSize;
    if functionArguments(end) >= interval(2)
        flag = 0;
    else
        flag = 1;
    end
end

function stepValue  = calculateNextStep(equations, stepValue, stepSize)
    for halfStep = 1 : 2
        for equationsNumber = 1:size(equations, 1)
            Phi = RK4Phi(equations{equationsNumber}, stepValue, stepSize / 2);
            stepValue(equationsNumber) = stepValue(equationsNumber) + (stepSize / 2) * Phi;
        end
    end
end

function [stepCorrectionFactor, errors] = calculateStepCorrection(stepValue, x, step, relativeEpsilon, absoluteEpsilon, errors)
    stepCorrectionFactor = Inf; % Initialize stepCorrectionFactor
    [stepCorrectionFactor, errors] = calculateStepCorrectionLoop(stepValue, x, step, relativeEpsilon, absoluteEpsilon, errors, stepCorrectionFactor);
    stepCorrectionFactor = stepCorrectionFactor ^ (1/5);
end

function [stepCorrectionFactor, errors] = calculateStepCorrectionLoop(stepValue, x, step, relativeEpsilon, absoluteEpsilon, errors, stepCorrectionFactor)
    for equationsNumber = 1 : 2
        approximationError = abs(stepValue(equationsNumber) - x(equationsNumber, step + 1)) / 15;
        errors(step) = approximationError;
        
        epsilon = abs(stepValue(equationsNumber)) * relativeEpsilon + absoluteEpsilon;
        equationAlpha = epsilon / approximationError;
        
        if equationAlpha < stepCorrectionFactor
            stepCorrectionFactor = equationAlpha; 
        end
    end
end
