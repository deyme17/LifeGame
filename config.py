WIDTH, HEIGHT = 1000, 750

CELL_SIZE = 25
GRID_SIZE = (WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)
SHOW_GRID = True

SETTINGS_PANEL_SIZE = 300
SETTINGS_PANEL_COLOR = (22, 22, 22) # Gray
PAUSED = True

FPS = 10

ALIVE_COLOR = (50, 205, 50)     # Lime
DEAD_COLOR = (40, 40, 40)       # Gray
GRID_COLOR = (0, 0, 0)          # Black
TEXT_COLOR = (255, 255, 255)    # White
BACKGROUND_COLOR = DEAD_COLOR

# Rules
BIRTH = {3}                # A dead cell with 3 neighbors becomes alive
SURVIVE = {2, 3}           # A live cell with 2 or 3 neighbors survives
FILL_PROBABILITY = 0.2
