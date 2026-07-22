#!/usr/bin/env python3

from config_parser import config_parser
from maze_generator.generator import MazeGenerator

if __name__ == "__main__":

    try:
        config = config_parser("config.txt")
        print(config)
    
        gen = MazeGenerator(config)
        maze = gen.generate()
        gen.print_maze(maze)
    except Exception as e:
        print(e)

    # config = config_parser("config.txt")
    # print(config)

    # gen = MazeGenerator(config)
    # maze = gen.generate()
    # gen.print_maze(maze)
