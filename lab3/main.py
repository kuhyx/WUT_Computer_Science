"""
Program that optimizes Rastrigin function: f (x, y) = 
20 + (x^2 - 10cos(2πx)) + (y^2 - 10 cos(2πy)).
Using Evolutionary Strategy (μ, λ).
"""
import numpy as np


def rastrigin(x_argument, y_argument):
    """ Define the Rastrigin function """
    return 20 + x_argument**2 - 10 * np.cos(2 * np.pi * x_argument) + \
        y_argument**2 - 10 * np.cos(2 * np.pi * y_argument)


def evolution_strategy(top_individuals, lambda_, sigma, iterations):
    """ Define the Evolutionary Strategy (μ, λ) algorithm """
    # Initialize the population
    population = np.random.uniform(low=-5.12, high=5.12, size=(lambda_, 2))

    # Iterate for a fixed number of iterations
    for i in range(iterations):
        # Evaluate the fitness of each individual
        fitness = np.array([rastrigin(x, y) for x, y in population])

        # Select the top top_individuals individuals
        parents = population[np.argsort(fitness)[:top_individuals]]

        # Generate the next generation of lambda individuals by recombination
        children = np.concatenate(
            [np.random.permutation(parents) for i in range(lambda_ // top_individuals)])

        # Add mutation to the children
        mutation = np.random.normal(loc=0, scale=sigma, size=(lambda_, 2))
        population = children + mutation

    # Evaluate the fitness of the final population
    fitness = np.array([rastrigin(x, y) for x, y in population])

    # Return the best individual found
    best_idx = np.argmin(fitness)
    return population[best_idx], fitness[best_idx]


# Ran first in the code
if __name__ == "__main__":
    # Set the parameters
    MU = 5
    LAMBDA = 20
    SIGMA = 0.1
    ITERATIONS = 100

    # Run the Evolutionary Strategy algorithm
    best_individual, best_fitness = evolution_strategy(
        MU, LAMBDA, SIGMA, ITERATIONS)

    print("Best individual found:", best_individual)
    print("Best fitness found:", best_fitness)
