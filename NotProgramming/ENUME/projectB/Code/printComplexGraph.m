% graph the complex roots of a function
function printComplexGraph(printComplexGraph, algorithmName, algorithm, rootBrackets, plottitle)
    figure();
    grid on; % Get y values lines
    hold on; % Retain current plot when adding new plots
    title([plottitle, algorithmName]);
    xlabel("Real part");
    ylabel("Imaginary part");
    set(gca, 'XAxisLocation', 'origin'); % Set properties of current axis 
    
    % find all zeros within the bracket using the given algorithm
    [~, steps] = algorithm(printComplexGraph, rootBrackets(1), rootBrackets(2), 1e-15);
    
    % plot first step
    text(real(steps(1, 1)), imag(steps(1, 1)), 'start', 'HorizontalAlignment', 'center', 'VerticalAlignment', 'top');

    % plot steps on graph
    plot(real(steps(1, :)), imag(steps(1, :)), '-x');
    
    % plot last step
    text(real(steps(1, end)), imag(steps(1, end)), 'end', 'HorizontalAlignment', 'center', 'VerticalAlignment', 'top');

    
    % print root table
    disp([plottitle, ' (', algorithmName, ')']);
    columns = {'step', 'root', 'abs value at root'};
    disp(table([1:size(steps, 2)]', steps(1, :)', abs(steps(2, :))', 'VariableNames', columns));
end
