import random
import pygame
from cells import Cell


class Creature:
    def __init__(self, name, x, y, speed, color, size):
        self.name = name
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.size = size
        self.vx = 0
        self.vy = 0
        self.thirst = random.randint(35, 50)
        self.thirst_threshold = 50  # arbitrary value for now
        self.target_cell: Cell = None
        self.home = (x, y)

    def seek_water(self, cells) -> None:
        water_cells = [cell for cell in cells if cell.name == "water"]
        if not water_cells:
            raise ValueError("No water cells provided to creature seek_water")
        self.target_cell = min(water_cells, key=lambda cell: ((cell.x - self.x) ** 2 + (cell.y - self.y) ** 2) ** 0.5)

    def update(self, cells):
        if not cells:
            raise ValueError("No cells provided to creature update")

        self.thirst += 1

        if self.thirst >= self.thirst_threshold and not self.target_cell:
            # print("Seeking water")
            self.seek_water(cells)

        if self.target_cell:
            if self.target_cell.x == self.x and self.target_cell.y == self.y:
                if self.thirst > 0 and self.target_cell.name == "water":
                    # print("Drinking")
                    self.thirst -= 5
                    if self.thirst < 0:
                        self.thirst = 0
                        self.target_cell = None
                    return  # don't move if we're on water and drinking
                self.target_cell = None
                # print("Done drinking")
            else:
                # print("Moving towards target cell")
                dx = self.target_cell.x - self.x
                dy = self.target_cell.y - self.y
                distance_to_target = (dx ** 2 + dy ** 2) ** 0.5
                if distance_to_target < self.speed:
                    self.x = self.target_cell.x
                    self.y = self.target_cell.y
                elif distance_to_target != 0:
                    self.vx = dx / distance_to_target
                    self.vy = dy / distance_to_target
                    self.x += self.vx * self.speed
                    self.y += self.vy * self.speed
        elif (((self.x - self.home[0]) ** 2 + (self.y - self.home[1]) ** 2) ** 0.5) > 10:
            # print("Moving towards home")
            dx = self.home[0] - self.x
            dy = self.home[1] - self.y
            magnitude = (dx ** 2 + dy ** 2) ** 0.5
            if magnitude != 0:
                self.vx = dx / magnitude
                self.vy = dy / magnitude
                self.x += self.vx * self.speed
                self.y += self.vy * self.speed
        else:
            # print("Moving randomly")
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            self.vx, self.vy = random.choice(directions)
            self.x += self.vx * self.speed
            self.y += self.vy * self.speed

    def render(self, screen, cell_size):
        x_pos = (self.x * cell_size) + (cell_size // 2)
        y_pos = (self.y * cell_size) + (cell_size // 2)
        pygame.draw.circle(screen, self.color, (x_pos, y_pos), self.size)


def generate_creatures(config, cells):
    creatures = []
    # Iterate over all sections and create creatures for each species
    for section in config.sections():
        if section.startswith('species/'):
            creature_type = section[8:]  # Extract the species name
            number = int(config[section]['count'])
            speed = int(config[section]['speed'])
            color = [int(x) for x in config[section]['color'].split(',')]
            size = int(config[section]['size'])
            home_type = config[section]['home']
            possible_home_cells = [cell for cell in cells if cell.name == home_type]
            for _ in range(number):
                new_home = random.choice(possible_home_cells)
                creature = Creature(creature_type, new_home.x, new_home.y, speed, color, size)
                creatures.append(creature)
                
    return creatures

