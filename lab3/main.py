"""
Program that optimizes Rastrigin function: file_ (x_point_value, y_point_value) =
20 + (x_point_value^2 - 10cos(2πx)) + (y_point_value^2 - 10 cos(2πy)).
Using Evolutionary Strategy (μ, λ).
"""
import sys
import time
import tempfile
from cv2 import cv2
import matplotlib.pyplot as plt
import numpy as np


def rastrigin(x_argument, y_argument):
    """ Define the Rastrigin function """
    return 20 + x_argument**2 - 10 * np.cos(2 * np.pi * x_argument) + \
        y_argument**2 - 10 * np.cos(2 * np.pi * y_argument)


def generate(generation_number,
             population,
             number_of_parents=5,
             size_of_population=20,
             mutation_strength=0.1,
             ):
    """ Run single generation """
    # Evaluate the fitness of each individual
    fitness = np.array([rastrigin(x_point_value, y_point_value)
                       for x_point_value, y_point_value in population])

    # Select the top number_of_parents individuals
    parents = population[np.argsort(fitness)[:number_of_parents]]

    # Generate the next generation of lambda individuals by recombination
    children = np.concatenate([np.random.permutation(
        parents) for generation_number in range(size_of_population // number_of_parents)])

    # Add mutation to the children
    mutation = np.random.normal(
        loc=0, scale=mutation_strength, size=(
            size_of_population, 2))
    population = children + mutation
    return fitness, population


def evolution_strategy(
        number_of_parents=5,
        size_of_population=20,
        mutation_strength=0.1,
        number_of_generations=100,
        min_max=(-5.12, 5.12)
):
    """ Define the Evolutionary Strategy (μ, λ) algorithm """
    # Initialize the population
    population = np.random.uniform(
        low=min_max[0], high=min_max[1], size=(
            size_of_population, 2))

    # Iterate untill we reach max number of generate and terminate
    for generation_number in range(number_of_generations):
        fitness, population = generate(
            generation_number,
            population,
            number_of_parents,
            size_of_population,
            mutation_strength)

    # Evaluate the fitness of the final population
    fitness = np.array([rastrigin(x_point_value, y_point_value)
                       for x_point_value, y_point_value in population])

    # Return the best individual found
    best_idx = np.argmin(fitness)
    return population[best_idx], fitness[best_idx], population


def print_help():
    """ Print program functionality and how to access it """
    print("""
    python main.py - Default functionality optimizing Rastrigin function file_ (x_point_value, y_point_value) =
    20 + (x_point_value^2 - 10cos(2πx)) + (y_point_value^2 - 10 cos(2πy))
    using Evolutionary Strategy (μ, λ), using only default values
    Default values:
    number_of_parents=5,
    size_of_population=20,
    mutation_strength=0.1,
    number_of_generations=100,
    min_value=-5.12,
    max_value=5.12

    python main.py -h --help print this prompt
    Any of the default values an be changed using arguments:
    -nop --number_of_parents [number]
    -sop --size_of_population [number]
    -ms --mutation_strength [number]
    -nog --number_of_generations [number]
    -min --min_value [number]
    -max --max_value [number]
    Those arguments can be given in any order and any argument which was not entered will be replaced with default value,
    exemplary use:
    python main.py -nop 5 -sop 20 -s 0.1 -i 100 -min -5.12 -max 5.12
    """)


def output(population_output):
    """ Draw result of our function """
    # define number of data points
    output_length = len(population_output)
    # define the visualization params
    colors = np.random.rand(output_length)

    with tempfile.NamedTemporaryFile(suffix=".png") as file_:
        # iterate over the optimization steps
        # generate random 2D data - replace it with the results from your
        # algorithm
        print(population_output)
        x_data = []
        y_data = []
        for x_point_value, y_point_value in population_output:
            x_data.append(x_point_value)
            y_data.append(y_point_value)
        print("x_data", x_data)
        # plot the data
        plt.cla()
        plt.figure()
        plt.scatter(x_data, y_data, c=colors, alpha=0.5)
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.savefig(file_.name)

        # read image
        image = cv2.imread(file_.name)

        # show the image, provide window name first
        cv2.imshow('visualization', image)

        # add wait key. window waits until user presses a key and quits if
        # the key is 'q'
        if cv2.waitKey(0) == 113:
            # and finally destroy/close all open windows
            sys.exit()

    cv2.destroyAllWindows()


def user_input():
    """ Handle user terminal arguments"""
    arguments = {
        "number_of_parents": 5,
        "size_of_population": 20,
        "mutation_strength": 0.1,
        "number_of_generations": 100,
        "min": -5.12,
        "max": 5.12}
    for argument in enumerate(sys.argv):
        if argument in ('-h', '--help'):
            print_help()
            sys.exit()
        if argument in ('-nop', '--number_of_parents'):
            arguments["number_of_parents"] = float(argument)
        if argument in ('-sop', '--size_of_population'):
            arguments["size_of_population"] = float(argument)
        if argument in ('-ms', '--mutation_strength'):
            arguments["mutation_strength"] = float(argument)
        if argument in ('-nog', '--number_of_generations'):
            arguments["number_of_generations"] = float(argument)
        if argument in ('-min', '--min_value'):
            arguments["min"] = float(argument)
        if argument in ('-max', '--max_value'):
            arguments["max"] = float(argument)

    return arguments


# Ran first in the code
if __name__ == "__main__":
    # Run the Evolutionary Strategy algorithm
    ARGUMENTS = user_input()
    start_time = time.perf_counter()
    best_individual, best_fitness, output_population = evolution_strategy(
        ARGUMENTS["number_of_parents"],
        ARGUMENTS["size_of_population"],
        ARGUMENTS["mutation_strength"],
        ARGUMENTS["number_of_generations"],
        (ARGUMENTS["min"], ARGUMENTS["max"]))
    end_time = time.perf_counter()
    total_generation_time = end_time - start_time
    time_per_generation = total_generation_time / \
        ARGUMENTS["number_of_generations"]

    print("Best individual found:", best_individual)
    print("Best fitness found:", best_fitness)
    print("total_generation_time: ", total_generation_time)
    print("time_per_generation: ", time_per_generation)
    output(output_population)
