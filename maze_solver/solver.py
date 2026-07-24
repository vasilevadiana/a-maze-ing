from collections import deque
from typing import List, Tuple, Optional, Dict


def get_neighbors(maze: List[List[int]],
                  cell: Tuple[int, int]
                  ) -> List[Tuple[int, int]]:
    neighbors: List[Tuple[int, int]] = []
    x, y = cell
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    total_rows = len(maze)
    total_cols = len(maze[0]) if total_rows > 0 else 0
    for dx, dy in directions:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < total_cols and 0 <= ny < total_rows:
            neighbors.append((nx, ny))
    return neighbors


direction_masks = {
    (0, -1): 1,
    (1, 0): 2,
    (0, 1): 4,
    (-1, 0): 8
}

opposite_masks = {
    1: 4,
    2: 8,
    4: 1,
    8: 2
}


def is_walkable(maze: List[List[int]],
                cell: Tuple[int, int],
                neighbor_cell: Tuple[int, int]) -> bool:
    curr_x, curr_y = cell
    nghbr_x, nghbr_y = neighbor_cell
    change = (nghbr_x - curr_x, nghbr_y - curr_y)
    if change not in direction_masks:
        return False
    out_wall = direction_masks[change]
    in_wall = opposite_masks[out_wall]
    if (maze[curr_y][curr_x] & out_wall) != 0:
        return False
    if (maze[nghbr_y][nghbr_x] & in_wall) != 0:
        return False
    return True


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


# ---------TESTER----------

# import unittest
# # Import your functions here:
# # from solver import get_neighbors, is_walkable, solve_maze, direction_masks


# class TestMazeSolver(unittest.TestCase):

#     def setUp(self):
#         """
#         Bitwise wall encoding scheme used:
#         1: North wall
#         2: East wall
#         3: South wall / 4: South wall (depending on 1=N, 2=E, 4=S, 8=W)
#         8: West wall

#         Sample 3x3 Maze:
#         Cell values store wall presence as bit flags.
#         For example:
#         0  = No walls (open in all directions)
#         15 = 1|2|4|8 = Fully walled cell (isolated)
#         """
#         # Simple open 3x3 grid (no internal walls)
#         self.open_grid = [
#             [0, 0, 0],
#             [0, 0, 0],
#             [0, 0, 0]
#         ]

#         # 3x3 Maze with a wall blocking middle cell (1, 1)
#           from the top (1, 0 has South wall = 4)
#         # and cell (0, 1) has South wall flag (4).
#         self.walled_grid = [
#             [0, 4, 0],   # (0, 1) has South wall (4)
#             [0, 1, 0],   # (1, 1) has North wall (1)
#             [0, 0, 0]
#         ]

#         # Completely blocked off exit
#         self.unsolvable_grid = [
#             [0, 0, 0],
#             [0, 15, 0],  # Middle cell has all 4 walls (1+2+4+8)
#             [0, 0, 0]
#         ]

#     # -------------------------------------------------------------
#     # 1. Tests for get_neighbors
#     # -------------------------------------------------------------
#     def test_get_neighbors_corner(self):
#         """Top-left corner (0,0) should only have 2 in-bounds neighbors."""
#         neighbors = get_neighbors(self.open_grid, (0, 0))
#         self.assertCountEqual(neighbors, [(0, 1), (1, 0)])

#     def test_get_neighbors_center(self):
#         """Center cell (1,1) in a 3x3 grid should have 4 neighbors."""
#         neighbors = get_neighbors(self.open_grid, (1, 1))
#         self.assertCountEqual(neighbors, [(0, 1), (2, 1), (1, 0), (1, 2)])

#     def test_get_neighbors_bottom_right(self):
#         """Bottom-right cell (2,2) should only have 2 valid neighbors."""
#         neighbors = get_neighbors(self.open_grid, (2, 2))
#         self.assertCountEqual(neighbors, [(1, 2), (2, 1)])

#     # -------------------------------------------------------------
#     # 2. Tests for is_walkable
#     # -------------------------------------------------------------
#     def test_is_walkable_no_wall(self):
#         """Moving between open cells should return True."""
#         self.assertTrue(is_walkable(self.open_grid, (0, 0), (0, 1)))

#     def test_is_walkable_with_wall(self):
#         """Moving from (0, 1) to (1, 1) across a South wall (4)
#            should return False."""
#         self.assertFalse(is_walkable(self.walled_grid, (0, 1), (1, 1)))

#     def test_is_walkable_invalid_direction(self):
#         """Diagonal steps or non-adjacent steps should return False."""
#         self.assertFalse(is_walkable(self.open_grid, (0, 0), (1, 1)))
#         self.assertFalse(is_walkable(self.open_grid, (0, 0), (0, 2)))

#     # -------------------------------------------------------------
#     # 3. Tests for solve_maze
#     # -------------------------------------------------------------
#     def test_solve_maze_simple_path(self):
#         """Should find the shortest path in an open grid."""
#         start = (0, 0)
#         exit_cell = (0, 2)
#         path = solve_maze(self.open_grid, start, exit_cell)
#         expected_path = [(0, 0), (0, 1), (0, 2)]
#         self.assertEqual(path, expected_path)

#     def test_solve_maze_around_wall(self):
#         """Should navigate around a wall to reach the target."""
#         start = (0, 1)
#         exit_cell = (1, 1)
#         # Blocked directly from (0,1) ->
#           (1,1), must go around via (0,0) or (0,2)
#         path = solve_maze(self.walled_grid, start, exit_cell)
#         self.assertIsNotNone(path)
#         self.assertEqual(path[0], start)
#         self.assertEqual(path[-1], exit_cell)

#     def test_solve_maze_same_start_and_exit(self):
#         """When start and exit are the same cell,
#         return a path with 1 element."""
#         path = solve_maze(self.open_grid, (1, 1), (1, 1))
#         self.assertEqual(path, [(1, 1)])

#     def test_solve_maze_unsolvable(self):
#         """Should return None if target is surrounded by walls."""
#         start = (0, 0)
#         exit_cell = (1, 1)  # Surrounded by 15 (all walls)
#         path = solve_maze(self.unsolvable_grid, start, exit_cell)
#         self.assertIsNone(path)


# if __name__ == '__main__':
#     unittest.main()
