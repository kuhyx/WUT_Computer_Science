function A = matrix4(n)
    A = 10 * rand(n); % rand generates 5x5 matrix filled with random numbers
    % we multiply by 10 to get at lest one digit in front of the dot
    A = floor(A); % we floor the matrix we got to get nice natural numbers matrix
    A = A * A'; % we get symmetric matrix
end