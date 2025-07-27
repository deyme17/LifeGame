import pygame as pg
import random as rnd
from config import WIDTH, HEIGHT

class Game:
    def __init__(self, settings, grid_renderer, grid_logic, cell_generator):
        self.settings = settings
        self.renderer = grid_renderer
        self.logic = grid_logic
        self.cell_generator = cell_generator

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Game of Life")

        self.positions = set()

    def start_game(self) -> None:
        running = True
        paused = True
        frame_counter = 0

        while running:
            self.clock.tick(self.settings.FPS)
            events = pg.event.get()

            if not paused:
                frame_counter += 1
                if frame_counter >= self.settings.FPS:
                    frame_counter = 0
                    self.positions = self.logic.adjust_grid(self.positions)

            for event in events:
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    pos = (x // self.settings.CELL_SIZE, y // self.settings.CELL_SIZE)
                    if pos in self.positions:
                        self.positions.remove(pos)
                    else:
                        self.positions.add(pos)

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        paused = not paused
                    elif event.key == pg.K_c:
                        self.positions.clear()
                        paused = True
                        frame_counter = 0
                    elif event.key == pg.K_r:
                        count = int(self.settings.GRID_WIDTH * self.settings.GRID_HEIGHT * self.settings.FILL_PROBABILITY)
                        self.positions = self.cell_generator.gen_cells(count)

            self.renderer.draw_grid(self.positions, show_grid=self.settings.SHOW_GRID)
            pg.display.update()

        pg.quit()
