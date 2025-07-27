import random as rnd
from abc import ABC, abstractmethod


class ICellGenerator(ABC):
    def __init__(self, grid_size):
        self.grid_size = grid_size

    @abstractmethod
    def gen_cells():
        pass
    
    
class RandomCellGenerator(ICellGenerator):
    def __init__(self, grid_size):
        super().__init__(grid_size)

    def gen_cells(self, cell_num: int) -> set[tuple[int, int]]:
        poses = set()
        for _ in range(cell_num):
            new_pos = (rnd.randrange(0, self.grid_size[0]), rnd.randrange(0, self.grid_size[1]))
            poses.add(new_pos)
        return poses