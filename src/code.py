import argparse
import heapq
import random
import numpy as np
import matplotlib.pyplot as plt
from time import time
from visualization import visualize_binary_maze

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

# generates a perfect maze using the given maze
def maze_generator(maze):
    rows, cols = maze.shape
    my_perfect_maze_generation_algorithm(maze, 0, rows - 1, 0, cols - 1)

    for c in range(1, cols - 1):
        if maze[0, c] == 0:
            maze[1, c] = 0
        if maze[rows - 1, c] == 0:
            maze[rows - 2, c] = 0
    for r in range(1, rows - 1):
        if maze[r, 0] == 0:
            maze[r, 1] = 0
        if maze[r, cols - 1] == 0:
            maze[r, cols - 2] = 0

    return maze

# generates a perfect maze using the given maze
def my_perfect_maze_generation_algorithm(maze, row_bottom, row_top, column_left, column_right):
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
                maze[horizontal_wall][i] = 1

        my_perfect_maze_generation_algorithm(maze, row_bottom, horizontal_wall, column_left, column_right)
        my_perfect_maze_generation_algorithm(maze, horizontal_wall, row_top, column_left, column_right)

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
                maze[i][vertical_wall] = 1

        my_perfect_maze_generation_algorithm(maze, row_bottom, row_top, column_left, vertical_wall)
        my_perfect_maze_generation_algorithm(maze, row_bottom, row_top, vertical_wall, column_right)

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

# solves the maze by finding the shortest path in the given maze
def solver(maze):
    maze = np.array(maze)
    n = maze.shape[0]
    m = maze.shape[1]
    
    openings = []
    for c in range(m):
        if maze[0, c] == 0:
            openings.append((0, c))
        if maze[n - 1, c] == 0:
            openings.append((n - 1, c))
    for r in range(1, n - 1):            
        if maze[r, 0] == 0:
            openings.append((r, 0))
        if maze[r, m - 1] == 0:
            openings.append((r, m - 1))
    
    if len(openings) < 2:
        return np.zeros((n, m), dtype=int)
    
    start = openings[0]
    end = openings[-1]
    
    parent_r = np.full((n, m), -1, dtype=np.int32)
    parent_c = np.full((n, m), -1, dtype=np.int32)
    
    sr, sc = start
    er, ec = end
    
    parent_r[sr, sc] = sr
    parent_c[sr, sc] = sc
    
    counter = 0
    h = abs(sr - er) + abs(sc - ec)
    pq = [(h, counter, sr, sc)]
    
    g_score = np.full((n, m), np.iinfo(np.int32).max, dtype=np.int32)
    g_score[sr, sc] = 0
    
    found = False
    
    while pq:
        f, _, r, c = heapq.heappop(pq)
        
        if r == er and c == ec:
            found = True
            break
        
        cur_g = g_score[r, c]
        if cur_g + abs(r - er) + abs(c - ec) > f:
            continue
        
        new_g = cur_g + 1
        
        nr = r - 1
        if nr >= 0 and maze[nr, c] == 0 and new_g < g_score[nr, c]:
            g_score[nr, c] = new_g
            parent_r[nr, c] = r
            parent_c[nr, c] = c
            counter += 1
            heapq.heappush(pq, (new_g + abs(nr - er) + abs(c - ec), counter, nr, c))
        
        nr = r + 1
        if nr < n and maze[nr, c] == 0 and new_g < g_score[nr, c]:
            g_score[nr, c] = new_g
            parent_r[nr, c] = r
            parent_c[nr, c] = c
            counter += 1
            heapq.heappush(pq, (new_g + abs(nr - er) + abs(c - ec), counter, nr, c))
        
        nc = c - 1
        if nc >= 0 and maze[r, nc] == 0 and new_g < g_score[r, nc]:
            g_score[r, nc] = new_g
            parent_r[r, nc] = r
            parent_c[r, nc] = c
            counter += 1
            heapq.heappush(pq, (new_g + abs(r - er) + abs(nc - ec), counter, r, nc))
        
        nc = c + 1
        if nc < m and maze[r, nc] == 0 and new_g < g_score[r, nc]:
            g_score[r, nc] = new_g
            parent_r[r, nc] = r
            parent_c[r, nc] = c
            counter += 1
            heapq.heappush(pq, (new_g + abs(r - er) + abs(nc - ec), counter, r, nc))
    
    solution = np.zeros((n, m), dtype=int)
    
    if not found:
        return solution
    
    r, c = er, ec
    while not (r == sr and c == sc):
        solution[r, c] = 1
        pr, pc = parent_r[r, c], parent_c[r, c]
        r, c = pr, pc
    solution[sr, sc] = 1
    
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

    if args.show_init:
        visualize_binary_maze(init, height=vis_height, width=vis_width, display=True)

    gen_maze = maze_generator(init)
    visualize_binary_maze(
        gen_maze,
        height=vis_height,
        width=vis_width,
        save_dir=args.output,
        display=display,
    )

if __name__ == '__main__':
    main()