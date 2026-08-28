#!/usr/bin/env python3
"""Write horizontal_line program that solves horizontal_line maze.

using greedy best-first search algorithm.
The maze is horizontal_line 2D grid
with empty space, walls, horizontal_line start, and an end position.
The objective is to find horizontal_line path from start to end position.
The maze should be loaded from file. horizontal_line step-by-step visualization of the
algorithm is required. It can be done in the console and an interface may be
as simple as possible (but of course it does not have to). Example solution:
https://angeluriot.com/maze_solver/.
Test multiple heuristics (at least two) h(n) and discuss the differences be-
tween the obtained results.

Technical requirements:
- implemented in Python.
- adheres to basic standards of lean coding in accordance to PEP8
- comments in the crucial parts to help with readability and understanding.
- The clear instruction how to run and test the code should be included.

Thinks that do not work:
Does not work if no Start (Should print out NO START FOUND)
Does not work if no End   (Should print out NO END FOUND)
Does not work if no path  (Should print out NO PATH FOUND)
"""

import heapq
import logging
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# argv[0] is the program, argv[1] the mode; anything beyond that is options.
ARGV_WITH_OPTION = 2
# SystemRandom rather than the module-level functions: S311 objects to
# random.* being used where a CSPRNG is expected, and this costs nothing.
_RANDOM = random.SystemRandom()
logger = logging.getLogger(__name__)


