% find the root brackets of a function within the given range
function rootBrackets = rootBracketing(givenFunction, intervalLeft, intervalRight)
    [a, b, rootBrackets, resolution] = initializeValues(intervalLeft, intervalRight);
    rootBrackets = bracketingLoop(a, b, rootBrackets, intervalRight, resolution, givenFunction);
end

function [a, b, rootBrackets, resolution]  = initializeValues(intervalLeft, intervalRight)
    % define search resolution
    resolution = (intervalRight - intervalLeft) / 6;
    % The higher the value of denominator the less iterations will it take
    % to reach the roots, however in order to have nice graph showing those
    % brackets I will choose relatively small denominator - I have choosen
    % the smallest natural number that still generates brackets on a graph
    
    % start search at the start of the range
    a = intervalLeft;
    b = intervalLeft + resolution;
    rootBrackets = double.empty(2, 0); % initialize empty vector of size 2
end

function rootBrackets = bracketingLoop(a, b, rootBrackets, intervalRight, resolution, givenFunction)
    while b ~= intervalRight % if the bracket can't be expanded end loop
        % if the function changes sign inside the interval that means that we passed through a root that means that a bracket has been found
        if sign(givenFunction(a)) ~= sign(givenFunction(b))
            % save bracket
            rootBrackets(:, size(rootBrackets, 2) + 1) = [a, b]; % Add the new bracket to existing ones
        end
        % check next bracket
        a = b;
        b = min(a + resolution, intervalRight); 
        % Once a + resolution > intervalRight, then we will know that we
        % reached beyond the interval and we must stop
    end
end
