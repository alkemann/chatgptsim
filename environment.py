import random
import numpy as np
import pygame
from cells import CellType


class Environment:
    def __init__(self, config):
        self.width = int(config['world']['width'])
        self.height =  int(config['world']['height'])
        self.cell_size =  int(config['cell']['size'])
        self.cell_types = self.load_cell_types(config)
        rock = self.cell_types[0]
        self.grid = [[rock for x in range(self.width)] for y in range(self.height)]
        self.generate()

    def load_cell_types(self, config):
        cell_types = []
        for name, value in config["cell_types"].items():
            c1,c2,c3, nl, r, cr = value.split(",")
            color = (int(c1), int(c2), int(c3))
            nutrient_level = float(nl.strip())
            regions = int(r)
            cluster = int(cr)
            cell_types.append(CellType(name, color, 
                                       nutrient_level,
                                       regions, cluster
                                       ))
        return cell_types

    def generate(self):
        for ct in self.cell_types:
            if ct.regions > 0:
                cluster_radius = ct.cluster
                for _ in range(ct.regions):
                    x = random.randint(0, self.width-1)
                    y = random.randint(0, self.height-1)
                    self.grid[y][x] = ct
                    for j in range(-cluster_radius, cluster_radius+1):
                        for i in range(-cluster_radius, cluster_radius+1):
                            if 0 <= y+j < self.height and 0 <= x+i < self.width:
                                self.grid[y+j][x+i] = ct

    def display(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                cell_type = self.grid[y][x]
                pygame.draw.rect(screen, cell_type.color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
