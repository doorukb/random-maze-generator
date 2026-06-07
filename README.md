# Random Maze Generator

- Python 3.8

This project focuses on perfect maze generation using a recursive divide-and-conquer algorithm. A perfect maze is one that is fully connected (every cell is reachable from every other cell) and acyclic (there is exactly one path between any two points, meaning no loops). It generates a completely different maze each time the algorithm is run.

The algorithm works by recursively dividing a chamber into two sub-chambers with a wall, then cutting exactly one passage through that wall. Because each division produces exactly one passage, no cycle can ever be formed between any two sub-mazes. The maze is proven correct by induction: the base cases are trivially perfect, and each recursive step combines two perfect sub-mazes through a single connection, preserving both connectivity and acyclicity.


Algorithm Details

The maze is represented as a 2D binary matrix where 1 is a wall and 0 is a passage. The outer border is initialized as walls, and one entrance and one exit are randomly placed on opposite sides.

At each recursive step, the algorithm inspects the current chamber's interior dimensions. If the interior height or width is less than or equal to 1, the recursion stops (base case). Otherwise, the chamber is divided along its longer axis: a horizontal wall is drawn if the chamber is taller, a vertical wall if it is wider, and the direction is chosen randomly when the dimensions are equal.

Wall positions are restricted to even-indexed rows or columns, and hole positions are restricted to odd-indexed rows or columns. This constraint prevents walls and holes from overlapping with each other across different recursive calls. The wall position is chosen randomly from all valid even-indexed positions within the current chamber, and the hole is chosen randomly from all valid odd-indexed positions along that wall. The algorithm then recurses on each of the two resulting sub-chambers.


## Installation
    pip install -r requirements.txt


## Usage
    cd src
    python code.py


## CLI 

- `-r`, `--rows` — maze height in rows (default: 32)
- `-c`, `--cols` — maze width in columns (default: same as `--rows`)
- `-o`, `--output` — save the final frame to a PNG path
- `--height` — visualization height in pixels (default: 800)
- `--width` — visualization width in pixels (default: scaled from aspect ratio)
- `--seed` — random seed for reproducible mazes
- `--delay` — milliseconds between animation frames (default: 15)
- `--no-solve` — skip the DFS solution animation after generation
- `--no-display` — save with `--output` without opening a window
- `--show-init` — show the border-only maze in a separate static window before animation
- `--benchmark` — plot generation time vs maze size instead of generating a maze


## Examples

    # Default animated run (32×32)
    python code.py

    # Rectangular maze with a fixed seed
    python code.py -r 32 -c 48 --seed 42

    # Faster animation on a larger maze
    python code.py -r 64 --delay 5

    # Headless PNG export (no animation, no DFS overlay)
    python code.py -r 16 -o maze.png --no-display

    # Benchmark plot only
    python code.py --benchmark