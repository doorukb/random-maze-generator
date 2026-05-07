import heapq
import random
import numpy as np
import matplotlib.pyplot as plt
from time import time
from visualization import visualize_binary_maze

def init_maze(n=64):
    maze = np.zeros((n, n), dtype=int)
    maze[0, :] = 1
    maze[n - 1, :] = 1
    maze[:, 0] = 1
    maze[:, n - 1] = 1
    entrance = random.randrange(1, n - 1, 2)  
    exit = random.randrange(1, n - 1, 2)
    maze[entrance, 0] = 0
    maze[exit, n - 1] = 0
    return maze

def maze_generator(maze):
    n = len(maze)
    my_perfect_maze_generation_algorithm(maze, 0, n - 1, 0, n - 1)

    for c in range(1, n - 1):
        if maze[0, c] == 0:
            maze[1, c] = 0
        if maze[n - 1, c] == 0:
            maze[n - 2, c] = 0
    for r in range(1, n - 1):
        if maze[r, 0] == 0:
            maze[r, 1] = 0
        if maze[r, n - 1] == 0:
            maze[r, n - 2] = 0

    return maze

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

    
def time_to_gen(n):
    maze = init_maze(n)
    start_time = time()
    maze_generator(maze)
    end_time = time()
    return end_time - start_time

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

def bonus(maze):
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


if __name__ == '__main__':
    # Test 1:
    init = init_maze(32)
    visualize_binary_maze(init)

    # Test 2:
    gen_maze = maze_generator(init)
    visualize_binary_maze(gen_maze)

    # Test 3:
    plot_time_growth()
