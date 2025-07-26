WIDTH, HEIGHT = 1000, 800

CELL_SIZE = 10
GRID_SIZE = (WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)

FPS = 10

ALIVE_COLOR = (50, 205, 50)     # Lime
DEAD_COLOR = (40, 40, 40)       # Gray
GRID_COLOR = (0, 0, 0)          # Black

# Rules
BIRTH = {3}                # A dead cell with 3 neighbors becomes alive
SURVIVE = {2, 3}           # A live cell with 2 or 3 neighbors survives