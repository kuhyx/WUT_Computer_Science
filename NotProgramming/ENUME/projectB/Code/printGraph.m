% graph the real roots of a function
function printGraph(taskFunction, algorithmName, algorithm, interval, rootBrackets, plotTitle)
    figure()
    grid on; % Get y values lines
    hold on; % Retain current plot when adding new plots
    title([plotTitle, algorithmName]);
    set(gca, 'XAxisLocation', 'origin'); % Set properties of current axis 
    x = interval(1):0.01:interval(2); 
    % x is a vector of values between left and right interval with every value being higher by 0.01
    y = arrayfun(taskFunction, x); % We sketch the function from task for each x
    plot(x, y);
    
    % iterate over rootBrackets and add them to the plot
    for rootBracket = rootBrackets   
        % find all zeros within the bracket using the given algorithm
        % Get all steps from the algorithm we use
        [~, steps] = algorithm(taskFunction, rootBracket(1), rootBracket(2), 1e-10);
        
        firstStepColor = [1 0 0]; % Red
        otherStepsColor = 	[0 1 0]; % Green
        % plot first steps
        scatter(steps(1, 1), steps(2, 1), [], firstStepColor); 
        text(steps(1, 1), steps(2, 1), 'firstStep', 'HorizontalAlignment', 'center', 'VerticalAlignment', 'top'); % It makes text appear neatly
        % plot other steps
        scatter(steps(1, 2:end), steps(2, 2:end), [], otherStepsColor);


            
    % print root table
    disp([plotTitle, ' (', algorithmName, ')']);
    columns = {'step', 'root', 'value at root'};
    disp(table((1:size(steps, 2))', steps(1, :)', steps(2, :)', 'VariableNames', columns));
    end
end
