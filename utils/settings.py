from config import *

class Settings:
    def __init__(
        self,
        cell_size=CELL_SIZE,
        show_grid=SHOW_GRID,
        fps=FPS,
        alive_color=ALIVE_COLOR,
        dead_color=DEAD_COLOR,
        grid_color=GRID_COLOR,
        birth=BIRTH,
        survive=SURVIVE,
        initial_state=INITIAL_STATE,
        initial_fill_probability=INITIAL_FILL_PROBABILITY,
    ):
        self.CELL_SIZE = cell_size
        self.SHOW_GRID = show_grid
        self.FPS = fps
        self.ALIVE_COLOR = alive_color
        self.DEAD_COLOR = dead_color
        self.GRID_COLOR = grid_color
        self.BIRTH = birth
        self.SURVIVE = survive
        self.INITIAL_STATE = initial_state
        self.INITIAL_FILL_PROBABILITY = initial_fill_probability

        self.GRID_WIDTH = WIDTH // self.CELL_SIZE
        self.GRID_HEIGHT = HEIGHT // self.CELL_SIZE
