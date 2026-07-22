from collections import deque
from typing import List, Tuple, Optional, Dict


def get_neighbors(maze: List[List[int]],
                  cell: Tuple[int, int]
                  ) -> List[Tuple[int, int]]:
    neighbors: List[Tuple[int, int]] = []
    row, col = cell
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    total_rows = len(maze)
    total_cols = len(maze[0]) if total_rows > 0 else 0
    for dr, dc in directions:
        next_rows = row + dr
        next_cols = col + dc
        if 0 <= next_rows < total_rows and 0 <= next_cols < total_cols:
            neighbors.append((next_rows, next_cols))
    return neighbors

# todo!

# def is_walkable(maze: List[List[int]],
#                 cell: Tuple[int, int],
#                 neighbor_cell: Tuple[int, int]) -> bool:
#     dr = cell[0] - neighbor_cell[0]
#     dc = cell[1] - neighbor_cell[1]
#     if dr == -1
#         direction =
#     return


def solve_maze(
        maze: List[List[int]],
        start: Tuple[int, int],
        exit: Tuple[int, int]
        ) -> Optional[List[Tuple[int, int]]]:
    queue = deque([start])
    visited = {start}
    parent_map: Dict[Tuple[int, int],
                     Optional[Tuple[int, int]]] = {start: None}

    while queue:
        current = queue.popleft()
        if current == exit:
            path = []
            while current is not None:
                path.append(current)
                current = parent_map[current]
            path.reverse()
            return path
        for nghbor in get_neighbors(maze, current):
            if nghbor not in visited and is_walkable(maze, current, nghbor):
                visited.add(nghbor)
                parent_map[nghbor] = current
                queue.append(nghbor)
    return None
