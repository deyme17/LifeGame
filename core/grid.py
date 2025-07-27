class Grid:
    def __init__(self, grid_size, survive_set, birth_set):
        self.grid_size = grid_size
        self.survive_set = survive_set
        self.birth_set = birth_set

    def adjust_grid(self, positions: set[tuple[int, int]]) -> set[tuple[int, int]]:
        new_positions = set()
        candidates = positions.copy()

        for pos in positions:
            candidates.update(self.get_neighbors(pos))

        for pos in candidates:
            alive_neighbors = sum((neighbor in positions) for neighbor in self.get_neighbors(pos))

            if pos in positions and alive_neighbors in self.survive_set:
                new_positions.add(pos)
            elif pos not in positions and alive_neighbors in self.birth_set:
                new_positions.add(pos)

        return new_positions
    
    def get_neighbors(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        DIRECTIONS = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1),
        ]
        neighbors = []
        x, y = position

        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy

            if not (0 <= new_x < self.grid_size[0] and 0 <= new_y < self.grid_size[1]):
                continue

            neighbors.append((new_x, new_y))

        return neighbors