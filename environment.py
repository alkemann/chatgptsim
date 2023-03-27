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
        self.generate()

    def load_cell_types(self, config):
        cell_types = {}
        for name, value in config["cell_types"].items():
            c1,c2,c3, nutrient_level = value.split(",")
            color = (int(c1), int(c2), int(c3))
            nutrient_level = float(nutrient_level.strip())
            cell_types[name] = CellType(name, color, nutrient_level)

        return cell_types

    def generate(self):
        # Generate a random grid of cells
        for x in range(self.width // self.cell_size):
            for y in range(self.height // self.cell_size):
                cell_type = random.choices(self.cell_types)
                self.grid[x][y] = CellType(cell_type)

    def display(self):
        # Define colors for visualization
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Set up window and display environment
        screen_width = self.width * self.cell_size
        screen_height = self.height * self.cell_size
        screen = pygame.display.set_mode((screen_width, screen_height))
        for y in range(self.height):
            for x in range(self.width):
                if self.environment[y][x] == 0:
                    pygame.draw.rect(screen, WHITE, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, BLACK, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))

        pygame.display.update()