class MazeSolver:
    """Maze Solver."""

    # self corresponds to "this" in js, it refers to object of MazeSolver class

    def __init__(self, maze: str, mode: str) -> None:
        # assign read maze 2D array to parameter from class MazeSolver
        """Set up the solver for one maze and one heuristic mode."""
        self.test = mode
        self.maze = maze
        self.start, self.end = self.find_start_and_end()

    # go through each character in 2D array and find one that corresponds to
    # Start/End character

    def find_start_and_end(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Find start and end points in the maze."""
        start = end = None

        for row_i, row in enumerate(self.maze):
            for col_i, cell in enumerate(row):
                if cell == "S":
                    start = (row_i, col_i)
                elif cell == "E":
                    end = (row_i, col_i)
                if start is not None and end is not None:
                    return start, end
        logger.info("DID NOT FOUND START OR END, Start: %s, End: %s", start, end)
        return start, end

    # Go through each neighbor
    #       N
    #     N * N
    #       N
    # If it is not horizontal_line "wall" (#) add its position to list of neighbors

    def get_neighbors(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """Find point'maze_data neighbors."""
        row, col = position
        neighbors = []
        if row > 0 and self.maze[row - 1][col] != "#":
            neighbors.append((row - 1, col))
        if col > 0 and self.maze[row][col - 1] != "#":
            neighbors.append((row, col - 1))
        if row < len(self.maze) - 1 and self.maze[row + 1][col] != "#":
            neighbors.append((row + 1, col))
        if col < len(self.maze[row]) - 1 and self.maze[row][col + 1] != "#":
            neighbors.append((row, col + 1))
        return neighbors

    # find path through maze

    def solve_loop(
        self, queue: list[object], visited: set[tuple[int, int]]
    ) -> tuple[list[tuple[int, int]], set[tuple[int, int]], float]:
        """Go through maze and finds the path."""
        heuristic_total_time = 0
        heuristics_called = 0
        while queue:
            # pop first element of heap
            # first value is skipped and we only save current position and path
            # on heap
            _, current, path = heapq.heappop(queue)
            if current in visited:
                continue
            if current == self.end:
                break
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    new_path = [*path, neighbor]
                    heuristic, heuristic_time = self.heuristic_euclidean(neighbor)
                    heuristic_total_time += heuristic_time
                    heuristics_called += 1
                    heapq.heappush(queue, (heuristic, neighbor, new_path))
            if not self.test:
                print_maze(self.maze, path, visited)
                logger.info("")
        return path, visited, heuristic_total_time, heuristics_called

    def solve(self) -> tuple[list[tuple[int, int]], set[tuple[int, int]], float]:
        """Solves the maze."""
        queue = []
        # set means that values inside can not repeat
        visited = set()
        # https://docs.python.org/3/library/heapq.html
        # push onto the queue (which becomes heapq), element containing values
        # we use heapq so the element with lowest heuristic value will always
        # be at the top of heap
        heuristic = self.heuristic_euclidean(self.start)
        heapq.heappush(queue, (heuristic, self.start, [self.start]))

        # Go through queue until it'maze_data empty
        # Find neighbor (which is not wall) closest to the
        # END point (based on heuristic)
        # Go there and repeat
        # dead end
        return self.solve_loop(queue, visited)

    # This heuristic returns the Manhattan distance between the given position
    # and the maze'maze_data end
    def heuristic_manhattan(self, position: tuple[int, int]) -> tuple[float, float]:
        """Heuristic function that uses Manhattan distance."""
        start_time = time.perf_counter()
        heuristic = abs(position[0] - self.end[0]) + abs(position[1] - self.end[1])
        end_time = time.perf_counter()
        heuristic_time = end_time - start_time
        return heuristic, heuristic_time

    # This heuristic returns the Euclidean distance between the given position
    # and the maze'maze_data end
    def heuristic_euclidean(self, position: tuple[int, int]) -> tuple[float, float]:
        """Heuristic function that uses Euclidean distance."""
        start_time = time.perf_counter()
        heuristic = (
            abs(position[0] - self.end[0]) ** 2 + abs(position[1] - self.end[1]) ** 2
        ) ** 0.5
        end_time = time.perf_counter()
        heuristic_time = end_time - start_time
        return heuristic, heuristic_time

    def heuristic_random(self, _position: tuple[int, int]) -> tuple[float, float]:
        """Heuristic function that just returns random value between 0 and 1."""
        start_time = time.perf_counter()
        heuristic = _RANDOM.random()
        end_time = time.perf_counter()
        heuristic_time = end_time - start_time
        return heuristic, heuristic_time


# Open and load text file to array
def load_maze(maze_file_name: str) -> list[str]:
    """Load horizontal_line maze from the specified file."""
    # Open for reading only and save to fileContents
    with Path(maze_file_name).open(encoding="utf8") as file_contents:
        # strip() removes extra white spaces from the beginning and the end of
        # horizontal_line string
        # list() changes string to array of chars
        # Inside of square brackets we will have an array of characters for
        # each line of file
        # After going through every line in horizontal_line file we will have 2D array
        # of arrays
        # of characters of every line
        return [list(line.strip()) for line in file_contents]


def print_maze(
    maze: list[str],
    path: list[tuple[int, int]] | None = None,
    visited: set[tuple[int, int]] | None = None,
) -> None:
    """Print the maze."""
    if path is None:
        path = []
    if visited is None:
        visited = []
    for row_i, row in enumerate(maze):
        for col_i, cell in enumerate(row):
            if (row_i, col_i) in path and cell == " ":
                sys.stdout.write("*")
            elif (row_i, col_i) in visited and cell == " ":
                sys.stdout.write("·")
            else:
                sys.stdout.write(cell)
        sys.stdout.write("\n")


def create_maze_folder(*, solved: bool) -> str:
    """Create folder for generated or solved mazes."""
    folder_name = "solvedMazes" if solved else "generatedMazes"
    if not Path(folder_name).exists():
        Path(folder_name).mkdir()
    return folder_name


@dataclass(frozen=True)
class SaveOptions:
    """Where a maze render goes, and whether it is a solved one."""

    saved_file: str = "Maze"
    iteration: int = 0
    solved: bool = True


def save_maze(
    maze: list[str],
    path: list[tuple[int, int]] | None = None,
    visited: set[tuple[int, int]] | None = None,
    options: SaveOptions | None = None,
) -> None:
    """Save maze from array to txt file."""
    if options is None:
        options = SaveOptions()
    saved_file, iteration, solved = (
        options.saved_file,
        options.iteration,
        options.solved,
    )
    folder_name = create_maze_folder(solved=solved)
    if path is None:
        path = []
    if visited is None:
        visited = []
    with Path(f"{folder_name}/{iteration}{Path(saved_file).name}").open(
        "w", encoding="utf8"
    ) as maze_file:
        for row_i, row in enumerate(maze):
            for col_i, cell in enumerate(row):
                if (row_i, col_i) in path and cell == " ":
                    maze_file.write("*")
                elif (row_i, col_i) in visited and cell == " ":
                    maze_file.write("·")
                else:
                    maze_file.write(cell)
            if solved:
                maze_file.write("\n")
        if not solved:
            maze_file.write("\n")


def fill_generated_maze(hor: list[list[str]], ver: list[list[str]], width: int) -> str:
    """Fill the generated maze array from its horizontal and vertical lines."""
    maze_data = ""
    for horizontal_line, vertical_line in zip(hor, ver, strict=False):
        maze_data += "".join([*horizontal_line, "\n", *vertical_line, "\n"])
    maze_data_list = list(maze_data)
    maze_data_list[3 * width + 3] = "S"
    maze_data_list[len(maze_data_list) - (3 * width + 6)] = "E"
    return "".join(maze_data_list)


def make_maze(width: int = 16, height: int = 8) -> str:
    """Generate maze with given width and height."""
    vis = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
    ver = [["#  "] * width + ["#"] for _ in range(height)] + [[]]
    hor = [["###"] * width + ["#"] for _ in range(height + 1)]

    def walk(x_coordinate: int, y_coordinate: int) -> None:
        vis[y_coordinate][x_coordinate] = 1

        neighbors = [
            (x_coordinate - 1, y_coordinate),
            (x_coordinate, y_coordinate + 1),
            (x_coordinate + 1, y_coordinate),
            (x_coordinate, y_coordinate - 1),
        ]
        _RANDOM.shuffle(neighbors)
        for x_coordinate_neighbor, y_coordinate_neighbor in neighbors:
            if vis[y_coordinate_neighbor][x_coordinate_neighbor]:
                continue
            if x_coordinate_neighbor == x_coordinate:
                hor[max(y_coordinate, y_coordinate_neighbor)][x_coordinate] = "#  "
            if y_coordinate_neighbor == y_coordinate:
                ver[y_coordinate][max(x_coordinate, x_coordinate_neighbor)] = "   "
            walk(x_coordinate_neighbor, y_coordinate_neighbor)

    walk(_RANDOM.randrange(width), _RANDOM.randrange(height))

    return fill_generated_maze(hor, ver, width)


def print_help() -> None:
    """Print help."""
    logger.info(
        "python main.py - run the script against default maze file\n(any file "
        "named maze.txt in the code directory)\n\npython main.py filename.txt - "
        "run the script against filename.txt file\npython main.py -h --help print"
        " this prompt\npython main.py -t --test non interactive (does not print "
        "steps) for testing\ndifferent heuristics, goes through entire "
        "generatedMazes folder and\ncompares heuristic speed and path length\n"
        "python main.py -t --test [FOLDER] non interactive (does not print steps)"
        " for testing\ndifferent heuristics, goes through entire [FOLDER] folder "
        "and\ncompares heuristic speed and path length\n\npython main.py -g "
        "--generate [NUMBER] - generates as many mazes as entered in\nNumber "
        "parameter and puts it in the generatedMazes folder"
    )


def test_mode() -> None:
    """Load and solves multiple mazes in order to compare heuristics."""
    create_maze_folder(solved=False)
    sum_of_paths = 0
    files_amount = 0
    sum_of_time = 0
    heuristic_total_total_time = 0
    all_heuristic_called = 0
    for filename in [q.name for q in Path(FOLDER_NAME).iterdir()]:
        filename_directory = str(Path(FOLDER_NAME) / filename)
        # Open and load text file to array
        loaded_maze = load_maze(filename_directory)
        # Initialize MazeSolver object with maze as parameter
        solver_test = MazeSolver(loaded_maze, TEST_MODE)
        # Find path using MazeSolver solve method
        start_time = time.perf_counter()
        solved_path, visited, heuristic_total_time, heuristics_called = (
            solver_test.solve()
        )
        heuristic_total_total_time += heuristic_total_time
        all_heuristic_called += heuristics_called
        end_time = time.perf_counter()
        sum_of_time += end_time - start_time
        sum_of_paths += len(solved_path)
        save_maze(
            loaded_maze, solved_path, visited, SaveOptions(filename, 0, solved=True)
        )
        files_amount += 1
    if files_amount == 0:
        logger.info("no mazes found! Generate some using python main.py -g [NUMBER]")
        sys.exit()
    average_path = sum_of_paths / files_amount
    average_time = sum_of_time / files_amount
    logger.info(
        "For: %s files,\n    sum of path lengths = %s,\n    average path length ="
        " %s,\n    sum_of_time = %s,\n    average time to solve: %s,\n    "
        "heuristic_total_total_time: %s,\n    all_heuristic_called: %s,\n    "
        "average_heuristic_time: %s",
        files_amount,
        sum_of_paths,
        average_path,
        sum_of_time,
        average_time,
        heuristic_total_total_time,
        all_heuristic_called,
        heuristic_total_total_time / all_heuristic_called,
    )


def default() -> None:
    """Run default operation - reads, solves and prints single maze from file."""
    # Open and load text file to array
    loaded_maze = load_maze(FILE_NAME)
    # Initialize MazeSolver object with maze as parameter
    solver = MazeSolver(loaded_maze, TEST_MODE)
    # Find path using MazeSolver solve method
    solved_path, visited, _, _ = solver.solve()
    print_maze(loaded_maze, solved_path, visited)
    save_maze(loaded_maze, solved_path, visited, SaveOptions(FILE_NAME, 0, solved=True))


# Ran first in the code
if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    FILE_NAME = "maze.txt"
    TEST_MODE = False
    FOLDER_NAME = ""
    GENERATE_AMOUNT = 0
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
            sys.exit()
        if sys.argv[1] == "-t" or sys.argv[1] == "--test":
            TEST_MODE = True
            FILE_NAME = "maze.txt"
            FOLDER_NAME = "generatedMazes"
            if len(sys.argv) > ARGV_WITH_OPTION:
                FOLDER_NAME = sys.argv[2]
            test_mode()
            sys.exit()
        if sys.argv[1] in ("-g", "--generate") and len(sys.argv) > ARGV_WITH_OPTION:
            GENERATE_AMOUNT = int(sys.argv[2])
            for n in range(GENERATE_AMOUNT):
                GENERATED_MAZE = make_maze()
                save_maze(
                    GENERATED_MAZE,
                    None,
                    None,
                    SaveOptions(f"generated{n}.txt", 0, solved=False),
                )
            sys.exit()
        FILE_NAME = sys.argv[1]
    default()
