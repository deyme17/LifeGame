import pygame as pg
from config import WIDTH, HEIGHT

class Game:
    def __init__(self, settings, grid_renderer, grid_logic, cell_generator, settings_panel):
        self.settings = settings
        self.renderer = grid_renderer
        self.logic = grid_logic
        self.cell_generator = cell_generator
        self.settings_panel = settings_panel

        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH + 300, HEIGHT))
        pg.display.set_caption("Game of Life")

        self.positions = set()

    def start_game(self) -> None:
        running = True
        while running:
            time_delta = self.clock.tick(self.settings.FPS) / 1000.0
            running = self.handle_events()
            self.update()
            self.settings_panel.update(time_delta)
            self.render()
        pg.quit()

    def update(self) -> None:
        if not self.settings.PAUSED:
            self.positions = self.logic.adjust_grid(self.positions)

    def render(self) -> None:
        self.renderer.draw_grid(self.positions, show_grid=self.settings.SHOW_GRID)
        self.settings_panel.draw()
        pg.display.update()

    def handle_events(self) -> bool:
        events = pg.event.get()
        for event in events:
            settings_changed = self.settings_panel.handle_event(event)
            if settings_changed:
                self.update_game_logic()

            if event.type == pg.QUIT:
                return False

            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if x < WIDTH:
                    pos = (x // self.settings.CELL_SIZE, y // self.settings.CELL_SIZE)
                    if 0 <= pos[0] < self.settings.GRID_WIDTH and 0 <= pos[1] < self.settings.GRID_HEIGHT:
                        if pos in self.positions:
                            self.positions.remove(pos)
                        else:
                            self.positions.add(pos)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.toggle_pause()
                elif event.key == pg.K_c:
                    self.positions.clear()
                    self.settings.PAUSED = True
                elif event.key == pg.K_r:
                    count = int(self.settings.GRID_WIDTH * self.settings.GRID_HEIGHT * self.settings.FILL_PROBABILITY)
                    self.positions = self.cell_generator.gen_cells(count)
        return True

    def update_game_logic(self):
        self.logic.grid_size = (self.settings.GRID_WIDTH, self.settings.GRID_HEIGHT)
        self.logic.survive_set = self.settings.SURVIVE
        self.logic.birth_set = self.settings.BIRTH
        
        self.cell_generator.grid_size = (self.settings.GRID_WIDTH, self.settings.GRID_HEIGHT)
        
        self.renderer.grid_size = (self.settings.GRID_WIDTH, self.settings.GRID_HEIGHT)
        self.renderer.cell_size = self.settings.CELL_SIZE
        
        valid_positions = set()
        for pos in self.positions:
            if 0 <= pos[0] < self.settings.GRID_WIDTH and 0 <= pos[1] < self.settings.GRID_HEIGHT:
                valid_positions.add(pos)
        self.positions = valid_positions

    def toggle_pause(self) -> None:
        self.settings.PAUSED = not self.settings.PAUSED
        self.settings_panel.pause_button.set_text(f'Paused: {"Yes" if self.settings.PAUSED else "No"}')
        self.settings_panel.draw()
        pg.display.update()
