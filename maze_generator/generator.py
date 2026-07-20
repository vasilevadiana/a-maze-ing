#!/usr/bin/env python3

import random


class Cell():
    def __init__(self):
        self.visited = False
        self.blocked = False  # Part of 42 pattern
        self.walls = {
            "north": True,
            "east": True,
            "south": True,
            "west": True
        }
        # add variable for encryption?


class MazeGenerator():
    def __init__(self, config):
        self.seed = config["SEED"]
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.perfect = config["PERFECT"]

    def _set_42_pattern(self, maze):
        pattern_width = 7
        pattern_height = 5
        y = self.height // 2 - pattern_height // 2
        x = self.width // 2 - pattern_width // 2
        print(x, y)
        # TODO: validate - if not possible to fit 42 return error (enter exit also)
        # pattern "4"
        maze[y][x].blocked = True
        maze[y+1][x].blocked = True
        maze[y+2][x].blocked = True
        maze[y+2][x+1].blocked = True
        maze[y+2][x+2].blocked = True
        maze[y+3][x+2].blocked = True
        maze[y+4][x+2].blocked = True
        # pattern "2"
        maze[y][x+4].blocked = True
        maze[y][x+5].blocked = True
        maze[y][x+6].blocked = True
        maze[y+1][x+6].blocked = True
        maze[y+2][x+6].blocked = True
        maze[y+2][x+5].blocked = True
        maze[y+2][x+4].blocked = True
        maze[y+3][x+4].blocked = True
        maze[y+4][x+4].blocked = True
        maze[y+4][x+5].blocked = True
        maze[y+4][x+6].blocked = True
        return maze

    def _get_unvisited_neighbors(self, x, y, maze):
        unvisited_neighbors = []

        if y > 0:
            if not maze[y - 1][x].visited and not maze[y - 1][x].blocked:
                unvisited_neighbors.append({"y": y-1, 
                                            "x": x, 
                                            "neighbors_direction": "south",
                                            "current_cell_direction": "north"})
        if y < self.height - 1:
            if not maze[y + 1][x].visited and not maze[y + 1][x].blocked:
                unvisited_neighbors.append({"y": y+1, 
                                            "x": x,
                                            "neighbors_direction": "north",
                                            "current_cell_direction": "south"})
        if x > 0:
            if not maze[y][x - 1].visited and not maze[y][x - 1].blocked:
                unvisited_neighbors.append({"y": y, 
                                            "x": x-1, 
                                            "neighbors_direction": "east",
                                            "current_cell_direction": "west"})
        if x < self.width - 1:
            if not maze[y][x + 1].visited and not maze[y][x + 1].blocked:
                unvisited_neighbors.append({"y": y,
                                            "x": x+1,
                                            "neighbors_direction": "west",
                                            "current_cell_direction": "east"})
        return unvisited_neighbors


    def has_open_3x3(self): #TODO
        return False


    def _remove_random_walls(self, maze, walls_num):
        removed = 0
        while removed < walls_num:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if maze[y][x].blocked:
                continue

            neighbors = []

            if y > 0:
                neighbors.append({"y": y-1, 
                                  "x": x, 
                                  "neighbors_direction": "south",
                                  "current_cell_direction": "north"})
            if y < self.height - 1:
                neighbors.append({"y": y+1, 
                                  "x": x,
                                  "neighbors_direction": "north",
                                  "current_cell_direction": "south"})
            if x > 0:
                neighbors.append({"y": y, 
                                  "x": x-1, 
                                  "neighbors_direction": "east",
                                  "current_cell_direction": "west"})
            if x < self.width - 1:
                neighbors.append({"y": y,
                                  "x": x+1,
                                  "neighbors_direction": "west",
                                  "current_cell_direction": "east"})
                
            neighbor = random.choice(neighbors)
            if maze[neighbor["y"]][neighbor["x"]].blocked:
                continue
            if maze[y][x].walls[neighbor["current_cell_direction"]]:
                maze[y][x].walls[neighbor["current_cell_direction"]] = False
                maze[neighbor["y"]][neighbor["x"]].walls[neighbor["neighbors_direction"]] = False
                if self.has_open_3x3():
                    maze[y][x].walls[neighbor["current_cell_direction"]] = True
                    maze[neighbor["y"]][neighbor["x"]].walls[neighbor["neighbors_direction"]] = True
                else:
                    removed += 1
        return maze


    def generate(self) -> list[list[Cell]]:
        random.seed(self.seed)

        maze = [[Cell() for i in range(self.width)] for j in range(self.height)]
        maze = self._set_42_pattern(maze)
        # x = random.randint(0, self.width - 1)
        # y = random.randint(0, self.height - 1)
        x = 0
        y = 0
        maze[y][x].visited = True

        stack = [] #to save visited Cells

        while True:
            neighbors = self._get_unvisited_neighbors(x, y, maze)

            if neighbors:
                neighbor = random.choice(neighbors)
                maze[neighbor["y"]][neighbor["x"]].visited = True
                maze[neighbor["y"]][neighbor["x"]].walls[neighbor["neighbors_direction"]] = False
                maze[y][x].walls[neighbor["current_cell_direction"]] = False
                
                stack.append((x, y))
                x, y = neighbor["x"], neighbor["y"]
            elif stack:
                x, y = stack.pop()
            else:
                break

        if not self.perfect:
            walls_num = (self.height * self.width) // 10
            maze = self._remove_random_walls(maze, walls_num)
        return maze


    def print_maze(self):
        # Top border
        print("+" + "---+" * self.width)

        for y in range(self.height):

            # Vertical walls
            line = "|"
            for x in range(self.width):
                line += "   "
                if maze[y][x].walls["east"]:
                    line += "|"
                else:
                    line += " "
            print(line)

            # Horizontal walls
            line = "+"
            for x in range(self.width):
                if maze[y][x].walls["south"]:
                    line += "---+"
                else:
                    line += "   +"
            print(line)


if __name__ == "__main__":
    try:
        # If executed as a package (python -m), relative import works
        from ..config_parser import config_parser
    except (ImportError, ValueError):
        # If executed as a script, add parent folder to sys.path and import absolutely
        import os
        import sys

        ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if ROOT not in sys.path:
            sys.path.insert(0, ROOT)
        from config_parser import config_parser

    config = config_parser("/Users/dianavasileva/Documents/42/Core/Milestone2/amazing/a-maze-ing/config.txt")
    print(config)

    gen = MazeGenerator(config)
    maze = gen.generate()
    # for i in range(len(maze)):
    #     for j in range(len(maze[0])):
    #         print(maze[i][j].visited)
    #         print(maze[i][j].walls)
    #     print()
    gen.print_maze()
