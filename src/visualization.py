import pygame
import sys
import numpy as np

# --- Constants ---
COLOR_WALL = (0, 0, 0)       # Black for 1s
COLOR_PATH = (255, 255, 255) # White for 0s

# takes a 2D binary matrix representing a maze and visualizes it using Pygame.  
# 1 = Wall (Black), 0 = Path (White).
# keeps the window open until the user closes it.
def visualize_binary_maze(matrix, height=800, width=800, save_dir=None):
    # 1. Basic Validation
    rows = len(matrix)
    if rows == 0:
        print("Error: Empty matrix provided.")
        return
    cols = len(matrix[0])
    if cols == 0:
        print("Error: Matrix has rows but no columns.")
        return

    # 2. Pygame Setup
    pygame.init()

    cell_width = width / len(matrix[0])
    cell_height = height / len(matrix)
    
    # Calculate window dimensions based on grid size and cell size
    window_width = width
    window_height = height
    
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(f"Maze Visualization ({cols}x{rows})")
    
    # 3. Drawing Loop
    # Fill background white first (assuming 0s are paths)
    screen.fill(COLOR_PATH) 

    for r in range(rows):
        for c in range(cols):
            cell_value = matrix[r][c]
            
            # Calculate the position of this specific cell
            x_pos = c * cell_width
            y_pos = r * cell_height
            
            # Define the rectangular area for this cell
            rect = pygame.Rect(x_pos, y_pos, cell_width, cell_height)

            # Draw based on value
            if cell_value == 1:
                pygame.draw.rect(screen, COLOR_WALL, rect)
            # (Optional: else draw white, but the background fill handles this)
                
    # Update the display to show what we just drew
    pygame.display.flip()

    print("Visualization open. Close the window to exit.")

    # 4. Event Loop to keep window open
    running = True
    while running:
        # Cap the frame rate to prevent high CPU usage just waiting for events
        pygame.time.Clock().tick(30) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # If you want to save your maze you can do it with this
    if save_dir is not None:
        pygame.image.save(screen, save_dir)
                
    pygame.quit()

# =========================================
# Example Usage
# =========================================
if __name__ == "__main__":
    # A sample 15x15 binary matrix representing a maze
    # 1s are walls, 0s are paths
    sample_maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    # Another way to randomly generate 0 and 1
    #sample_maze = np.random.randint(0, 2, size=(64, 80))

    # Notice that we can scale height and width to match the ratio of the dimensions (not needed for this proj)
    # If save-dir is made not None then you can save your maze visualization
    visualize_binary_maze(sample_maze, height=800, width=1000, save_dir=None)