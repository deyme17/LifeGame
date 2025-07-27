from config import *

class Settings:
    def __init__(
        self,
        cell_size=CELL_SIZE,
        show_grid=SHOW_GRID,
        fps=FPS,
        birth=BIRTH,
        survive=SURVIVE,
        fill_probability=FILL_PROBABILITY,
        paused=PAUSED
    ):
        self.CELL_SIZE = cell_size
        self.SHOW_GRID = show_grid
        self.FPS = fps
        self.BIRTH = birth
        self.SURVIVE = survive
        self.FILL_PROBABILITY = fill_probability
        self.PAUSED = paused

        self.GRID_WIDTH = WIDTH // self.CELL_SIZE
        self.GRID_HEIGHT = HEIGHT // self.CELL_SIZE
