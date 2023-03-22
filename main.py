"""
Write horizontal_line program that solves horizontal_line maze
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
import sys
import time
import os
from random import shuffle, randrange


class MazeSolver:
    """Maze Solver"""

    # self corresponds to "this" in js, it refers to object of MazeSolver class

    def __init__(self, maze, mode):
        # assign read maze 2D array to parameter from class MazeSolver
        self.test = mode
        self.maze = maze
        self.start, self.end = self.find_start_and_end()

    # go through each character in 2D array and find one that corresponds to
    # Start/End character

    def find_start_and_end(self):
        """Finds start and end points in the maze"""
        start = end = None

        for row_i, row in enumerate(self.maze):
            for col_i, cell in enumerate(row):
                if cell == "S":
                    start = (row_i, col_i)
                elif cell == "E":
                    end = (row_i, col_i)
                if start is not None and end is not None:
                    return start, end
        print(f"DID NOT FOUND START OR END, Start: {start}, End: {end}")
        return start, end

    # Go through each neighbor
    #       N
    #     N * N
    #       N
    # If it is not horizontal_line "wall" (#) add its position to list of neighbors

    def get_neighbors(self, position):
        """Finds point'maze_data neighbors"""
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

    def solve_loop(self, queue, visited):
        """ Goes through maze and finds the path """
        while queue:
            # pop first element of heap
            # first value is skipped and we only save current position and path
            # on heap
            _, current, path = heapq.heappop(queue)
            # if we already visited current skip code and go to next iteration
            if current in visited:
                continue
            # if we found the end return path
            if current == self.end:
                break
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    heapq.heappush(
                        queue, (self.heuristic_manhattan(neighbor), neighbor, new_path)
                    )
            if not self.test:
                print_maze(self.maze, new_path)
                print()
        return path

    def solve(self):
        """Solves the maze"""
        queue = []
        # set means that values inside can not repeat
        visited = set()
        # https://docs.python.org/3/library/heapq.html
        # push onto the queue (which becomes heapq), element containing values
        # we use heapq so the element with lowest heuristic value will always
        # be at the top of heap
        heapq.heappush(
            queue, (self.heuristic_manhattan(self.start), self.start, [self.start])
        )

        # Go through queue until it'maze_data empty
        # Find neighbor (which is not wall) closest to the
        # END point (based on heuristic)
        # Go there and repeat
        # if cannot find path it starts over but skips the path that lead it to
        # dead end
        return self.solve_loop(queue, visited)

    # This heuristic returns the Manhattan distance between the given position
    # and the maze'maze_data end
    def heuristic_manhattan(self, position):
        """Heuristic function that uses Manhattan distance"""
        return abs(position[0] - self.end[0]) + abs(position[1] - self.end[1])

    # This heuristic returns the Euclidean distance between the given position
    # and the maze'maze_data end
    def heuristic_euclidean(self, position):
        """Heuristic function that uses Euclidean distance"""
        return (
            abs(position[0] - self.end[0]) ** 2 + abs(position[1] - self.end[1]) ** 2
        ) ** 0.5


# Open and load text file to array
def load_maze(maze_file_name):
    """Loads horizontal_line maze from the specified file"""
    # Open for reading only and save to fileContents
    with open(maze_file_name, "r", encoding="utf8") as file_contents:
        # strip() removes extra white spaces from the beginning and the end of
        # horizontal_line string
        # list() changes string to array of chars
        # Inside of square brackets we will have an array of characters for
        # each line of file
        # After going through every line in horizontal_line file we will have 2D array of arrays
        # of characters of every line
        maze = [list(line.strip()) for line in file_contents]
    return maze


def print_maze(maze, path=None):
    """Prints the maze"""
    if path is None:
        path = []
    for row_i, row in enumerate(maze):
        for col_i, cell in enumerate(row):
            if (row_i, col_i) in path:
                print("*", end="")
            else:
                print(cell, end="")
        print()


def create_maze_folder(solved):
    """ Creates folder for generated or solved mazes"""
    if solved:
        folder_name = "solvedMazes"
    else:
        folder_name = "generatedMazes"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    return folder_name

def save_maze(maze, solved=True, path=None, saved_file="Maze", iteration=0):
    """Saves maze from array to txt file"""
    folder_name = create_maze_folder(solved)
    with open(f"{folder_name}/{iteration}{saved_file}", "w", encoding="utf8") as maze_file:
        if path is None:
            path = []
        for row_i, row in enumerate(maze):
            for col_i, cell in enumerate(row):
                if (row_i, col_i) in path:
                    maze_file.write("*")
                else:
                    maze_file.write(cell)
            if solved:
                maze_file.write("\n")
        if not solved:
            maze_file.write("\n")

