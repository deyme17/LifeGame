import pygame as pg
from config import GRID_COLOR, ALIVE_COLOR, BACKGROUND_COLOR, WIDTH, HEIGHT

class GridRenderer:
    def __init__(self, surface, grid_size, cell_size):
        self.surface = surface
        self.grid_size = grid_size
        self.cell_size = cell_size

    def draw_grid(self, positions: set[tuple[int, int]]) -> None:
        self.surface.fill(BACKGROUND_COLOR)
        cols, rows = self.grid_size

        for row in range(rows + 1):
            pg.draw.line(surface=self.surface, color=GRID_COLOR, start_pos=(0, row * self.cell_size), end_pos=(WIDTH, row * self.cell_size))
        for col in range(cols + 1):
            pg.draw.line(surface=self.surface, color=GRID_COLOR, start_pos=(col * self.cell_size, 0), end_pos=(col * self.cell_size, HEIGHT))

        for col, row in positions:
            top_left = (col * self.cell_size, row * self.cell_size)
            pg.draw.rect(surface=self.surface, color=ALIVE_COLOR, rect=(*top_left, self.cell_size, self.cell_size))