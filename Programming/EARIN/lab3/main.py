#!/usr/bin/env python3
"""Program that optimizes Rastrigin function: file_ (x_point_value, y_point_value) =.

20 + (x_point_value^2 - 10cos(2πx)) + (y_point_value^2 - 10 cos(2πy)).
Using Evolutionary Strategy (μ, λ).
"""

import logging
import sys
import tempfile
import time
from collections.abc import Callable
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

# cv2.waitKey returns the ASCII code of the key pressed; 'q' quits.
KEY_Q = ord("q")
# NumPy's legacy np.random.* functions share one global state; Generator is
# the modern API and is what NPY002 asks for.
RNG = np.random.default_rng()
logger = logging.getLogger(__name__)


def rastrigin(x_argument: float, y_argument: float) -> float:
    """Define the Rastrigin function."""
    return (
        20
        + x_argument**2
        - 10 * np.cos(2 * np.pi * x_argument)
        + y_argument**2
        - 10 * np.cos(2 * np.pi * y_argument)
    )


def generate(population: object, arguments: dict[str, float]) -> tuple[object, object]:
    """Run single generation."""
    # Evaluate the fitness of each individual
    fitness = np.array(
        [
            rastrigin(x_point_value, y_point_value)
            for x_point_value, y_point_value in population
        ]
    )

    # Select the top arguments["number_of_parents"] individuals
    parents = population[np.argsort(fitness)[: arguments["number_of_parents"]]]

    # Generate the next generation of lambda individuals by recombination
    children = np.concatenate(
        [
            RNG.permutation(parents)
            for i in range(
                (arguments["size_of_population"] // arguments["number_of_parents"]) + 1
            )
        ]
    )
    children = children[: arguments["size_of_population"]]

    # Add mutation to the children
    mutation = RNG.normal(
        loc=0,
        scale=arguments["mutation_strength"],
        size=(arguments["size_of_population"], 2),
    )
    population = children + mutation
    return fitness, population


def evolution_strategy(
    arguments: dict[str, float], *, no_display: bool = False
) -> tuple[object, object]:
    """Define the Evolutionary Strategy (μ, λ) algorithm."""
    # Initialize the population
    print_info = []
    population = RNG.uniform(
        low=arguments["min"],
        high=arguments["max"],
        size=(arguments["size_of_population"], 2),
    )

    summary = []
    if not no_display:
        print_info.append(
            (
                population,
                0,
                f"""0:nop-{arguments["number_of_parents"]}:sop-{arguments["size_of_population"]}:
             ms-{arguments["mutation_strength"]}:nog-{arguments["number_of_generations"]}:
             min-max-{arguments["min"], arguments["max"]}:
             noo-{arguments["number_of_outputs"]}""",
            )
        )
    arguments["number_of_outputs"] = min(
        [arguments["number_of_outputs"] - 1, arguments["number_of_generations"]]
    )

    # Iterate until we reach max number of generate and terminate
    for generation_number in range(1, arguments["number_of_generations"] + 1):
        fitness, population = generate(population, arguments)
        step = (
            arguments["number_of_generations"] // arguments["number_of_outputs"]
            if arguments["number_of_generations"] % arguments["number_of_outputs"] == 0
            else arguments["number_of_generations"]
            // (arguments["number_of_outputs"] - 1)
        )
        offset = arguments["number_of_generations"] % step
        if (generation_number - offset) % step == 0 and not no_display:
            print_info.append(
                (
                    population,
                    generation_number,
                    f"""{generation_number}:nop_{arguments["number_of_parents"]}:
                 sop_{arguments["size_of_population"]}:ms_{arguments["mutation_strength"]}:
                 nog_{arguments["number_of_generations"]}:
                 min_max_{arguments["min"], arguments["max"]}:
                 noo_{arguments["number_of_outputs"]}""",
                )
            )
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


def print_help() -> None:
    """Print program functionality and how to access it."""
    logger.info(
        "\n    python main.py - Default functionality optimizing\n    Rastrigin "
        "function file_ (x_point_value, y_point_value) =\n    20 + "
        "(x_point_value^2 - 10cos(2πx)) + (y_point_value^2 - 10 cos(2πy))\n    "
        "using Evolutionary Strategy (μ, λ), using only default values\n    "
        'Default values:\n    arguments["number_of_parents"]=5,\n    '
        'arguments["size_of_population"]=20,\n    '
        'arguments["mutation_strength"]=0.1,\n    '
        'arguments["number_of_generations"]=100,\n    min_value=-5.12,\n    '
        'max_value=5.12\n    arguments["number_of_outputs"] = 100\n\n    python '
        "main.py -h --help print this prompt\n    Any of the default values an be"
        ' changed using arguments:\n    -nop --arguments["number_of_parents"] '
        '[number]\n    -sop --arguments["size_of_population"] [number]\n    -ms '
        '--arguments["mutation_strength"] [number]\n    -nog '
        '--arguments["number_of_generations"] [number]\n    -min --min_value '
        "[number]\n    -max --max_value [number]\n    -noo, "
        '--arguments["number_of_outputs"] [number]\n    Those arguments can be '
        "given in any order and any argument\n    which was not entered will be "
        "replaced with default value,\n    Additional flags:\n    -nd, "
        "--no-display (does not show the plots)\n    -s, --save (if issued WILL "
        "save the files)\n    exemplary use:\n    python main.py -nop 5 -sop 20 "
        "-ms 0.1 -nog 100 -min -5.12 -max 5.12 -noo 100\n    "
    )


def get_output_bounds(
    x_data: object, y_data: object
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Get x and y output limits for pyplot."""
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
    population_output: object,
    generation_number: int,
    file_name: str = "temp",
    *,
    save_results: bool = False,
) -> None:
    """Draw result of our function."""
    # define the visualization params
    colors = RNG.random(len(population_output))

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
        if cv2.waitKey(0) == KEY_Q:
            # and finally destroy/close all open windows
            sys.exit()

    cv2.destroyAllWindows()

    file_.close()
    Path(file_.name).unlink()


def print_summary(
    populations: object, file_name: str = "temp_summary", *, save_results: bool = False
) -> None:
    """Draw result of our function for chosen generations."""
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
            plt.scatter(x_data, y_data, c=color, alpha=transparency, label=f"{ind}")
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
        if cv2.waitKey(0) == KEY_Q:
            # and finally destroy/close all open windows
            sys.exit()

    cv2.destroyAllWindows()

    file_.close()
    Path(file_.name).unlink()


# Long option, short option, and how to read the value that follows. A table
# rather than an if-ladder: the ladder was C901 12, and one row per flag makes
# adding one a data change.
_OPTIONS: dict[tuple[str, str], tuple[str, Callable[[str], float] | None]] = {
    ("-nop", "--number_of_parents"): ("number_of_parents", int),
    ("-sop", "--size_of_population"): ("size_of_population", int),
    ("-ms", "--mutation_strength"): ("mutation_strength", float),
    ("-nog", "--number_of_generations"): ("number_of_generations", int),
    ("-min", "--min_value"): ("min", float),
    ("-max", "--max_value"): ("max", float),
    ("-noo", "--number_of_outputs"): ("number_of_outputs", int),
    ("-nd", "--no_display"): ("no_display", None),
    ("-s", "--save"): ("save", None),
}


def user_input() -> dict[str, float]:
    """Handle user terminal arguments."""
    arguments: dict[str, float] = {
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
        for flags, (key, parse) in _OPTIONS.items():
            if argument in flags:
                arguments[key] = True if parse is None else parse(sys.argv[index + 1])

    return arguments


def print_output(print_info: object, save_results: object, summary: object) -> None:
    """Print out population and summary plots."""
    for population, generation_number, file_name in print_info:
        output(population, generation_number, file_name, save_results=save_results)
        summary_file_name = file_name
    print_summary(summary, summary_file_name, save_results=save_results)


# Ran first in the code
if __name__ == "__main__":
    # Run the Evolutionary Strategy algorithm
    logging.basicConfig(format="%(message)s", level=logging.INFO)
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
        no_display=bool(ARGUMENTS["no_display"]),
    )
    end_time = time.perf_counter()
    if not ARGUMENTS["no_display"]:
        print_output(PRINT_INFO, ARGUMENTS["save"], SUMMARY)
    TOTAL_TIME = end_time - start_time
    time_per_generation = TOTAL_TIME / ARGUMENTS["number_of_generations"]

    logger.info("Best individual found: %s", best_individual)
    logger.info("Best fitness found: %s", best_fitness)
    logger.info("total_generation_time:  %s", TOTAL_TIME)
    logger.info("time_per_generation:  %s", time_per_generation)
