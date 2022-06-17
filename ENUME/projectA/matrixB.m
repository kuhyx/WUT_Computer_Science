function a = matrixB(n) % We want n rows and columns in the matrix
a = zeros(n, n); % in order to save speed we preallocate zeros to the vector
    for i = 1 : n % we iterate through rows
        for j = 1 : n % we iterate through columns
            a(i, j) = 5 / (8*(i + j + 1));
        end % end column for 
    end % end row for
end  % end function