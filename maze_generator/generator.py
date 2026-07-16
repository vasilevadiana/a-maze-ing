#!/usr/bin/env python3

import random


class Cell:
    def __init__(self, north=0, east=0, south=0, west=0):
        self.north = int(north)
        self.east = int(east)
        self.south = int(south)
        self.west = int(west)
        self._validate()

    def _validate(self):
        for name in ("north", "west", "east", "south"):
            val = getattr(self, name)
            if val not in (0, 1):
                raise ValueError(f"{name} must be 0 or 1")


class MazeGenerator():
    def __init__(self, config):
        self.config = config

    def generate(self, seed: int | None = None) -> list[list[Cell]]:
        maze: list[list[Cell]] = []

        return maze


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

    config = config_parser("/home/dvasilev/Documents/core/Milestone2/amazing/config")
    print(config)
