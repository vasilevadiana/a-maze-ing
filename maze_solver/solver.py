from collections import deque
from typing import List, Tuple, Optional, Dict

def get_neighbors(maze: List[List[int]], cell: Tuple[int, int]):
    return

def is_walkable(maze: List[List[int]], cell: Tuple[int, int], neighbor_cell: Tuple[int, int]):
    return


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
