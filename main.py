from core import Grid, RandomCellGenerator, Game
from ui.renderers import GridRenderer
from utils.settings import Settings
from config import WIDTH, HEIGHT
import pygame as pg

pg.init()

def main() -> None:
    settings = Settings()
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    renderer = GridRenderer(screen, (settings.GRID_WIDTH, settings.GRID_HEIGHT), settings.CELL_SIZE)
    grid = Grid((settings.GRID_WIDTH, settings.GRID_HEIGHT), settings.SURVIVE, settings.BIRTH)
    cell_gen = RandomCellGenerator((settings.GRID_WIDTH, settings.GRID_HEIGHT))

    game = Game(settings, renderer, grid, cell_gen)
    game.start_game()

if __name__=='__main__':
    main()