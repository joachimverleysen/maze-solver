import tkinter as tk
from time import sleep
import queue

from Maze import Maze

maze = []
current_position = None
adjacent_positions = None


def get_maze(file: str) -> list:
    maze = []
    with open(file, 'r') as f:
        for line in f:
            row = []
            for char in line:
                if char == '\n':
                    continue
                row.append(char)
            maze.append(row)
    return maze

def get_start_end(maze):
    start = None
    end = None
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 's':
                if start is not None:
                    raise Exception("Multiple start positions")
                start = (i, j)

            elif maze[i][j] == 'x':
                end = (i, j)

    return start, end

def get_adjacent_positions(maze, row, col):
    result = []
    if row > 0:
        if maze[row-1][col] == 'p' or maze[row-1][col] == 'x':
            result.append((row-1, col))

    if row < len(maze)-1:
        if maze[row-1][col] == 'p' or maze[row-1][col] == 'x':
            result.append((row-1, col))

    if col > 0:
        if maze[row][col-1] == 'p' or maze[row][col-1] == 'x':
            result.append((row, col-1))

    if col < len(maze[0]) - 1:
        if maze[row][col+1] == 'p' or maze[row][col+1] == 'x':
            result.append((row, col+1))

    return result

def find_exit(maze, start, end):
    paths = [[start]]
    positions_visited = set()
    while not len(paths) == 0:
        for path in paths:
            current_position = path[-1]
            if current_position == end:
                return path

            adjacent_positions = list(set(filter(lambda pos : pos not in positions_visited,
                                        get_adjacent_positions(maze, current_position[0], current_position[1]))))
            maze.update(current_position, adjacent_positions, positions_visited)
            if len(adjacent_positions) == 0:
                paths.remove(path)      # Dead end
            elif len(adjacent_positions) == 1:
                path.append(adjacent_positions[0])
            else:
                for adjacent_position in adjacent_positions:
                    new_path = path.copy()
                    new_path.append(adjacent_position)
                    paths.append(new_path)
                # first_adjacent_position = adjacent_positions[0]
                # path.append(first_adjacent_position)
                # for i in range(1, len(adjacent_positions)):
                #     new_path = path.copy()
                #     new_path.append(adjacent_positions[i])
                #     paths.append(new_path)

            positions_visited.add(current_position)
            sleep(.1)
    return False

def main():
    window = tk.Tk()
    inputfile = "input/happyDay.txt"
    maze = Maze(inputfile, window)
    start, end = get_start_end(maze)
    if start is None:
        raise Exception("No start position in input file")
    elif end is None:
        print("No end position in input file")

    path_to_exit = find_exit(maze, start, end)
    if path_to_exit:
        print("Exit found")
        maze.show_path(path_to_exit, start, end)
    else:
        print("Exit not Found")
    window.mainloop()


if __name__ == '__main__':
    main()