def fill_generated_maze(hor, ver, width):
    """ Fills generated maze array from horizontal and vertical lines """
    maze_data = ""
    for horizontal_line, vertical_line in zip(hor, ver):
        maze_data += "".join(horizontal_line + ["\n"] + vertical_line + ["\n"])
    maze_data_list = list(maze_data)
    maze_data_list[3 * width + 3] = "S"
    maze_data_list[len(maze_data_list) - (3 * width + 6)] = "E"
    maze_data = "".join(maze_data_list)
    return maze_data

def make_maze(width=16, height=8):
    """ generate maze with given width and height """
    vis = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
    ver = [["#  "] * width + ["#"] for _ in range(height)] + [[]]
    hor = [["###"] * width + ["#"] for _ in range(height + 1)]

    def walk(x_coordinate, y_coordinate):
        vis[y_coordinate][x_coordinate] = 1

        neighbors = [(x_coordinate - 1, y_coordinate),
                    (x_coordinate, y_coordinate + 1),
                    (x_coordinate + 1, y_coordinate),
                    (x_coordinate, y_coordinate - 1)]
        shuffle(neighbors)
        for x_coordinate_neighbor, y_coordinate_neighbor in neighbors:
            if vis[y_coordinate_neighbor][x_coordinate_neighbor]:
                continue
            if x_coordinate_neighbor == x_coordinate:
                hor[max(y_coordinate, y_coordinate_neighbor)][x_coordinate] = "#  "
            if y_coordinate_neighbor == y_coordinate:
                ver[y_coordinate][max(x_coordinate, x_coordinate_neighbor)] = "   "
            walk(x_coordinate_neighbor, y_coordinate_neighbor)

    walk(randrange(width), randrange(height))

    return fill_generated_maze(hor, ver, width)

def print_help():
    """prints help"""
    print(
"""python main.py - run the script against default maze file
(any file named maze.txt in the code directory)

python main.py filename.txt - run the script against filename.txt file
python main.py -h --help print this prompt
python main.py -t --test non interactive (does not print steps) for testing 
different heuristics, goes through entire generatedMazes folder and
compares heuristic speed and path length
python main.py -t --test [FOLDER] non interactive (does not print steps) for testing 
different heuristics, goes through entire [FOLDER] folder and
compares heuristic speed and path length

python main.py -g --generate [NUMBER] - generates as many mazes as entered in
Number parameter and puts it in the generatedMazes folder"""
            )

def test_mode():
    """ Loads and solves multiple mazes in order to compare heuristics """
    for filename in os.listdir(FOLDER_NAME):
        filename_directory = os.path.join(FOLDER_NAME, filename)
        print(filename_directory)
        # Open and load text file to array
        loaded_maze = load_maze(filename_directory)
        # Initialize MazeSolver object with maze as parameter
        solver_test = MazeSolver(loaded_maze, TEST_MODE)
        # Find path using MazeSolver solve method
        solved_path = solver_test.solve()
        save_maze(loaded_maze, True, solved_path, filename, 0)

def default():
    """ Runs default operation - reads, solves and prints single maze from file """
    # Open and load text file to array
    loaded_maze = load_maze(FILE_NAME)
    # Initialize MazeSolver object with maze as parameter
    solver = MazeSolver(loaded_maze, TEST_MODE)
    # Find path using MazeSolver solve method
    solved_path = solver.solve()
    print_maze(loaded_maze, solved_path)
    save_maze(loaded_maze, True, solved_path, FILE_NAME, 0)

# Ran first in the code
if __name__ == "__main__":
    start_time = time.perf_counter()
    # print(sys.argv)
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
            if len(sys.argv) > 2:
                FOLDER_NAME = sys.argv[2]
            test_mode()
            sys.exit()
        if sys.argv[1] == '-g' or sys.argv[1] == '--generate':
            if len(sys.argv) > 2:
                GENERATE_AMOUNT = int(sys.argv[2])
                for n in range(GENERATE_AMOUNT):
                    GENERATED_MAZE = make_maze()
                    save_maze(GENERATED_MAZE, False, None, f'generated{n}.txt')
                    sys.exit()
        FILE_NAME = sys.argv[1]
    default()
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The execution time is: {execution_time}")
