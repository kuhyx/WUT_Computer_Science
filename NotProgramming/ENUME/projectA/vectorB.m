function b = vectorB(n) % We want n elements in the vector 
b = zeros(n, 1); % in order to save speed we preallocate zeros to the vector
    for i = 1 : n % We loop from first element to the last element of the vector
        if mod(i, 2) == 0 % as per problem description
            b(i, 1) = 9 / (2*i);
        else
            b(i, 1) = 0;
        end % end if
    end % end for
end % end function