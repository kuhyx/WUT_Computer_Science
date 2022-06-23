function a = matrixA(n) % We want n rows and columns in the matrix
a = zeros(n, n); % in order to save speed we preallocate zeros to the vector
    for i = 1 : n % we iterate through rows
        for j = 1 : n % we iterate through columns
            if i == j % as per problem description on how to fill the matrix
                a(i, j) = 9;
            elseif i == j - 1 || i == j + 1
                a(i, j) = -3;
            else
                a(i, j) = 0;
            end % end if
        end % end column for 
    end % end row for
end  % end function