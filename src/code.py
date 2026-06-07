import argparse
import random
import numpy as np
import matplotlib.pyplot as plt
from time import time
from visualization import animate_maze, visualize_binary_maze

# initializes a maze with the given number of rows and columns
def init_maze(rows=64, cols=None):
    if cols is None:
        cols = rows
    maze = np.zeros((rows, cols), dtype=int)
    maze[0, :] = 1
    maze[rows - 1, :] = 1
    maze[:, 0] = 1
    maze[:, cols - 1] = 1
    entrance = random.randrange(1, rows - 1, 2)
    exit = random.randrange(1, rows - 1, 2)
    maze[entrance, 0] = 0
    maze[exit, cols - 1] = 0
    return maze

# records the step in the maze
def _record_step(maze, on_step, row, col, value):
    if maze[row, col] != value:
        maze[row, col] = value
        if on_step is not None:
            on_step(row, col, value)

# generates a perfect maze using the given maze
def maze_generator(maze, on_step=None):
    rows, cols = maze.shape
    my_perfect_maze_generation_algorithm(maze, 0, rows - 1, 0, cols - 1, on_step)

    for c in range(1, cols - 1):
        if maze[0, c] == 0:
            _record_step(maze, on_step, 1, c, 0)
        if maze[rows - 1, c] == 0:
            _record_step(maze, on_step, rows - 2, c, 0)
    for r in range(1, rows - 1):
        if maze[r, 0] == 0:
            _record_step(maze, on_step, r, 1, 0)
        if maze[r, cols - 1] == 0:
            _record_step(maze, on_step, r, cols - 2, 0)
    return maze

# generates a perfect maze using the given maze
def my_perfect_maze_generation_algorithm(maze, row_bottom, row_top, column_left, column_right, on_step=None):
    interior_width = column_right - column_left
    interior_height = row_top - row_bottom

    if(interior_height <= 1 or interior_width <= 1):
        return
    if(interior_width > interior_height):
        direction = 'vertical'
    elif(interior_width < interior_height):
        direction = 'horizontal'
    else:
        direction = random.choice(['horizontal', 'vertical'])

    if direction == 'horizontal':
        possible_walls = [r for r in range(row_bottom + 1, row_top) if r % 2 == 0]
        if not possible_walls:
            return
        horizontal_wall = random.choice(possible_walls)

        possible_holes = [c for c in range(column_left + 1, column_right) if c % 2 == 1]
        if not possible_holes:
            return
        random_hole = random.choice(possible_holes)

        for i in range(column_left, column_right + 1):
            if i != random_hole:
                _record_step(maze, on_step, horizontal_wall, i, 1)

        my_perfect_maze_generation_algorithm(maze, row_bottom, horizontal_wall, column_left, column_right, on_step)
        my_perfect_maze_generation_algorithm(maze, horizontal_wall, row_top, column_left, column_right, on_step)

    elif direction == 'vertical':
        possible_walls = [c for c in range(column_left + 1, column_right) if c % 2 == 0]
        if not possible_walls:
            return
        vertical_wall = random.choice(possible_walls)

        possible_holes = [r for r in range(row_bottom + 1, row_top) if r % 2 == 1]
        if not possible_holes:
            return
        random_hole = random.choice(possible_holes)

        for i in range(row_bottom, row_top + 1):
            if i != random_hole:
                _record_step(maze, on_step, i, vertical_wall, 1)

        my_perfect_maze_generation_algorithm(maze, row_bottom, row_top, column_left, vertical_wall, on_step)
        my_perfect_maze_generation_algorithm(maze, row_bottom, row_top, vertical_wall, column_right, on_step)

# measures the time taken to generate a perfect maze
def time_to_gen(n):
    maze = init_maze(n)
    start_time = time()
    maze_generator(maze)
    end_time = time()
    return end_time - start_time

# plots the time taken to generate a perfect maze
def plot_time_growth(ns=[2,4,8,16,32,64,128,256]):
    times = [time_to_gen(n) for n in ns]
    plt.plot(ns, times)
    plt.xlabel('size of the maze')
    plt.ylabel('time to generate (s)')
    plt.title('Total time to generate nxn maze')
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.show()
    return

