from config import (WIDTH, HEIGHT, FPS, CELL_SIZE,
                    BACKGROUND_COLOR, GRID_COLOR, GRID_SIZE, ALIVE_COLOR, 
                    SURVIVE, BIRTH, UPDATE_FREQ)
import random as rnd
import pygame as pg

pg.init()

pg.display.set_caption("Life Game")
screen = pg.display.set_mode(size=(WIDTH, HEIGHT))
clock = pg.time.Clock()

def gen_cells(cell_num: int) -> set[tuple[int, int]]:
    poses = set()
    for _ in range(cell_num):
        new_pos = (rnd.randrange(0, GRID_SIZE[0]), rnd.randrange(0, GRID_SIZE[1]))
        poses.add(new_pos)
    return poses

def draw_grid(positions: set[tuple[int, int]]) -> None:
    cols, rows = GRID_SIZE

    for row in range(rows + 1):
        pg.draw.line(surface=screen, color=GRID_COLOR, start_pos=(0, row * CELL_SIZE), end_pos=(WIDTH, row * CELL_SIZE))
    for col in range(cols + 1):
        pg.draw.line(surface=screen, color=GRID_COLOR, start_pos=(col * CELL_SIZE, 0), end_pos=(col * CELL_SIZE, HEIGHT))

    for col, row in positions:
        top_left = (col * CELL_SIZE, row * CELL_SIZE)
        pg.draw.rect(surface=screen, color=ALIVE_COLOR, rect=(*top_left, CELL_SIZE, CELL_SIZE))

def adjust_grid(positions: set[tuple[int, int]]) -> set[tuple[int, int]]:
    new_positions = set()
    candidates = positions.copy()

    for pos in positions:
        candidates.update(get_neighbors(pos))

    for pos in candidates:
        alive_neighbors = sum((neighbor in positions) for neighbor in get_neighbors(pos))

        if pos in positions and alive_neighbors in SURVIVE:
            new_positions.add(pos)
        elif pos not in positions and alive_neighbors in BIRTH:
            new_positions.add(pos)

    return new_positions

def get_neighbors(position: tuple[int, int]) -> list[tuple[int, int]]:
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]
    neighbors = []
    x, y = position

    for dx, dy in DIRECTIONS:
        new_x, new_y = x + dx, y + dy

        if not (0 <= new_x < GRID_SIZE[0] and 0 <= new_y < GRID_SIZE[1]):
            continue

        neighbors.append((new_x, new_y))

    return neighbors

def main() -> None:
    running = True
    paused = True
    count = 0

    positions = set()

    while running:
        clock.tick(FPS)
        events = pg.event.get()

        if not paused:
            count += 1

        if count >= UPDATE_FREQ:
            count = 0
            positions = adjust_grid(positions)

        pg.display.set_caption("Playing" if not paused else "Paused")

        for event in events:
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                pos = (x // CELL_SIZE, y // CELL_SIZE)
                
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    paused = not paused

                if event.key == pg.K_c:
                    paused = True
                    positions.clear()
                    count = 0

                if event.key == pg.K_r:
                    positions = gen_cells(rnd.randrange(5, 7) * GRID_SIZE[0])

        screen.fill(BACKGROUND_COLOR)
        draw_grid(positions)
        pg.display.update()

    pg.quit()


if __name__=='__main__':
    main()