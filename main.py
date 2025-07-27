from core import Grid, RandomCellGenerator, Game
from ui import GridRenderer, SettingsPanel
from utils.settings import Settings
from config import WIDTH, HEIGHT, SETTINGS_PANEL_SIZE
import pygame as pg

pg.init()

def main() -> None:
    settings = Settings()
    screen = pg.display.set_mode((WIDTH + SETTINGS_PANEL_SIZE, HEIGHT))

    renderer = GridRenderer(screen, (settings.GRID_WIDTH, settings.GRID_HEIGHT), settings.CELL_SIZE)
    grid = Grid((settings.GRID_WIDTH, settings.GRID_HEIGHT), settings.SURVIVE, settings.BIRTH)
    cell_gen = RandomCellGenerator((settings.GRID_WIDTH, settings.GRID_HEIGHT))

    settings_panel = SettingsPanel(screen, WIDTH, 0, SETTINGS_PANEL_SIZE, HEIGHT, settings)

    game = Game(settings, renderer, grid, cell_gen, settings_panel)
    game.start_game()

if __name__=='__main__':
    main()