# finds the border openings in the given maze
def find_border_openings(maze):
    maze = np.array(maze)
    rows, cols = maze.shape
    openings = []
    for col in range(cols):
        if maze[0, col] == 0:
            openings.append((0, col))
        if maze[rows - 1, col] == 0:
            openings.append((rows - 1, col))
    for row in range(1, rows - 1):
        if maze[row, 0] == 0:
            openings.append((row, 0))
        if maze[row, cols - 1] == 0:
            openings.append((row, cols - 1))
    return openings

# finds the steps to solve the maze using DFS
def solver_dfs_steps(maze):
    maze = np.array(maze)
    rows, cols = maze.shape
    openings = find_border_openings(maze)
    if len(openings) < 2:
        return

    start, end = openings[0], openings[-1]
    visited = set()

    def dfs(row, col, path):
        visited.add((row, col))
        path = path + [(row, col)]
        yield ("visit", row, col)

        if (row, col) == end:
            yield ("solution", path)
            return True

        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0 and (nr, nc) not in visited):
                found = yield from dfs(nr, nc, path)
                if found:
                    return True

        yield ("backtrack", row, col)
        return False
    yield from dfs(*start, [])

# solves the maze using DFS helpers
def solver(maze):
    rows, cols = np.array(maze).shape
    solution = np.zeros((rows, cols), dtype=int)
    for step in solver_dfs_steps(maze):
        if step[0] == "solution":
            for row, col in step[1]:
                solution[row, col] = 1
    return solution

# parses the arguments from the command line, so the maze size and
# output options can be set without editing code
def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate and visualize perfect mazes.',
    )
    parser.add_argument(
        '-r', '--rows', type=int, default=32,
        help='number of rows / height (default: 32)',
    )
    parser.add_argument(
        '-c', '--cols', type=int, default=None,
        help='number of columns / width; defaults to --rows for a square maze',
    )
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help='save the generated maze image to this path (e.g. output/maze.png)',
    )
    parser.add_argument(
        '--height', type=int, default=800,
        help='visualization height in pixels (default: 800)',
    )
    parser.add_argument(
        '--width', type=int, default=None,
        help='visualization width in pixels (default: scaled from maze aspect ratio)',
    )
    parser.add_argument(
        '--seed', type=int, default=None,
        help='random seed for reproducible mazes',
    )
    parser.add_argument(
        '--show-init', action='store_true',
        help='also display the uninitialized border maze before generation',
    )
    parser.add_argument(
        '--no-display', action='store_true',
        help='save with --output without opening an interactive window',
    )
    parser.add_argument(
        '--benchmark', action='store_true',
        help='plot generation time vs maze size instead of generating a maze',
    )
    parser.add_argument(
        '--delay', type=int, default=15,
        help='milliseconds between animation frames (default: 15)',
    )
    parser.add_argument(
        '--no-solve', action='store_true',
        help='skip DFS solution animation after generation',
    )
    return parser.parse_args()

def main():
    args = parse_args()

    if args.benchmark:
        plot_time_growth()
        return

    if args.no_display and not args.output:
        raise SystemExit('error: --no-display requires --output')

    rows = args.rows
    cols = args.cols if args.cols is not None else rows

    if rows < 3 or cols < 3:
        raise SystemExit('error: rows and cols must each be at least 3')

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    vis_height = args.height
    vis_width = args.width if args.width is not None else int(vis_height * cols / rows)
    display = not args.no_display

    init = init_maze(rows, cols)
    maze = init.copy()
    generation_steps = []

    maze_generator(maze, on_step=lambda r, c, v: generation_steps.append((r, c, v)))

    if not display:
        visualize_binary_maze(maze, height=vis_height, width=vis_width, save_dir=args.output, display=False)
        return
    if args.show_init:
        visualize_binary_maze(init, height=vis_height, width=vis_width, display=True)
    if args.no_solve:
        solve_steps = []
    else:
        solve_steps = list(solver_dfs_steps(maze))
    animate_maze(init, generation_steps, solve_steps, height=vis_height, width=vis_width, delay_ms=args.delay, save_dir=args.output)

if __name__ == '__main__':
    main()