#!/usr/bin/env python3

import random
from pydantic import BaseModel, Field


class Cell(BaseModel):
    north: int = Field(ge=0, le=1, default=0)
    east: int = Field(ge=0, le=1, default=0)
    south: int = Field(ge=0, le=1, default=0)
    west: int = Field(ge=0, le=1, default=0)


class MazeGenerator():
    def __init__(self, config):
        self.config = config

    def generate(self, seed: int | None = None) -> list[list[Cell]]:
        maze: list[list[Cell]] = []
        width = self.config["WIDTH"]
        heigth = self.config["HEIGHT"]
        entry = self.config["ENTRY"]
        exit = self.config["EXIT"]

        maze = [[Cell() for i in range(width)] for j in range(heigth)]
        visited = [[0 for i in range(width)] for j in range(heigth)]

        
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
