import random
import pygame
import typing
from cells import Cell


class Creature:
    def __init__(self, name, x, y, speed, color, size, pasture, predator):
        self.name = name
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.size = size
        self.vx = 0
        self.vy = 0
        self.thirst = random.randint(0, 50)
        self.thirst_threshold = 100
        self.hunger = random.randint(0, 100)
        self.hunger_threshold = 100
        self.stamina = random.randint(0, 100)
        self.stamina_threshold = 100
        self.target_cell: Cell = None
        self.home = (x, y)
        self.pasture = pasture
        self.predator = predator

    def update(self, cells: typing.List[Cell]) -> None:
        self.thirst += 2
        self.hunger += 2
        self.stamina += 2

        if not self.target_cell:
            if self.stamina >= self.stamina_threshold:
                self.target_cell = Cell(self.home[0], self.home[1], "home", (0, 0, 0), 0, 0)
            elif self.thirst >= self.thirst_threshold:
                self.seek_water(cells)
            elif self.hunger >= self.hunger_threshold:
                self.seek_pasture(cells)

        if self.target_cell:
            return self.has_target()

        distance_to_home = ((self.x - self.home[0]) ** 2 + (self.y - self.home[1]) ** 2) ** 0.5
        if distance_to_home > 10:
            self.move_towards_home()
        else:
            if random.random() < 0.5:
                self.move_randomly()

    def seek_pasture(self, cells: typing.List[Cell]) -> None:
        self.seek_closest_cell(cells, self.pasture)

    def seek_water(self, cells: typing.List[Cell]) -> None:
        self.seek_closest_cell(cells, "water")

    def has_target(self):
        if self.target_cell.x == self.x and self.target_cell.y == self.y:
            if random.random() < 0.1:
                self.move_randomly()
            if self.thirst > 0 and self.target_cell.name == "water":
                return self.drink()
            if self.hunger > 0 and self.target_cell.name == self.pasture:
                return self.eat()
            if self.stamina > 0 and self.target_cell.name == "home":
                return self.rest()
            self.target_cell = None  # reset target cell
        else:
            self.move_towards_target()

    def rest(self):
        self.stamina -= 4
        self.hunger -= 1  # to simulate that resting takes less food than moving
        self.thirst -= 1  # to simulate that resting takes less water than moving
        if self.stamina <= 0:
            self.target_cell = None

    def eat(self):
        self.hunger -= 6
        if self.hunger <= 0:
            self.target_cell = None
        if self.hunger > self.hunger_threshold * 0.5 and self.thirst > self.thirst_threshold:
            self.target_cell = None
            # stop eatig and seek water

    # ... more methods ...

    def drink(self):
        self.thirst -= 50
        self.hunger -= 25  # to not bounce straight to eating
        if self.thirst < 0:
            self.target_cell = None

    def move_towards_home(self):
        dx = self.home[0] - self.x
        dy = self.home[1] - self.y
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        if magnitude != 0:
            self.vx = dx / magnitude
            self.vy = dy / magnitude
            self.x += self.vx * self.speed
            self.y += self.vy * self.speed

    def move_randomly(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.vx, self.vy = random.choice(directions)
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

    def move_towards_target(self):
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

    def render(self, screen, cell_size):
        x_pos = (self.x * cell_size) + (cell_size // 2)
        y_pos = (self.y * cell_size) + (cell_size // 2)
        pygame.draw.circle(screen, self.color, (x_pos, y_pos), self.size)
        x_pos = (self.home[0] * cell_size) + (cell_size // 2)
        y_pos = (self.home[1] * cell_size) + (cell_size // 2)
        pygame.draw.circle(screen, self.color, (x_pos, y_pos), self.size/2)

    def seek_closest_cell(self, cells: typing.List[Cell], target_cell_name: str) -> None:
        target_cells = [cell for cell in cells if cell.name == target_cell_name]
        if not target_cells:
            raise ValueError(f"No {target_cell_name} cells provided to creature seek_closest_cell")
        self.target_cell = min(target_cells, key=lambda cell: ((cell.x - self.x) ** 2 + (cell.y - self.y) ** 2) ** 0.5)

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
            pasture = config[section]['pasture']
            predator = bool(config[section]['predator'])
            home_type = config[section]['home']
            possible_home_cells = [cell for cell in cells if cell.name == home_type]
            for _ in range(number):
                new_home = random.choice(possible_home_cells)
                creature = Creature(creature_type, new_home.x, new_home.y, speed, color, size, pasture, predator)
                creatures.append(creature)

    return creatures

#