function Phi = RK4Phi(algorithm, stepValue, stepSize)
    k1 = algorithm(stepValue);
    k2 = algorithm(stepValue + 0.5 * stepSize * k1);
    k3 = algorithm(stepValue + 0.5 * stepSize * k2);
    k4 = algorithm(stepValue + stepSize * k3);
    Phi = (k1 + 2 * k2 + 2 * k3 + k4) / 6;
end
% calculates the Phi used in RK4 algorithms
