function x = AdamsPCMethod(functions, initialValues, interval, stepSize)
    [x, derrivatives, explicitCoefficients, implicitCoefficients, stepCount] = initialize(functions, initialValues, interval, stepSize);
    x = adamsPcLoop(x, derrivatives, explicitCoefficients, implicitCoefficients, stepCount, functions, stepSize);
    % append arguments to output
    x = [interval(1):stepSize:(stepCount * stepSize); x];
end

function [x, derrivatives, explicitCoefficients, implicitCoefficients, stepCount] = initialize(functions, initialValues, interval, stepSize)
    % obtain first five steps from RK4
    [x, derrivatives] = RK4(functions, initialValues, interval, stepSize, 5);
    x = x(2:end, :);
    
    % define coefficient 
    explicitCoefficients = [1901, -2774, 1616, -1274, 251] / 720; 
    % Constants that can  be found on the Internet or in Mister Tatjewski
    % book on page 177, notice how beta(3) = 1616 instead of 2616
    % I have found on the internet different value for this parameter and
    % got better results with it so I decided to stick with it
    implicitCoefficients = [475, 1427, -798, 482, -173, 27] / 1440;  
    % Constants that can  be found on the Internet or in Mister Tatjewski
    % book on page 178
    % build output based on preceding values
    stepCount = ceil((interval(2) - interval(1)) / stepSize);
end

function x = adamsPcLoop(x, derrivatives, explicitCoefficients, implicitCoefficients, stepCount, functions, stepSize)
    for step = 6: (stepCount + 1)    
        [x, derrivatives] = PECE(x, derrivatives, explicitCoefficients, implicitCoefficients, step, functions, stepSize);
    end
end

function [x, derrivatives] = PECE(x, derrivatives, explicitCoefficients, implicitCoefficients, step, functions, stepSize)
    % P
    predictionOfX = adamsPredict(x, step, stepSize, explicitCoefficients, derrivatives);
        
    % E
    derrivativePrediction = zeros(size(functions, 1), 1);
    derrivativePrediction = adamsEvaluate(functions, predictionOfX, derrivativePrediction);
        
    % C
    x = adamsCorrect(step, functions, stepSize, implicitCoefficients, derrivatives, derrivativePrediction, x);
    
    % E
    derrivatives = adamsEvaluateTwo(functions, step, x, derrivatives);
end


function predictionOfX = adamsPredict(x, step, stepSize, explicitCoefficients, derrivatives)
    % predict
    predictionOfX = x(:, step - 1);
    for equationNumber = 1 : 2
        for previous = 1:5
            predictionOfX(equationNumber) = predictionOfX(equationNumber) ...
                + stepSize * explicitCoefficients(previous) * derrivatives(equationNumber, step - previous);
        end
    end
end

function derrivativePrediction = adamsEvaluate(functions, predictionOfX, derrivativePrediction)
    for equationNumber = 1:size(functions, 1)
        derrivativePrediction(equationNumber) = functions{equationNumber}(predictionOfX);
    end
end

function x = adamsCorrect(step, functions, stepSize, implicitCoefficients, derrivatives, derrivativePrediction, x)
    x(:, step) = x(:, step - 1);
    for equationNumber = 1:size(functions, 1)
        for previous = 1:5
            x(equationNumber, step) = x(equationNumber, step) + stepSize * implicitCoefficients(previous + 1) * derrivatives(equationNumber, step - previous);
        end
        x(equationNumber, step) = x(equationNumber, step) + stepSize * implicitCoefficients(1) * derrivativePrediction(equationNumber);
    end
end

function derrivatives = adamsEvaluateTwo(functions, step, x, derrivatives)
    for equationNumber = 1:size(functions, 1)
        derrivatives(equationNumber, step) = functions{equationNumber}(x(:, step));
    end
end