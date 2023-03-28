import random
import pygame


class Creature:
    def __init__(self, x, y, speed, color, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.size = size
        self.vx = 0
        self.vy = 0

    def update(self):
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
