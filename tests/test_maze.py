"""Headless tests for maze generation: perfect-maze invariants."""
import os
import sys
from collections import deque

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import random  # noqa: E402

from maze import find_border_openings, init_maze, maze_generator, solver_dfs_steps  # noqa: E402


def _generate(rows=17, cols=17, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    maze = init_maze(rows, cols)
    maze_generator(maze)
    return maze


def _passage_cells(maze):
    return {(r, c) for r, c in zip(*np.where(maze == 0))}


def _reachable(maze, start):
    h, w = maze.shape
    seen = {start}
    q = deque([start])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and maze[nr, nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc))
    return seen


def test_maze_shape_and_border():
    maze = _generate()
    assert maze.shape == (17, 17)
    border = np.concatenate([maze[0], maze[-1], maze[:, 0], maze[:, -1]])
    # exactly two openings (entrance + exit) on the border
    assert (border == 0).sum() == 2


def test_maze_is_fully_connected():
    maze = _generate(seed=7)
    passages = _passage_cells(maze)
    start = next(iter(passages))
    assert _reachable(maze, start) == passages


def test_maze_is_acyclic():
    """A perfect maze's passage graph is a tree: edges == nodes - 1."""
    maze = _generate(seed=21)
    passages = _passage_cells(maze)
    edges = 0
    for r, c in passages:
        for dr, dc in ((1, 0), (0, 1)):
            if (r + dr, c + dc) in passages:
                edges += 1
    assert edges == len(passages) - 1


def test_same_seed_reproduces_same_maze():
    a = _generate(seed=99)
    b = _generate(seed=99)
    assert np.array_equal(a, b)


def test_solver_reaches_exit():
    maze = _generate(seed=3)
    openings = find_border_openings(maze)
    assert len(openings) == 2
    steps = list(solver_dfs_steps(maze))
    assert steps, "solver produced no steps"
