import tkinter as tk
class Maze:
    def __init__(self, inputfile, window):
        self.maze = self.parse_file(inputfile)
        self.window = window
        self.tiles = self.make_grid(window)


    def parse_file(self, file):
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

    def make_grid(self, window):
        grid = []
        for i in range(len(self)):
            row = []
            for j in range(len(self[0])):
                cell_color = "black"

                if self[i][j] == 'p':
                    cell_color = "white"

                elif self[i][j] == 's':
                    cell_color = "red"

                elif self[i][j] == 'x':
                    cell_color = "green"

                cell = tk.Frame(window, bg=cell_color, highlightbackground="black",
                                highlightcolor="black", highlightthickness=1,
                                width=50, height=50, padx=3, pady=3)

                cell.grid(row=i, column=j)
                row.append(cell)
            grid.append(row)
        return grid
    def __getitem__(self, pos):
        return self.maze[pos]

    def __len__(self):
        return len(self.maze)
    def get_start_end(self):
        start = None
        end = None
        for i in range(len(self)):
            for j in range(len(self[0])):
                if self[i][j] == 's':
                    if start is not None:
                        raise Exception("Multiple start positions")
                    start = (i, j)

                elif self[i][j] == 'x':
                    end = (i, j)

        return start, end

    def set_tile_color(self, row, col, color):
        self.tiles[row][col].configure(background=color)
        self.tiles[row][col].update()


    def get_tile_color(self, row, col):
        return self.tiles[row][col].cget("background")
    def update(self, current_position, adjacent_positions, visited):
        for row in self.tiles:
            for tile in row:
                if tile.cget("background") == "yellow" or tile.cget("background") == "grey":
                    tile.configure(background="white")
                    tile.update()

        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                tile = self.tiles[row][col]
                if (row, col) in visited:
                    tile.configure(background="blue")
                if (row, col) in adjacent_positions:
                    tile.configure(background="yellow")

                if (row, col) == current_position:
                    tile.configure(background="red")
                tile.update()

    def show_path(self, path, start, end):
        for row in self.tiles:
            for tile in row:
                if (tile.cget("background") == "yellow" or
                        tile.cget("background") == "grey" or tile.cget("background") == "blue"):
                    tile.configure(background="white")
                tile.update()

        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                tile = self.tiles[row][col]
                if (row, col) in path:
                    tile.configure(background="yellow")

                tile.update()

        self.set_tile_color(start[0], start[1], "red")
        self.set_tile_color(end[0], end[1], "green")
