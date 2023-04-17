"""
Program that optimizes Rastrigin function: file_ (x_point_value, y_point_value) =
20 + (x_point_value^2 - 10cos(2πx)) + (y_point_value^2 - 10 cos(2πy)).
Using Evolutionary Strategy (μ, λ).
"""
import sys
import os
import time
import tempfile
import cv2
import matplotlib.pyplot as plt
import numpy as np


def rastrigin(x_argument, y_argument):
    """Define the Rastrigin function"""
    return (
        20
        + x_argument**2
        - 10 * np.cos(2 * np.pi * x_argument)
        + y_argument**2
        - 10 * np.cos(2 * np.pi * y_argument)
    )


def generate(
    population,
    arguments
):
    """Run single generation"""
    # Evaluate the fitness of each individual
    fitness = np.array(
        [
            rastrigin(x_point_value, y_point_value)
            for x_point_value, y_point_value in population
        ]
    )

    # Select the top arguments["number_of_parents"] individuals
    parents = population[np.argsort(fitness)[:arguments["number_of_parents"]]]

    # Generate the next generation of lambda individuals by recombination
    children = np.concatenate(
        [
            np.random.permutation(parents)
            for i in range((arguments["size_of_population"] // arguments["number_of_parents"]) + 1)
        ]
    )
    children = children[:arguments["size_of_population"]]

    # Add mutation to the children
    mutation = np.random.normal(
        loc=0, scale=arguments["mutation_strength"], size=(arguments["size_of_population"], 2)
    )
    population = children + mutation
    return fitness, population


def evolution_strategy(
    arguments,
    no_display=False,
):
    """Define the Evolutionary Strategy (μ, λ) algorithm"""
    # Initialize the population
    print_info = []
    population = np.random.uniform(
        low=arguments["min"], high=arguments["max"], size=(arguments["size_of_population"], 2)
    )

    summary = []
    if not no_display:
        print_info.append(
            (population,
             0,
             f"""0:nop-{arguments["number_of_parents"]}:sop-{arguments["size_of_population"]}:
             ms-{arguments["mutation_strength"]}:nog-{arguments["number_of_generations"]}:
             min-max-{arguments["min"], arguments["max"]}:noo-{arguments["number_of_outputs"]}""",
             ))
    arguments["number_of_outputs"] = min(
        [arguments["number_of_outputs"] - 1, arguments["number_of_generations"]])

    # Iterate until we reach max number of generate and terminate
    for generation_number in range(1, arguments["number_of_generations"] + 1):
        fitness, population = generate(
            population, arguments)
        step = (
            arguments["number_of_generations"] // arguments["number_of_outputs"]
            if arguments["number_of_generations"] % arguments["number_of_outputs"] == 0
            else arguments["number_of_generations"] // (arguments["number_of_outputs"] - 1)
        )
        offset = arguments["number_of_generations"] % step
        if (generation_number - offset) % step == 0 and not no_display:
            print_info.append(
                (population,
                 generation_number,
                 f"""{generation_number}:nop_{arguments["number_of_parents"]}:
                 sop_{arguments["size_of_population"]}:ms_{arguments["mutation_strength"]}:
                 nog_{arguments["number_of_generations"]}:
                 min_max_{arguments["min"], arguments["max"]}:
                 noo_{arguments["number_of_outputs"]}""",
                 ))
            summary.append(population)

    # Evaluate the fitness of the final population
    fitness = np.array(
        [
            rastrigin(x_point_value, y_point_value)
            for x_point_value, y_point_value in population
        ]
    )

    # Return the best individual found
    best_idx = np.argmin(fitness)
    return (
        population[best_idx],
        fitness[best_idx],
        population,
        print_info,
        summary,
    )


def print_help():
    """Print program functionality and how to access it"""
    print(
        """
    python main.py - Default functionality optimizing
    Rastrigin function file_ (x_point_value, y_point_value) =
    20 + (x_point_value^2 - 10cos(2πx)) + (y_point_value^2 - 10 cos(2πy))
    using Evolutionary Strategy (μ, λ), using only default values
    Default values:
    arguments["number_of_parents"]=5,
    arguments["size_of_population"]=20,
    arguments["mutation_strength"]=0.1,
    arguments["number_of_generations"]=100,
    min_value=-5.12,
    max_value=5.12
    arguments["number_of_outputs"] = 100

    python main.py -h --help print this prompt
    Any of the default values an be changed using arguments:
    -nop --arguments["number_of_parents"] [number]
    -sop --arguments["size_of_population"] [number]
    -ms --arguments["mutation_strength"] [number]
    -nog --arguments["number_of_generations"] [number]
    -min --min_value [number]
    -max --max_value [number]
    -noo, --arguments["number_of_outputs"] [number]
    Those arguments can be given in any order and any argument
    which was not entered will be replaced with default value,
    Additional flags:
    -nd, --no-display (does not show the plots)
    -s, --save (if issued WILL save the files)
    exemplary use:
    python main.py -nop 5 -sop 20 -ms 0.1 -nog 100 -min -5.12 -max 5.12 -noo 100
    """
    )


def get_output_bounds(x_data, y_data):
    """Get x and y output limits for pyplot"""
    # min_size = 0.2
    min_output_size = ARGUMENTS["mutation_strength"] * 10

    xmin = min(x_data)
    xmax = max(x_data)
    ymin = min(y_data)
    ymax = max(y_data)
    x_diff = xmax - xmin
    y_diff = ymax - ymin

    if min_output_size is None:
        min_output_size = max(x_diff, y_diff)

    margin = max(x_diff, y_diff) / 5

    if x_diff < min_output_size:
        xmax += (min_output_size - x_diff) / 2
        xmin -= (min_output_size - x_diff) / 2
    if y_diff < min_output_size:
        ymax += (min_output_size - y_diff) / 2
        ymin -= (min_output_size - y_diff) / 2
    x_bounds = [xmin - margin, xmax + margin]
    y_bounds = [ymin - margin, ymax + margin]
    return x_bounds, y_bounds


def output(
        population_output,
        generation_number,
        file_name="temp",
        save_results=False):
    """Draw result of our function"""

    # define the visualization params
    colors = np.random.rand(len(population_output))

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as file_:
        # iterate over the optimization steps
        x_data = []
        y_data = []
        for x_point_value, y_point_value in population_output:
            x_data.append(x_point_value)
            y_data.append(y_point_value)

        x_lim, y_lim = get_output_bounds(x_data, y_data)

        # plot the data
        plt.cla()
        plt.figure()
        plt.scatter(x_data, y_data, c=colors, alpha=0.5)
        plt.xlim(x_lim)
        plt.ylim(y_lim)
        plt.savefig(file_.name)

        # read image
        image = cv2.imread(file_.name)

        # show the image, provide window name first
        cv2.imshow(f"Generation {generation_number}", image)
        if save_results:
            cv2.imwrite(file_name + ".jpg", image)
        # add wait key. window waits until user presses a key and quits if
        # the key is 'q'
        if cv2.waitKey(0) == 113:
            # and finally destroy/close all open windows
            sys.exit()

    cv2.destroyAllWindows()

    file_.close()
    os.unlink(file_.name)


def print_summary(populations, file_name="temp_summary", save_results=False):
    """Draw result of our function for chosen generations"""

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as file_:
        # iterate over the optimization steps
        # generate random 2D data - replace it with the results from your
        # algorithm
        plt.cla()
        plt.figure()
        bounds = None
        for ind, pop in enumerate(populations):
            x_data = []
            y_data = []
            for x_point_value, y_point_value in pop:
                x_data.append(x_point_value)
                y_data.append(y_point_value)

            if ind == 0:
                bounds = get_output_bounds(x_data, y_data)
            # plot the data
            transparency = ind / (len(populations) - 1)
            color = [[transparency, 0, 0]] * len(pop)
            plt.scatter(
                x_data,
                y_data,
                c=color,
                alpha=transparency,
                label=f"{ind}")
        plt.xlim(bounds[0])
        plt.ylim(bounds[1])
        plt.savefig(file_.name)

        # read image
        image = cv2.imread(file_.name)
        if save_results:
            cv2.imwrite("SUMMARY:" + file_name + ".jpg", image)

        # show the image, provide window name first
        cv2.imshow("Summary", image)

        # add wait key. window waits until user presses a key and quits if
        # the key is 'q'
        if cv2.waitKey(0) == 113:
            # and finally destroy/close all open windows
            sys.exit()

    cv2.destroyAllWindows()

    file_.close()
    os.unlink(file_.name)


def user_input():
    """Handle user terminal arguments"""
    arguments = {
        "number_of_parents": 5,
        "size_of_population": 20,
        "mutation_strength": 0.1,
        "number_of_generations": 100,
        "min": -5.12,
        "max": 5.12,
        "number_of_outputs": 10,
        "no_display": False,
        "save": False,
    }
    for index, argument in enumerate(sys.argv):
        if argument in ("-h", "--help"):
            print_help()
            sys.exit()
        if argument in ("-nop", "--number_of_parents"):
            arguments["number_of_parents"] = int(sys.argv[index + 1])
        if argument in ("-sop", "--size_of_population"):
            arguments["size_of_population"] = int(sys.argv[index + 1])
        if argument in ("-ms", "--mutation_strength"):
            arguments["mutation_strength"] = float(sys.argv[index + 1])
        if argument in ("-nog", "--number_of_generations"):
            arguments["number_of_generations"] = int(sys.argv[index + 1])
        if argument in ("-min", "--min_value"):
            arguments["min"] = float(sys.argv[index + 1])
        if argument in ("-max", "--max_value"):
            arguments["max"] = float(sys.argv[index + 1])
        if argument in ("-noo", "--number_of_outputs"):
            arguments["number_of_outputs"] = int(sys.argv[index + 1])
        if argument in ("-nd", "--no_display"):
            arguments["no_display"] = True
        if argument in ("-s", "--save"):
            arguments["save"] = True

    return arguments


def print_output(print_info, save_results, summary):
    """ Prints out population and summary plots """
    for population, generation_number, file_name in print_info:
        output(population, generation_number, file_name, save_results)
        summary_file_name = file_name
    print_summary(summary, summary_file_name, save_results)


# Ran first in the code
if __name__ == "__main__":
    # Run the Evolutionary Strategy algorithm
    ARGUMENTS = user_input()
    TOTAL_TIME = 0
    start_time = time.perf_counter()
    (
        best_individual,
        best_fitness,
        output_population,
        PRINT_INFO,
        SUMMARY,
    ) = evolution_strategy(
        ARGUMENTS,
        ARGUMENTS["no_display"],
    )
    end_time = time.perf_counter()
    if not ARGUMENTS["no_display"]:
        print_output(PRINT_INFO, ARGUMENTS["save"], SUMMARY)
    TOTAL_TIME = end_time - start_time
    time_per_generation = TOTAL_TIME / ARGUMENTS["number_of_generations"]

    print("Best individual found:", best_individual)
    print("Best fitness found:", best_fitness)
    print("total_generation_time: ", TOTAL_TIME)
    print("time_per_generation: ", time_per_generation)
