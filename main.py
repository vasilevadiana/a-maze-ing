#!/usr/bin/env python3

from config_parser import config_parser
from maze_generator.generator import MazeGenerator
from maze_solver.solver import solve_maze

if __name__ == "__main__":

    # try:
    #     config = config_parser("config.txt")
    #     print(config)
    
    #     gen = MazeGenerator(config)
    #     maze = gen.generate()
    #     print(maze)

    #     start = (0, 0)
    #     exit_cell = (0, 2)
    #     path = solve_maze(maze, start, exit_cell)
    # except Exception as e:
    #     print(e)

    config = config_parser("config.txt")
    print(config)

    gen = MazeGenerator(config)
    maze = gen.generate()
    print(maze)

    start = config["ENTRY"]
    exit_cell = config["EXIT"]
    path = solve_maze(maze, start, exit_cell)
    print("\n", path)
