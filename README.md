Random Maze Generator

This project focuses on perfect maze generation using a recursive divide-and-conquer algorithm. A perfect maze is one that is fully connected (every cell is reachable from every other cell) and acyclic (there is exactly one path between any two points, meaning no loops). It generates a completely different maze each time the algorithm is run.

The algorithm works by recursively dividing a chamber into two sub-chambers with a wall, then cutting exactly one passage through that wall. Because each division produces exactly one passage, no cycle can ever be formed between any two sub-mazes. The maze is proven correct by induction: the base cases are trivially perfect, and each recursive step combines two perfect sub-mazes through a single connection, preserving both connectivity and acyclicity.


<img width="300" height="300" alt="maze" src="https://github.com/user-attachments/assets/938b319c-7317-43ea-a81c-d16c0bc05d90" />


Algorithm Details

The maze is represented as a 2D binary matrix where 1 is a wall and 0 is a passage. The outer border is initialized as walls, and one entrance and one exit are randomly placed on opposite sides.

At each recursive step, the algorithm inspects the current chamber's interior dimensions. If the interior height or width is less than or equal to 1, the recursion stops (base case). Otherwise, the chamber is divided along its longer axis: a horizontal wall is drawn if the chamber is taller, a vertical wall if it is wider, and the direction is chosen randomly when the dimensions are equal.

Wall positions are restricted to even-indexed rows or columns, and hole positions are restricted to odd-indexed rows or columns. This constraint prevents walls and holes from overlapping with each other across different recursive calls. The wall position is chosen randomly from all valid even-indexed positions within the current chamber, and the hole is chosen randomly from all valid odd-indexed positions along that wall. The algorithm then recurses on each of the two resulting sub-chambers.


INSTALLATION 

Python 3.8 or higher is required.

Install the required packages:
    pip install -r requirements.txt
    pip install pygame


USAGE

All runnable code is in the src/ directory. Run the scripts from the project root or from within the src/ directory.
    cd src
    python code.py


You can import and call the visualization function directly:

    from visualization import visualize_binary_maze
    visualize_binary_maze(your_matrix, height=800, width=800)

Set save_dir to a file path string (e.g. "output/maze.png") to save the rendered image instead of only displaying it.


Roadmap

- Add support for non-square (rectangular) maze dimensions as a starting input.
- Expose a command-line interface so maze size and output options can be set without editing code.
- Animate the maze generation step by step in the visualization window.
- Visualize the A* solution path overlaid on the maze in a distinct color.
- Add additional generation algorithms (e.g. Prim's, Kruskal's) for comparison.
- Write unit tests to verify perfect maze properties (connectivity and acyclicity) on generated outputs.
