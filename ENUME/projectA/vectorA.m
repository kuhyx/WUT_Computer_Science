function b = vectorA(n) % We want n elements in the vector 
b = zeros(n, 1); % in order to save speed we preallocate zeros to the vector
    for i = 1 : n % We loop from first element to the last element of the vector
        b(i, 1) = -5 + 0.3 * i; % Formula as in the task description
        % We need to put '1' in b(i, 1) so that matlab acknowledges that
        % this is a column and not a row
    end % end for
end % end function