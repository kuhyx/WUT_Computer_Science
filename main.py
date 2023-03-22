"""
Write a program that solves a maze using greedy best-first search algorithm.
The maze is a 2D grid with empty space, walls, a start, and an end position.
The objective is to find a path from start to end position.
The maze should be loaded from file. A step-by-step visualization of the
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


class MazeSolver:
    '''Maze Solver'''
    # self corresponds to "this" in js, it refers to object of MazeSolver class

    def __init__(self, maze, test_mode):
        # assign read maze 2D array to parameter from class MazeSolver
        self.test = test_mode
        self.maze = maze
        self.start, self.end = self.find_start_and_end()

# go through each character in 2D array and find one that corresponds to
# Start/End character

    def find_start_and_end(self):
        '''Finds start and end points in the maze'''
        start = end = None

        for row_i, row in enumerate(self.maze):
            for col_i, cell in enumerate(row):
                if cell == 'S':
                    start = (row_i, col_i)
                elif cell == 'E':
                    end = (row_i, col_i)
                if start is not None and end is not None:
                    return start, end
        print(f"DID NOT FOUND START OR END, Start: {start}, End: {end}")
        return start, end

# Go through each neighbor
#       N
#     N * N
#       N
# If it is not a "wall" (#) add its position to list of neighbors

    def get_neighbors(self, position):
        '''Finds point's neighbors'''
        row, col = position
        neighbors = []
        if row > 0 and self.maze[row - 1][col] != '#':
            neighbors.append((row - 1, col))
        if col > 0 and self.maze[row][col - 1] != '#':
            neighbors.append((row, col - 1))
        if row < len(self.maze) - 1 and self.maze[row + 1][col] != '#':
            neighbors.append((row + 1, col))
        if col < len(self.maze[row]) - 1 and self.maze[row][col + 1] != '#':
            neighbors.append((row, col + 1))
        return neighbors

# find path through maze

    def solve(self):
        '''Solves the maze'''
        queue = []
        # set means that values inside can not repeat
        visited = set()
        # https://docs.python.org/3/library/heapq.html
        # push onto the queue (which becomes heapq), element containing values
        # we use heapq so the element with lowest heuristic value will always
        # be at the top of heap
        heapq.heappush(
            queue, (self.heuristic_manhattan(
                self.start), self.start, [
                self.start]))

        # Go through queue until it's empty
        # Find neighbor (which is not wall) closest to the
        # END point (based on heuristic)
        # Go there and repeat
        # if cannot find path it starts over but skips the path that lead it to
        # dead end
        path = None
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
                        queue, (self.heuristic_manhattan(neighbor), neighbor, new_path))
            if not self.test:
                print_maze(self.maze, new_path)
                print()
        return path

    # This heuristic returns the Manhattan distance between the given position
    # and the maze's end
    def heuristic_manhattan(self, position):
        '''Heuristic function that uses Manhattan distance'''
        return abs(position[0] - self.end[0]) + abs(position[1] - self.end[1])

    # This heuristic returns the Euclidean distance between the given position
    # and the maze's end
    def heuristic_euclidean(self, position):
        '''Heuristic function that uses Euclidean distance'''
        return (abs(position[0] - self.end[0])**2 +
                abs(position[1] - self.end[1])**2)**0.5


# Open and load text file to array
def load_maze(filename):
    '''Loads a maze from the specified file'''
    # Open for reading only and save to fileContents
    with open(filename, 'r', encoding='utf8') as file_contents:
        # strip() removes extra white spaces from the beginning and the end of
        # a string
        # list() changes string to array of chars
        # Inside of square brackets we will have an array of characters for
        # each line of file
        # After going through every line in a file we will have 2D array of arrays
        # of characters of every line
        maze = [list(line.strip()) for line in file_contents]
    return maze


def print_maze(maze, path=None):
    '''Prints the maze'''
    if path is None:
        path = []
    for row_i, row in enumerate(maze):
        for col_i, cell in enumerate(row):
            if (row_i, col_i) in path:
                print('*', end='')
            else:
                print(cell, end='')
        print()

def save_maze(maze, path=None, file_name = 'Maze', iteration = 0):
    if not os.path.exists('solvedMazes'): 
        os.mkdir('solvedMazes')
    f = open(f"solvedMazes/{iteration}solved{file_name}", "w")
    if path is None:
        path = []
    for row_i, row in enumerate(maze):
        for col_i, cell in enumerate(row):
            if (row_i, col_i) in path:
                f.write('*')
            else:
                f.write(cell)
        f.write('\n')


# Ran first in the code
if __name__ == '__main__':
    start_time = time.perf_counter()
    # print(sys.argv)
    file_name = 'maze.txt'
    test_mode = False
    folder_name = ''
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print('python main.py - run the script against default maze file (any file named maze.txt in the code directory) \n python main.py filename.txt - run the script against filename.txt file \n python main.py -h --help print this prompt \n python main.py -t --test non interactive (does not print steps) for testing different heuristics, goes through entire folder of mazes file and compares heuristic speed and path length')
            sys.exit()
        if sys.argv[1] == '-t' or sys.argv[1] == '--test':
             test_mode = True
             file_name = 'maze.txt'
             if len(sys.argv) > 2:
                folder_name = sys.argv[2]
    # Open and load text file to array
    loadedMaze = load_maze(file_name)
    # Initialize MazeSolver object with maze as parameter
    solver = MazeSolver(loadedMaze, test_mode)
    # Find path using MazeSolver solve method
    solvedPath = solver.solve()
    if not test_mode:
        print_maze(loadedMaze, solvedPath)
    save_maze(loadedMaze, solvedPath, file_name, 0)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"The execution time is: {execution_time}")
