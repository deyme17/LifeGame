from config import SETTINGS_PANEL_SIZE, SETTINGS_PANEL_COLOR, WIDTH, HEIGHT
import pygame as pg
import pygame_gui as gui

ELEMENT_HEIGHT = 30
PANEL_SPACING = 40
INFO_LINE_HEIGHT = 25
INFO_LINES = [
    "Controls:",
    "Spacebar - pause/continue",
    "C - clear field",
    "R - random cells",
    "Mouse - add/delete cell"
]


class SettingsPanel:
    def __init__(self, screen: pg.Surface, x: int, y: int, width: int, height: int, settings) -> None:
        self.screen = screen
        self.rect = pg.Rect(x, y, width, height)
        self.settings = settings
        self.ui_manager = gui.UIManager((width, height))
        self.panel_width = SETTINGS_PANEL_SIZE - 20

        self.sliders: dict[str, tuple[gui.elements.UIHorizontalSlider, bool, callable]] = {}
        self.value_labels: dict[str, gui.elements.UILabel] = {}

        self.create_ui_elements()

    def create_slider(self, label_text: str, y_pos: int, start_value: float, value_range: tuple[float, float], slider_key: str, integer: bool = True, fmt: callable = str) -> None:
        # label
        gui.elements.UILabel(
            relative_rect=pg.Rect(10, y_pos, 100, ELEMENT_HEIGHT),
            text=label_text,
            manager=self.ui_manager
        )
        # slider
        slider = gui.elements.UIHorizontalSlider(
            relative_rect=pg.Rect(120, y_pos, 120, ELEMENT_HEIGHT),
            start_value=start_value,
            value_range=value_range,
            manager=self.ui_manager
        )
        # val
        value_label = gui.elements.UILabel(
            relative_rect=pg.Rect(250, y_pos, 40, ELEMENT_HEIGHT),
            text=fmt(start_value),
            manager=self.ui_manager
        )
        self.sliders[slider_key] = (slider, integer, fmt)
        self.value_labels[slider_key] = value_label

    def create_text_entry(self, label_text: str, y_pos: int, start_text: str, entry_key: str) -> None:
        # label
        gui.elements.UILabel(
            relative_rect=pg.Rect(10, y_pos, self.panel_width, ELEMENT_HEIGHT),
            text=label_text,
            manager=self.ui_manager
        )
        # text
        entry = gui.elements.UITextEntryLine(
            relative_rect=pg.Rect(10, y_pos + ELEMENT_HEIGHT, self.panel_width, ELEMENT_HEIGHT),
            manager=self.ui_manager
        )
        entry.set_text(start_text)
        setattr(self, entry_key, entry)

    def create_ui_elements(self) -> None:
        y = 20  # initial y pos

        gui.elements.UILabel(
            relative_rect=pg.Rect(10, y, self.panel_width, ELEMENT_HEIGHT),
            text='Settings',
            manager=self.ui_manager
        )
        y += PANEL_SPACING

        self.create_slider('FPS:', y, self.settings.FPS, (1, 60), 'fps')
        y += PANEL_SPACING
        self.create_slider('Cell size:', y, self.settings.CELL_SIZE, (5, 50), 'cell_size')
        y += PANEL_SPACING

        self.create_text_entry('Random filling (%):', y, f"{self.settings.FILL_PROBABILITY * 100:.0f}%", 'fill_entry')
        y += PANEL_SPACING + ELEMENT_HEIGHT

        self.show_grid_button = gui.elements.UIButton(
            relative_rect=pg.Rect(10, y, self.panel_width, ELEMENT_HEIGHT),
            text=f'Show grid: {"Yes" if self.settings.SHOW_GRID else "No"}',
            manager=self.ui_manager
        )
        y += PANEL_SPACING

        self.pause_button = gui.elements.UIButton(
            relative_rect=pg.Rect(10, y, self.panel_width, ELEMENT_HEIGHT),
            text=f'Paused: {"Yes" if self.settings.PAUSED else "No"}',
            manager=self.ui_manager
        )
        y += PANEL_SPACING

        self.create_text_entry('Survive rule (csv):', y, ','.join(map(str, self.settings.SURVIVE)), 'survive_entry')
        y += PANEL_SPACING + 20
        self.create_text_entry('Birth rule (csv):', y, ','.join(map(str, self.settings.BIRTH)), 'birth_entry')
        y += PANEL_SPACING + 50

        self.apply_button = gui.elements.UIButton(
            relative_rect=pg.Rect(10, y, 130, ELEMENT_HEIGHT),
            text='Apply',
            manager=self.ui_manager
        )
        self.reset_button = gui.elements.UIButton(
            relative_rect=pg.Rect(150, y, 130, ELEMENT_HEIGHT),
            text='Reset',
            manager=self.ui_manager
        )
        y += PANEL_SPACING + 20

        for i, line in enumerate(INFO_LINES):
            gui.elements.UILabel(
                relative_rect=pg.Rect(10, y + i * INFO_LINE_HEIGHT, self.panel_width, 20),
                text=line,
                manager=self.ui_manager
            )

    def handle_event(self, event: pg.event.Event) -> bool:
        # translate pos to panel local coords
        if hasattr(event, 'pos'):
            event = pg.event.Event(event.type, event.dict)
            event.pos = (event.pos[0] - WIDTH, event.pos[1])

        self.ui_manager.process_events(event)

        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.show_grid_button:
                self.settings.SHOW_GRID = not self.settings.SHOW_GRID
                self.show_grid_button.set_text(f'Show grid: {"Yes" if self.settings.SHOW_GRID else "No"}')
                return True
            if event.ui_element == self.pause_button:
                self.settings.PAUSED = not self.settings.PAUSED
                self.pause_button.set_text(f'Paused: {"Yes" if self.settings.PAUSED else "No"}')
                return True
            if event.ui_element == self.apply_button:
                return self.apply_settings()
            if event.ui_element == self.reset_button:
                return self.reset_settings()

        if event.type == gui.UI_HORIZONTAL_SLIDER_MOVED:
            for key, (slider, integer, fmt) in self.sliders.items():
                if event.ui_element == slider:
                    val = slider.get_current_value()
                    if integer:
                        val = int(val)
                    self.value_labels[key].set_text(fmt(val))
                    if key == 'fps':
                        self.settings.FPS = val
                    return True

        return False

    def apply_settings(self) -> bool:
        try:
            new_cell_size = int(self.sliders['cell_size'][0].get_current_value())
            if new_cell_size != self.settings.CELL_SIZE:
                self.settings.CELL_SIZE = new_cell_size
                self.settings.GRID_WIDTH = WIDTH // new_cell_size
                self.settings.GRID_HEIGHT = HEIGHT // new_cell_size

            fill_text = self.fill_entry.get_text().strip()
            if fill_text.endswith('%'):
                fill_text = fill_text[:-1]
            fill_value = float(fill_text) / 100.0
            if not (0 <= fill_value <= 1):
                return False
            self.settings.FILL_PROBABILITY = fill_value

            survive_text = self.survive_entry.get_text().strip()
            if survive_text:
                self.settings.SURVIVE = set(map(int, survive_text.split(',')))

            birth_text = self.birth_entry.get_text().strip()
            if birth_text:
                self.settings.BIRTH = set(map(int, birth_text.split(',')))

            return True
        except ValueError:
            return False

    def reset_settings(self) -> bool:
        from config import CELL_SIZE, SHOW_GRID, FPS, BIRTH, SURVIVE, FILL_PROBABILITY

        self.settings.CELL_SIZE = CELL_SIZE
        self.settings.SHOW_GRID = SHOW_GRID
        self.settings.FPS = FPS
        self.settings.BIRTH = BIRTH
        self.settings.SURVIVE = SURVIVE
        self.settings.FILL_PROBABILITY = FILL_PROBABILITY

        self.sliders['fps'][0].set_current_value(FPS)
        self.value_labels['fps'].set_text(str(FPS))

        self.sliders['cell_size'][0].set_current_value(CELL_SIZE)
        self.value_labels['cell_size'].set_text(str(CELL_SIZE))

        self.fill_entry.set_text(f"{int(FILL_PROBABILITY * 100)}%")

        self.show_grid_button.set_text(f'Show grid: {"Yes" if SHOW_GRID else "No"}')
        self.pause_button.set_text(f'Paused: {"Yes" if getattr(self.settings, "PAUSED", False) else "No"}')

        self.survive_entry.set_text(','.join(map(str, SURVIVE)))
        self.birth_entry.set_text(','.join(map(str, BIRTH)))

        return True

    def update(self, time_delta: float) -> None:
        self.ui_manager.update(time_delta)

    def draw(self) -> None:
        surface = pg.Surface((self.rect.width, self.rect.height))
        surface.fill(SETTINGS_PANEL_COLOR)
        self.ui_manager.draw_ui(surface)
        self.screen.blit(surface, (WIDTH, 0))
        pg.draw.line(self.screen, (200, 200, 200), (WIDTH, 0), (WIDTH, HEIGHT), 2)
