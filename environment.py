import random
import numpy as np
import pygame
from cells import CellType


class Environment:
    def __init__(self, config):
        
        width = int(config['world']['width'])
        height = int(config['world']['height'])
        cell_size = int(config['cell']['size'])
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cell_types = self.load_cell_types(config)
        self.grid = [[None for y in range(self.height)] for x in range(self.width)]
        self.generate()

    def load_cell_types(self, config):
        cell_types = []
        for name, value in config["cell_types"].items():
            c1,c2,c3, nutrient_level, weight = value.split(",")
            color = (int(c1), int(c2), int(c3))
            nutrient_level = float(nutrient_level.strip())
            cell_types.append(CellType(name, color, nutrient_level, weight))
        return cell_types

    def generate(self):
        weights = [cell.weight for cell in self.cell_types]
        for x in range(self.width):
            for y in range(self.height):
                cell_type = np.random.choice(self.cell_types, p=weights)
                self.grid[x][y] = cell_type

    def display(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                cell_type = self.grid[x][y]
                pygame.draw.rect(screen, cell_type.color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
