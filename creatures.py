import random
import pygame
from cells import Cell


class Creature:
    def __init__(self, x, y, speed, color, size):
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


def generate_creatures(config):
    width = int(config['world']['width'])
    height = int(config['world']['height'])
    creatures = []
    num_prey = int(config['species']['prey_count'])
    speed_prey = int(config['species']['prey_speed'])
    color_prey = [int(x) for x in config['species']['prey_color'].split(',')]
    size_prey = int(config['species']['prey_size'])
    for _ in range(num_prey):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        prey = Creature(x, y, speed_prey, color_prey, size_prey)
        creatures.append(prey)
    num_predators = int(config['species']['predator_count'])
    speed_predator = int(config['species']['predator_speed'])
    color_predator = [int(x) for x in config['species']['predator_color'].split(',')]
    size_predator = int(config['species']['predator_size'])
    for _ in range(num_predators):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        predator = Creature(x, y, speed_predator, color_predator, size_predator)
        creatures.append(predator)
    return creatures
