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
"""
""" Technical requirements:
- implemented in Python.
- adheres to basic standards of lean coding in accordance to PEP8
- comments in the crucial parts to help with readability and understanding.
- The clear instruction how to run and test the code should be included.
"""
"""
Thinks that do not work:
Does not work if no Start (Should print out NO START FOUND)
Does not work if no End   (Should print out NO END FOUND)
Does not work if no path  (Should print out NO PATH FOUND)
"""




import heapq
import sys

class MazeSolver:

    # self corresponds to "this" in js, it refers to object of MazeSolver class
    def __init__(self, maze):
        # assign readed maze 2D array to parameter from class MazeSolver
        self.maze = maze
        self.start, self.end = self.find_start_and_end()

# go through each character in 2D array and find one that corresponds to
# Start/End character

    def find_start_and_end(self):
        start = end = None
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                if self.maze[row][col] == 'S':
                    start = (row, col)
                elif self.maze[row][col] == 'E':
                    end = (row, col)
                if start is not None and end is not None:
                    return start, end
        print(f"DID NOT FOUND START OR END, Start: {start}, End: {end}")

# Go through each neighboor
#       N
#     N * N
#       N
# If it is not a "wall" (#) add its position to list of neighbors

    def get_neighbors(self, position):
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
        queue = []
        # set means that values inside can not repeat
        visited = set()
        # https://docs.python.org/3/library/heapq.html
        # push onto the queue (which becomes heapq), element containinig values
        # we use heapq so the element with lowest heurisitc value will always
        # be at the top of heap
        heapq.heappush(
            queue, (self.heuristicEuclidean(
                self.start), self.start, [
                self.start]))

        # go through queue until it's empty
        # find neighbour (which is not wall) closests to END point (based on heuristic)
        # go there and repeat
        # if cannot find path it starts over but skips the path that lead it to
        # dead end
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
                return path
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    heapq.heappush(
                        queue, (self.heuristicEuclidean(neighbor), neighbor, new_path))
            print_maze(self.maze, new_path)
            print()

    # This heuristic returns the Manhatan distance between the given position
    # and the maze's end
    def heuristicManhatan(self, position):
        return abs(position[0] - self.end[0]) + abs(position[1] - self.end[1])

    # This heuristic returns the Euclidean distance between the given position
    # and the maze's end
    def heuristicEuclidean(self, position):
        return (abs(position[0] - self.end[0])**2 +
                abs(position[1] - self.end[1])**2)**0.5


# Open and load text file to array
def load_maze(filename):
    # Open for reading only and save to fileContents
    fileContents = open(filename, 'r')
    # strip() removes extra white spaces from the beginning and the end of a string
    # list() changes string to array of chars
    # Inside of square brackets we will have an array of characters for each line of file
    # after going through every line in a file we will have 2D array of arrays
    # of characters of every line
    maze = [list(line.strip()) for line in fileContents]
    return maze


def print_maze(maze, path=None):
    if path is None:
        path = []
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if (row, col) in path:
                print('*', end='')
            else:
                print(maze[row][col], end='')
        print()


# Ran first in the code
if __name__ == '__main__':
    print (sys.argv)
    file_name = 'maze.txt'
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    # Open and load text file to array
    maze = load_maze(file_name)
    # Initialize MazeSolver object with maze as paramater
    solver = MazeSolver(maze)
    # Find path using MazeSolver solve method
    path = solver.solve()
    print_maze(maze, path)
