import pygame
import numpy as np

COLOR_WALL = (0, 0, 0)
COLOR_PATH = (255, 255, 255)
COLOR_VISITED = (170, 190, 255)
COLOR_CURRENT = (255, 190, 40)
COLOR_SOLUTION = (40, 180, 90)

# maze animator class to animate the maze generation and solution
class MazeAnimator:
    def __init__(self, maze, height=800, width=800, delay_ms=15):
        self.maze = np.array(maze, dtype=int)
        self.rows, self.cols = self.maze.shape
        self.height = height
        self.width = width
        self.delay_ms = delay_ms
        self.cell_w = width / self.cols
        self.cell_h = height / self.rows
        self.visited = set()
        self.solution = set()
        self.current = None
        self._running = True

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Maze ({self.cols}x{self.rows})")
        self.clock = pygame.time.Clock()

    def _cell_rect(self, row, col):
        return pygame.Rect(col * self.cell_w, row * self.cell_h, self.cell_w, self.cell_h)

    def _cell_color(self, row, col):
        if (row, col) in self.solution:
            return COLOR_SOLUTION
        if self.current == (row, col):
            return COLOR_CURRENT
        if (row, col) in self.visited:
            return COLOR_VISITED
        return COLOR_WALL if self.maze[row, col] == 1 else COLOR_PATH

    def _draw_cell(self, row, col):
        pygame.draw.rect(self.screen, self._cell_color(row, col), self._cell_rect(row, col))

    def _draw_all(self):
        self.screen.fill(COLOR_PATH)
        for row in range(self.rows):
            for col in range(self.cols):
                self._draw_cell(row, col)

    def _pump_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def _frame(self):
        pygame.display.flip()
        self.clock.tick(60)
        if self.delay_ms > 0:
            pygame.time.delay(self.delay_ms)
        self._pump_events()

    def apply_cell(self, row, col, value):
        self.maze[row, col] = value
        self._draw_cell(row, col)
        self._frame()

    def apply_visit(self, row, col):
        self.current = (row, col)
        self.visited.add((row, col))
        self._draw_cell(row, col)
        self._frame()

    def apply_backtrack(self, row, col):
        self.visited.discard((row, col))
        if self.current == (row, col):
            self.current = None
        self._draw_cell(row, col)
        self._frame()

    def apply_solution(self, path):
        self.solution = set(path)
        self.current = None
        self.visited.clear()
        self._draw_all()
        self._frame()

    def wait_until_closed(self):
        print("Animation complete. Close the window to exit.")
        while self._running:
            self.clock.tick(30)
            self._pump_events()

    def save(self, path):
        pygame.image.save(self.screen, path)
        print(f"Saved maze visualization to {path}")

    def quit(self):
        pygame.quit()

# draw the static maze visualization
def _draw_static(matrix, height, width):
    rows, cols = len(matrix), len(matrix[0])
    cell_w = width / cols
    cell_h = height / rows
    surface = pygame.Surface((width, height))
    surface.fill(COLOR_PATH)
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 1:
                pygame.draw.rect(surface, COLOR_WALL, pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h))
    return surface


def visualize_binary_maze(matrix, height=800, width=800, save_dir=None, display=True):
    rows = len(matrix)
    if rows == 0 or len(matrix[0]) == 0:
        print("Error: empty matrix provided.")
        return

    pygame.init()
    surface = _draw_static(matrix, height, width)

    if display:
        screen = pygame.display.set_mode((width, height))
        cols = len(matrix[0])
        pygame.display.set_caption(f"Maze Visualization ({cols}x{rows})")
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        print("Visualization open. Close the window to exit.")

        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    else:
        screen = surface

    if save_dir is not None:
        pygame.image.save(screen, save_dir)
        print(f"Saved maze visualization to {save_dir}")
    pygame.quit()

# animate the maze generation and solution
def animate_maze(maze, generation_steps, solve_steps, height=800, width=800,
                   delay_ms=15, save_dir=None):
    animator = MazeAnimator(maze, height=height, width=width, delay_ms=delay_ms)
    animator._draw_all()
    animator._frame()

    for row, col, value in generation_steps:
        if not animator._running:
            break
        animator.apply_cell(row, col, value)

    for step in solve_steps:
        if not animator._running:
            break
        kind = step[0]
        if kind == "visit":
            animator.apply_visit(step[1], step[2])
        elif kind == "backtrack":
            animator.apply_backtrack(step[1], step[2])
        elif kind == "solution":
            animator.apply_solution(step[1])

    if save_dir is not None:
        animator.save(save_dir)

    animator.wait_until_closed()
    animator.quit()